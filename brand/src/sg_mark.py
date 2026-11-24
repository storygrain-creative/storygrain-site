"""StoryGrain mark and wordmark geometry, read from the vectors live on storygrain.co
(the #sg-mark and #sg-word symbols in _symbols.html). Mark units = the raw path units."""
import os, re
from svgpathtools import parse_path
from shapely.geometry import Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
_SYM = open(os.path.join(HERE, '_symbols.html')).read()

def _symbol(name):
    m = re.search(r'<symbol id="%s" viewBox="([^"]+)">(.*?)</symbol>' % name, _SYM, re.S)
    body = m.group(2)
    p = re.search(r'transform="([^"]+)" d="([^"]+)"', body)
    return m.group(1), p.group(1), p.group(2)

MARK_VIEWBOX, MARK_TRANSFORM, MARK_D = _symbol('sg-mark')
WORD_VIEWBOX, WORD_TRANSFORM, WORD_D = _symbol('sg-word')

def path_d():
    return MARK_D

def polygons(samples=160):
    """One shapely Polygon per blade, in mark units."""
    polys = []
    for sub in re.findall(r'M[^M]+', MARK_D):
        path = parse_path(sub)
        pts = []
        for seg in path:
            for i in range(samples):
                z = seg.point(i / samples)
                pts.append((z.real, z.imag))
        polys.append(Polygon(pts).buffer(0))
    return polys

def bounds():
    ps = polygons()
    return (min(p.bounds[0] for p in ps), min(p.bounds[1] for p in ps),
            max(p.bounds[2] for p in ps), max(p.bounds[3] for p in ps))

def word_box():
    """Wordmark bounds in its own viewBox units (x, y, w, h)."""
    x, y, w, h = map(float, WORD_VIEWBOX.split())
    return x, y, w, h
