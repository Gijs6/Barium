# Barium

![The Barium logo](logo.png)

A simple static site generator.  
Jekyll is undocumented, and Flask feels a bit too bulky when all you need is a simple static site, so Barium aims to be the best of both worlds.

Barium generates static HTML pages from Markdown files and Jinja templates. And that's it. You get a folder of clean, static files and you can host them however and wherever you like. After all, it's a static site generator, not a static site deployer.

It also includes a really simple HTTP server to help you preview your site during development, but please don't use it in production.

## Documentation

### Installation

To get started, run `pip install BariumSSG`. You can then just run `barium build` to build all pages and `barium serve` to start the development server.

### Building pages

Barium reads files from the import directory, puts them in a template, and saves the output HTML files in the export directory. Static files (i.e., all files other than Markdown) are not processed but just copied.

### Templates

You can set which template to use in a file's front matter (YAML) by setting the `template` property to a file name (including file extension). If no template is provided, Barium tries to use the `default_template` that is configured in the `config.yaml` file. If that file also doesn't exist, Barium will not use any template.  
The templates can be every file extension that Jinja supports. Inside the template, you can use the following variables through the `page`-dict:

- All front matter properties
- `path`: the complete path of the file
- `slug`: the name of the file
- `content`: the HTML content of the page
- All the global template variables set in the config file

Please view the [Jinja template documentation](https://jinja.palletsprojects.com/en/stable/templates/) for docs about the templates and its syntax.

### Configuration

You can configure the following settings in the `config.yaml` file. If a setting is not set, the *default/fallback* value will be used.

| Setting            | Description                                                                                                                 | Default/fallback |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| `import_dir`       | The directory where the Markdown files are located                                                                          | `./source`       |
| `export_dir`       | The directory where the HTML files should be built                                                                          | `./build`        |
| `template_dir`     | The directory where the template files are located                                                                          | `./templates`    |
| `template_vars`    | A dictionary of template variables that are available in all templates                                                      | `{}`             |
| `default_template` | The template that should be used if no template is specified in the front matter or if the file has no front matter at all. | `default.jinja`  |
| `port`             | The port where the files should be served                                                                                   | `8000`           |
