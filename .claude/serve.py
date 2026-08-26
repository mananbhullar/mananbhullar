import functools
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(os.environ.get('PORT', 8080))
handler = functools.partial(SimpleHTTPRequestHandler, directory=ROOT)
HTTPServer(('0.0.0.0', PORT), handler).serve_forever()
