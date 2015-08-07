# Live Reload Server

This HTTP server serves static files from a specified directory. In addition to
that, it watches the directories for changes and forces the browsers that
are connected to it to reload so they can get the latest version. This is
accomplished by injecting a small JS snippet into the HTML sent back to the
browser.

Although, I called this server "Live Reload", this protocol is not the
standardized one.

# Installation

Install directly from git using pip
```bash
sudo pip install git+git://github.com/prashanthellina/livereload_server.git
```

or clone the code locally and install
```bash
git clone https://github.com/prashanthellina/livereload_server.git
cd livereload_server
sudo python setup.py install
```

# Usage

```bash
livereload_server -h
usage: __init__.py [-h] [--address ADDRESS] [--port PORT] path

Run a HTTP server serving static files with live reload functionality

positional arguments:
  path               Directory to serve

optional arguments:
  -h, --help         show this help message and exit
  --address ADDRESS
  --port PORT
```

```bash
livereload_server --address 0.0.0.0 --port 8000 <path_to_static_files_dir>
```
