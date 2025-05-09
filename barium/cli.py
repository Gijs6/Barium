from jinja2 import Environment, FileSystemLoader, exceptions
import http.server
import socketserver
import os
import shutil
import commonmark
import re
import yaml
import sys


def serve(export_dir, port=8000):
    os.chdir(export_dir)

    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if not os.path.splitext(self.path)[1]:
                potential_path = self.path.lstrip("/") + ".html"
                if os.path.exists(potential_path):
                    self.path = "/" + potential_path

            return super().do_GET()

    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        print(f"Serving files at http://localhost:{port}")
        httpd.serve_forever()


def build(import_dir, export_dir, template_dir, template_vars):
    env = Environment(loader=FileSystemLoader(template_dir))

    for root, dirs, files in os.walk(export_dir):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    for root, dirs, files in os.walk("./source"):
        for file in files:
            source_path = os.path.join(root, file)
            file_path = os.path.join(root, file).removeprefix(import_dir)

            if file_path.endswith((".md", ".markdown")):
                build_path = (
                    export_dir
                    + file_path.removesuffix(".md").removesuffix(".markdown")
                    + ".html"
                )

                with open(source_path, encoding="utf-8") as source_file:
                    source_content = source_file.read()

                match = re.match(
                    r"^---\n(.*?)\n---\n?", source_content, flags=re.DOTALL
                )
                source_content_clean = re.sub(
                    r"^---\n.*?\n---\n?", "", source_content, flags=re.DOTALL
                )
                if match:
                    page_data = yaml.safe_load(match.group(1))

                    template = page_data.get("template", "default.jinja")

                    if template:
                        try:
                            jinja_template = env.get_template(template)

                            html_content = commonmark.commonmark(source_content_clean)

                            template_data = {
                                **page_data,
                                "path": file_path,
                                "slug": os.path.basename(file_path),
                                "content": html_content,
                                **template_vars
                            }

                            build_content = jinja_template.render(page=template_data)
                            print(
                                f"Sucesfully builded {file_path} in template {template}."
                            )
                        except exceptions.TemplateNotFound:
                            print(
                                f"{file_path} has no template in the front matter. No template is being used."
                            )
                            build_content = commonmark.commonmark(source_content_clean)

                else:
                    print(
                        f"{file_path} has no front matter. No template is being used."
                    )
                    build_content = commonmark.commonmark(source_content_clean)

                os.makedirs(os.path.dirname(build_path), exist_ok=True)

                with open(build_path, "w", encoding="utf-8") as build_file:
                    build_file.write(build_content)
            else:
                print(f"{file_path} is not a markdown file, so it is just copied.")
                destination_path = export_dir + file_path
                shutil.copy2(source_path, destination_path)


def main():
    if len(sys.argv) < 2:
        print("Usage: barium [build|serve]")
        sys.exit(1)


    config = {}


    with open("./config.yaml", encoding="utf-8") as cf:
        config_file = yaml.safe_load(cf)

    config["import_dir"] = config_file.get("import_dir", "./source")
    config["export_dir"] = config_file.get("export_dir", "./build")
    config["template_dir"] = config_file.get("template_dir", "./templates")
    config["template_vars"] = config_file.get("template_vars", {})

    

    action = sys.argv[1]
    if action == "build":
        build(**config)
    elif action == "serve":
        serve(**config)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
