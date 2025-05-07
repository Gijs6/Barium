# Barium

![The Barium logo](logo.png)

A simple static site generator.  
Jekyll is undocumented, and Flask feels a bit too bulky when all you need is a simple static site, so Barium aims to be the best of both worlds.

Barium generates static HTML pages from Markdown files and Jinja templates. And that's it. You get a folder of clean, static files and you can host them however and wherever you like. After all, it's a static site generator, not a static site deployer.

It also includes a really simple HTTP server to help you preview your site during development please don't use it in production.

## Documentation

To get started, run `pip install BariumSSG`. You can then just run `barium build` and `barium serve`.

Barium reads files from the `source` directory, processes them with templates from the `templates` directory, and saves the output HTML files in the `build` directory.  
You can set which template to use in a file's front matter by setting the `template` to a file name (including file extension) property. If no template is provided, Barium tries to use `default.jinja`.  
The templates can be every file extension that jinja supports. Inside the template, you can use the following variables through the `page`-dict:

- All front matter properties
- `path`: the complete path of the file
- `slug`: the name of the file
- `content`: the HTML-content of the page
