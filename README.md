# Barium

![The Barium logo](logo.png)

A simple static site generator.  
Jekyll is undocumented, and Flask feels a bit too bulky when all you need is a simple static site, so Barium aims to be the best of both worlds.

Barium generates static HTML pages from Markdown files and Jinja templates. And that's it. You get a folder of clean, static files and you can host them however and wherever you like. After all, it's a static site generator, not a static site deployer.

It also includes a really simple HTTP server to help you preview your site during development please don't use it in production.

## Documentation

To get started, run `pip install BariumSSG`. You can then just run `barium build` and `barium serve`.

Barium reads files from the import directory, processes them with templates, and saves the output HTML files in the export directory.  Files other than markdown are just copied.  
You can set which template to use in a file's front matter by setting the `template` to a file name (including file extension) property. If no template is provided, Barium tries to use `default.jinja`.  
The templates can be every file extension that jinja supports. Inside the template, you can use the following variables through the `page`-dict:

- All front matter properties
- `path`: the complete path of the file
- `slug`: the name of the file
- `content`: the HTML-content of the page
- All the global template variables set in the config file

You can confige settings in the `config.yaml` file.

| Property        | Description                                                         | Standard value |
| --------------- | ------------------------------------------------------------------- | -------------- |
| `import_dir`    | The directory where the markdown files are located                  | `./source`     |
| `export_dir`    | The directory where the HTML files should be built                  | `./build`      |
| `template_dir`  | The directory where the template files are located                  | `./templates`  |
| `template_vars` | A dictonary of template vaiables that are avaiable in all templates | `{}`           |
