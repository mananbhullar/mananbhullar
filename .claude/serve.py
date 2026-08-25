import functools
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
handler = functools.partial(SimpleHTTPRequestHandler, directory=ROOT)
HTTPServer(('0.0.0.0', 8080), handler).serve_forever()
