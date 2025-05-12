from jinja2 import Environment, FileSystemLoader, exceptions
import http.server
import socketserver
import os
import shutil
import re
import yaml
import sys
from markdown_it import MarkdownIt
from importlib.metadata import version

__version__ = version("BariumSSG")


def serve(**config):
    export_dir = config["export_dir"]
    port = config["port"]

    os.chdir(export_dir)

    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if not os.path.splitext(self.path)[1]:
                potential_path = self.path.lstrip("/") + ".html"
                if os.path.exists(potential_path):
                    self.path = "/" + potential_path

            return super().do_GET()

    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        print(f"Serving files at http://localhost:{port}.")
        httpd.serve_forever()


def build(**config):
    import_dir = config["import_dir"]
    export_dir = config["export_dir"]
    template_dir = config["template_dir"]
    template_vars = config["template_vars"]
    default_template = config["default_template"]


    env = Environment(loader=FileSystemLoader(template_dir))

    md_renderer = MarkdownIt()

    # Clean the export dir

    for root, dirs, files in os.walk(export_dir):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    for root, dirs, files in os.walk(import_dir):
        for file in files:
            source_path = os.path.join(root, file)
            file_path = os.path.join(root, file).removeprefix(import_dir)

            if os.path.splitext(file_path)[1] in [".md", ".markdown"]:
                # So if not a static file, but a markdown, that needs to be built

                build_path = (
                    export_dir
                    + os.path.splitext(file_path)[0]
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
                    template = page_data.get("template")
                    if not template:
                        print(
                            f"{file_path} has no template property set in the front matter. Attempting to use {default_template}."
                        )
                        template = default_template
                else:
                    print(
                        f"{file_path} has no front matter at all. Attempting to use {default_template}."
                    )
                    template = default_template

                try:
                    jinja_template = env.get_template(template)

                    html_content = md_renderer.render(source_content_clean)

                    template_page_data = {
                        **page_data,
                        "path": file_path,
                        "slug": os.path.basename(file_path),
                        "content": html_content,
                        **template_vars,
                    }

                    build_content = jinja_template.render(page=template_page_data)
                    print(f"Sucesfully builded {file_path} in template {template}.")

                except exceptions.TemplateNotFound:
                    print(
                        f"{template} is not a template. {file_path} is built without a template!"
                    )
                    build_content = md_renderer.render(source_content_clean)

                os.makedirs(os.path.dirname(build_path), exist_ok=True)

                with open(build_path, "w", encoding="utf-8") as build_file:
                    build_file.write(build_content)
            else:
                # The file is not a markdown file, so it is just copied over
                destination_path = export_dir + file_path
                shutil.copy2(source_path, destination_path)


def main():
    print(f"BariumSSG {__version__}")

    if len(sys.argv) < 2:
        print("Usage: barium [build|serve]")
        sys.exit(1)

    config = {}

    try:
        with open("./config.yaml", encoding="utf-8") as cf:
            config_file = yaml.safe_load(cf)
    except FileNotFoundError:
        print("No config file found. Default values are used.")
        config_file = {}

    if not config_file:
        print("No valid config file. Default values are used.")
        config_file = {}

    config["import_dir"] = config_file.get("import_dir", "./source")
    config["export_dir"] = config_file.get("export_dir", "./build")
    config["template_dir"] = config_file.get("template_dir", "./templates")
    config["template_vars"] = config_file.get("template_vars", {})
    config["default_template"] = config_file.get("default_template", "default.jinja")
    config["port"] = config_file.get("port", 8000)

    action = sys.argv[1]
    if action == "build":
        build(**config)
    elif action == "serve":
        serve(**config)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
