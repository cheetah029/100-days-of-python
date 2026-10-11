# Compatibility layer loaded by run.html before a turtle project runs in Skulpt.
# Skulpt's turtle module is missing a few standard-library features that the
# course projects use; this adds them. Safe to run more than once.
import turtle as _t

if not getattr(_t, "_compat_applied", False):
    _t._compat_applied = True
    _OrigTurtle = _t.Turtle
    _OrigScreen = _t.Screen

    # Skulpt's built-in shape outlines (used to emulate shapesize()).
    _BASE_SHAPES = {
        "arrow": [(-10, 0), (10, 0), (0, 10)],
        "square": [(10, -10), (10, 10), (-10, 10), (-10, -10)],
        "triangle": [(10, -5.77), (0, 11.55), (-10, -5.77)],
        "classic": [(0, 0), (-5, -9), (0, -7), (5, -9)],
        "turtle": [(0, 16), (-2, 14), (-1, 10), (-4, 7), (-7, 9), (-9, 8), (-6, 5),
                   (-7, 1), (-5, -3), (-8, -6), (-6, -8), (-4, -5), (0, -7), (4, -5),
                   (6, -8), (8, -6), (5, -3), (7, 1), (6, 5), (9, 8), (7, 9), (4, 7),
                   (1, 10), (2, 14)],
        "circle": [(10, 0), (9.51, 3.09), (8.09, 5.88), (5.88, 8.09), (3.09, 9.51),
                   (0, 10), (-3.09, 9.51), (-5.88, 8.09), (-8.09, 5.88), (-9.51, 3.09),
                   (-10, 0), (-9.51, -3.09), (-8.09, -5.88), (-5.88, -8.09),
                   (-3.09, -9.51), (0, -10), (3.09, -9.51), (5.88, -8.09),
                   (8.09, -5.88), (9.51, -3.09)],
    }

    # colormode(255) support: Skulpt's own colormode is broken, so colour
    # arguments given as 0-255 RGB are converted to hex strings here.
    _cmode = [1]

    def _is_rgb(v):
        return isinstance(v, (tuple, list)) and len(v) == 3

    def _conv(args):
        if _cmode[0] != 255:
            return args
        if len(args) == 3 and not any(isinstance(a, (str, tuple, list)) for a in args):
            args = ((args[0], args[1], args[2]),)
        out = []
        for a in args:
            if _is_rgb(a):
                out.append("#%02x%02x%02x" % (int(a[0]), int(a[1]), int(a[2])))
            else:
                out.append(a)
        return tuple(out)

    class Turtle(_OrigTurtle):
        """Turtle with shapesize()/turtlesize(), teleport() and friends."""

        def color(self, *args):
            if not args:
                return _OrigTurtle.color(self)
            return _OrigTurtle.color(self, *_conv(args))

        def pencolor(self, *args):
            if not args:
                return _OrigTurtle.pencolor(self)
            return _OrigTurtle.pencolor(self, *_conv(args))

        def fillcolor(self, *args):
            if not args:
                return _OrigTurtle.fillcolor(self)
            return _OrigTurtle.fillcolor(self, *_conv(args))

        def dot(self, size=None, *color):
            if size is None:
                return _OrigTurtle.dot(self)
            return _OrigTurtle.dot(self, size, *_conv(color))

        def shape(self, name=None):
            if name is None:
                return getattr(self, "_cp_base", None) or _OrigTurtle.shape(self)
            _OrigTurtle.shape(self, name)
            self._cp_base = name
            if getattr(self, "_cp_stretch", None) and name in _BASE_SHAPES:
                self._cp_apply()

        def _cp_apply(self):
            wid, length = self._cp_stretch
            base = self._cp_base
            if base not in _BASE_SHAPES or (wid == 1 and length == 1):
                return
            name = "_sz_%s_%s_%s" % (base, wid, length)
            if name not in _OrigScreen().getshapes():
                # shapes point along +y (heading), so length scales y and width scales x
                _t.register_shape(name, [[x * wid, y * length] for x, y in _BASE_SHAPES[base]])
            _OrigTurtle.shape(self, name)

        def shapesize(self, stretch_wid=None, stretch_len=None, outline=None):
            current = getattr(self, "_cp_stretch", None) or (1, 1)
            if stretch_wid is None and stretch_len is None and outline is None:
                return (current[0], current[1], 1)
            if stretch_wid is not None:
                new = (stretch_wid, stretch_wid if stretch_len is None else stretch_len)
            elif stretch_len is not None:
                new = (current[0], stretch_len)
            else:
                new = current
            self._cp_stretch = new
            if not getattr(self, "_cp_base", None):
                self._cp_base = _OrigTurtle.shape(self)
            self._cp_apply()

        turtlesize = shapesize

        def resizemode(self, rmode=None):
            return "user"

        def teleport(self, x=None, y=None, fill_gap=False):
            was_down = self.isdown()
            self.penup()
            self.goto(x, y)
            if was_down:
                self.pendown()

    class _ScreenProxy:
        """Wraps Skulpt's Screen to add textinput/numinput/onkeypress."""

        def __init__(self, real):
            self._real = real

        def __getattr__(self, name):
            return getattr(self._real, name)

        def textinput(self, title, prompt):
            return input(str(title) + "\n\n" + str(prompt))

        def numinput(self, title, prompt, default=None, minval=None, maxval=None):
            while True:
                text = input(str(title) + "\n\n" + str(prompt))
                if text == "":
                    return default
                try:
                    value = float(text)
                except ValueError:
                    continue
                if (minval is None or value >= minval) and (maxval is None or value <= maxval):
                    return value

        def colormode(self, cmode=None):
            if cmode is not None:
                _cmode[0] = 255 if cmode == 255 else 1
            return _cmode[0]

        def bgcolor(self, *args):
            if not args:
                return self._real.bgcolor()
            self._cp_bg = args
            return self._real.bgcolor(*_conv(args))

        def setup(self, *args, **kwargs):
            # Skulpt resizes its canvases here, which wipes a background set
            # earlier with bgcolor(); CPython's turtle keeps it, so repaint.
            result = self._real.setup(*args, **kwargs)
            bg = getattr(self, "_cp_bg", None)
            if bg is not None:
                self._real.bgcolor(*_conv(bg))
            return result

        def onkeypress(self, fun, key=None):
            if key is None:
                key = "space"
            self._real.onkey(fun, key)

        def onkeyrelease(self, fun, key=None):
            pass  # not supported by Skulpt

        def getcanvas(self):
            return None

    _screen_singleton = []

    def Screen():
        if not _screen_singleton:
            _screen_singleton.append(_ScreenProxy(_OrigScreen()))
        return _screen_singleton[0]

    def colormode(cmode=None):
        return Screen().colormode(cmode)

    def bgcolor(*args):
        return Screen().bgcolor(*args)

    def setup(*args, **kwargs):
        return Screen().setup(*args, **kwargs)

    def textinput(title, prompt):
        return Screen().textinput(title, prompt)

    def numinput(title, prompt, default=None, minval=None, maxval=None):
        return Screen().numinput(title, prompt, default, minval, maxval)

    def onkeypress(fun, key=None):
        Screen().onkeypress(fun, key)

    def onkeyrelease(fun, key=None):
        pass

    _t.Turtle = Turtle
    _t.Screen = Screen
    _t.colormode = colormode
    _t.bgcolor = bgcolor
    _t.setup = setup
    _t.textinput = textinput
    _t.numinput = numinput
    _t.onkeypress = onkeypress
    _t.onkeyrelease = onkeyrelease
    if not hasattr(_t, "RawTurtle"):
        _t.RawTurtle = Turtle


