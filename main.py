import http.server
import socketserver

import os
import shutil

import commonmark


IMPORT_DIR = "./source"
EXPORT_DIR = "./build"

def serve(port=8000):
    os.chdir(EXPORT_DIR)

    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving files at http://localhost:{port}")
        httpd.serve_forever()

def build():
    for root, dirs, files in os.walk(EXPORT_DIR):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    for root, dirs, files in os.walk("./source"):
        for file in files:
            source_path = os.path.join(root, file)
            build_path = EXPORT_DIR + os.path.join(root, file).removeprefix(IMPORT_DIR).removesuffix(".md").removesuffix(".markdown") + ".html"
            
            with open(source_path, encoding="utf-8") as source_file:
                source_content = source_file.read()
            
            build_content = commonmark.commonmark(source_content)

            os.makedirs(os.path.dirname(build_path), exist_ok=True)

            with open(build_path, "w", encoding="utf-8") as build_file:
                build_file.write(build_content)

if __name__ == "__main__":
    build()
    serve()
