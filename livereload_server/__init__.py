#!/usr/bin/env python

import os
import re
import argparse
import mimetypes

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tornado.ioloop
import tornado.web

# This JS snippet below is embedded dynamically in every
# HTML response sent back from this server. The JS code
# establishes a connection with the server using Ajax.
# The server terminates connection when *any* file changes
# thus forcing a reload from JS in browser
JS = '''
<script>

function livereload() {
    var xmlhttp;

    if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            location.reload();
        }
    }

    xmlhttp.open("GET", "/_listen", true);
    xmlhttp.send();
}

livereload();

</script>
'''

class ListenHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        # add connection to list of known client
        # connections and then keep the conn open
        self.application.conns[id(self)] = self

    def on_connection_close(self):
        # if connection is closed by client for whatever
        # reason, ensure we clean up the state
        if id(self) in self.application.conns:
            del self.application.conns[id(self)]

class LocalFSEventHandler(FileSystemEventHandler):
    def __init__(self, on_change):
        self.on_change = on_change

    def on_any_event(self, evt):
        self.on_change()

def close_all_conns(app):
    '''
    Close all the client connections on this server
    thereby forcing JS client code to issues reload
    to the browser.
    '''
    conns = app.conns
    app.conns = {}
    for c in conns.itervalues():
        c.finish()

class StaticFileHandler(tornado.web.RequestHandler):
    def get(self, path):
        path = os.path.join(self.application.args.path, path)

        # default file is index.html
        if os.path.isdir(path):
            path = os.path.join(path, 'index.html')

        if not os.path.exists(path): return

        # guess mime type from file extension
        ctype, _ = mimetypes.guess_type(path)
        self.set_header("Content-Type", ctype)

        # read file contents and embed JS before
        # writing to client
        d = open(path).read()
        d = re.sub(r'<\s*/\s*body\s*>(?i)', JS + '</body>', d)
        self.write(d)

def main():
    parser = argparse.ArgumentParser(description='Run a HTTP server serving'
        ' static files with live reload functionality')
    parser.add_argument('path', help='Directory to serve')
    parser.add_argument('--address', default='127.0.0.1')
    parser.add_argument('--port', default=8000)
    args = parser.parse_args()

    app = tornado.web.Application([
        (r"/_listen", ListenHandler),
        (r"/(.*)", StaticFileHandler),
    ])

    app.args = args
    app.conns = {}

    # initialize the filesystem listener
    # to track change events
    app.fs_observer = Observer()
    app.fs_observer.schedule(LocalFSEventHandler(lambda: close_all_conns(app)),
        args.path, recursive=True)
    app.fs_observer.start()

    # start server
    app.listen(args.port, args.address)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