# ---- open(): Skulpt rejects keyword args (mode="w") and file writes. ----
# run.html installs `_cp_open` as the `open` builtin after this file has run.
# Writes go to an in-memory "disk" for the session; reads of anything not
# written fall back to Skulpt's own open().
_real_open = open
_fs = {}


class _VFile:
    def __init__(self, name, text, writable):
        self.name = name
        self._text = text
        self._pos = 0
        self._writable = writable
        self.closed = False

    def read(self, size=-1):
        if size is None or size < 0:
            out = self._text[self._pos:]
            self._pos = len(self._text)
        else:
            out = self._text[self._pos:self._pos + size]
            self._pos += len(out)
        return out

    def readline(self):
        i = self._text.find("\n", self._pos)
        end = len(self._text) if i < 0 else i + 1
        out = self._text[self._pos:end]
        self._pos = end
        return out

    def readlines(self):
        lines = []
        while True:
            line = self.readline()
            if not line:
                return lines
            lines.append(line)

    def __iter__(self):
        return iter(self.readlines())

    def write(self, text):
        if not self._writable:
            raise IOError("File not open for writing")
        self._text += str(text)
        _fs[self.name] = self._text
        return len(str(text))

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


def _cp_open(name, mode="r", *args, **kwargs):
    if "w" in mode or "a" in mode or "x" in mode or "+" in mode:
        base = _fs.get(name, "") if ("a" in mode or "+" in mode) else ""
        _fs[name] = base
        return _VFile(name, base, True)
    if name in _fs:
        return _VFile(name, _fs[name], False)
    return _real_open(name, mode)
