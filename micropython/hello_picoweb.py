#
# This is a picoweb example showing a centralized web page route
# specification (classical Django style).
#
import ure as re
import picoweb
from machine import Pin


def index(req, resp):
    # You can construct an HTTP response completely yourself, having
    # a full control of headers sent...
    yield from resp.awrite("HTTP/1.0 200 OK\r\n")
    yield from resp.awrite("Content-Type: text/html\r\n")
    yield from resp.awrite("\r\n")
    yield from resp.awrite("I can show you a table of <a href='squares'>squares</a>.<br/>")
    yield from resp.awrite("Or my <a href='file'>source</a><br/>")
    yield from resp.awrite("Toggle LED <a href='pin'>Toggle</a>.")


def squares(req, resp):
    # Or can use a convenience function start_response() (see its source for
    # extra params it takes).
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "squares.tpl", (req,))


def hello(req, resp):
    yield from picoweb.start_response(resp)
    # Here's how you extract matched groups from a regex URI match
    yield from resp.awrite("Hello " + req.url_match.group(1))

def set_pin(req, resp):
    global led_value
    pin = Pin(2, Pin.OUT)
    pin.value(led_value)
    led_value = 1 - led_value
    yield from picoweb.start_response(resp)
    yield from resp.awrite("Pin value has been changed tp {!r}".format(led_value))


led_value = 1

ROUTES = [
    # You can specify exact URI string matches...
    ("/", index),
    ("/squares", squares),
    ("/file", lambda req, resp: (yield from app.sendfile(resp, "hello_picoweb.py"))),
    ("/pin", set_pin),
    # ... or match using a regex, a match result available as req.url_match
    # for group extraction in your view.
    (re.compile("^/iam/(.+)"), hello),
]


import logging
logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

app = picoweb.WebApp(__name__, ROUTES)
app.run(host="0.0.0.0", port=7000, debug=True)