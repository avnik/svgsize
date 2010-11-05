import pkg_resources
pkg_resources.declare_namespace(__name__)

import re
from xml.sax import handler,  make_parser
from xml.sax.handler import feature_namespaces

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

SVG_NS = u"http://www.w3.org/2000/svg"

_unitLenght = {
    'px': 1.0,
    'pt': 1.25,
    'pc': 15.0,
    'mm': 3.543307,
    'cm': 35.43307,
    'in': 90.0,
    None: 1.0, # "User units" pixels by default
    '%' : 2.0, # Fake it!
}

class SVGError(RuntimeError):
    pass

SIZE_RE=re.compile('^(\\d+(?:\\.\\d+)?)(em|ex|px|pt|pc|cm|mm|in)?$')

def svg_unit(lenght):
    match = SIZE_RE.match(lenght)
    if match:
        return float(match.group(1)), match.group(2)
    else:
        # I'm believe -- NNNpx is int
        return int(lenght), None

class _SVG(handler.ContentHandler):
    def __init__(self, convert=True):
        handler.ContentHandler.__init__(self)
        self.found = False
        self.convert = convert
        self.height = None
        self.height_units = None
        self.width = None
        self.width_units = None

    def startElementNS(self, name, qname, attrs):
        (uri, localname) = name
        if uri == SVG_NS and localname == u"svg":
            data = {}
            for (ns, aname), value in attrs.items():
                if ns is None:
                    data[aname] = value
            
            self.height, self.height_units = svg_unit(data['height'])
            self.width, self.width_units = svg_unit(data['width'])
            self.found = True

def _process_svg_file(svgfile, convert=True):
    handler = _SVG()
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setFeature(feature_namespaces, True)
    while not handler.found:
        chunk = svgfile.read(1024)
        if not chunk:
            raise SVGError()
        parser.feed(chunk)
    
    if convert:
        h = handler.height * _unitLenght[handler.height_units]
        w = handler.width * _unitLenght[handler.width_units]
        return (w, h)
    else:
        return ((handler.height, handler.height_units),
                (handler.width, handler.width_units))



def get_SVG_size(svgfile, convertToPixels=True):
    return _process_svg_file(StringIO(svgfile), convertToPixels)

def get_SVG_file_size(svgfile, convertToPixels=True):
    return _process_svg_file(open(svgfile, 'r'), convertToPixels)

