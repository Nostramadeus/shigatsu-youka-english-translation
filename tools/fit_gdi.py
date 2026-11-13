"""GDI text metrics through ctypes (Windows only, no window, memory DC). Shared helper for the fit scripts.

    from gdi import Font
    f = Font('ＭＳ Ｐ明朝', 30)            # lfHeight = +30 (cell height), default quality
    f.adv('a')      -> integer advance GetCharWidth32W
    f.tm            -> dict of TEXTMETRIC fields
    f.ggo('a')      -> (gmBlackBoxX, gmBlackBoxY, originX, originY, gmCellIncX) from GetGlyphOutlineW(GGO_METRICS)
"""
import ctypes
from ctypes import wintypes

gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)


class LOGFONTW(ctypes.Structure):
    _fields_ = [('lfHeight', wintypes.LONG), ('lfWidth', wintypes.LONG), ('lfEscapement', wintypes.LONG),
                ('lfOrientation', wintypes.LONG), ('lfWeight', wintypes.LONG), ('lfItalic', wintypes.BYTE),
                ('lfUnderline', wintypes.BYTE), ('lfStrikeOut', wintypes.BYTE), ('lfCharSet', wintypes.BYTE),
                ('lfOutPrecision', wintypes.BYTE), ('lfClipPrecision', wintypes.BYTE), ('lfQuality', wintypes.BYTE),
                ('lfPitchAndFamily', wintypes.BYTE), ('lfFaceName', wintypes.WCHAR * 32)]


class TEXTMETRICW(ctypes.Structure):
    _fields_ = [('tmHeight', wintypes.LONG), ('tmAscent', wintypes.LONG), ('tmDescent', wintypes.LONG),
                ('tmInternalLeading', wintypes.LONG), ('tmExternalLeading', wintypes.LONG),
                ('tmAveCharWidth', wintypes.LONG), ('tmMaxCharWidth', wintypes.LONG), ('tmWeight', wintypes.LONG),
                ('tmOverhang', wintypes.LONG), ('tmDigitizedAspectX', wintypes.LONG),
                ('tmDigitizedAspectY', wintypes.LONG), ('tmFirstChar', wintypes.WCHAR),
                ('tmLastChar', wintypes.WCHAR), ('tmDefaultChar', wintypes.WCHAR), ('tmBreakChar', wintypes.WCHAR),
                ('tmItalic', wintypes.BYTE), ('tmUnderlined', wintypes.BYTE), ('tmStruckOut', wintypes.BYTE),
                ('tmPitchAndFamily', wintypes.BYTE), ('tmCharSet', wintypes.BYTE)]


class POINTFX(ctypes.Structure):
    _fields_ = [('x', wintypes.LONG), ('y', wintypes.LONG)]


class GLYPHMETRICS(ctypes.Structure):
    _fields_ = [('gmBlackBoxX', wintypes.UINT), ('gmBlackBoxY', wintypes.UINT), ('ptx', wintypes.LONG),
                ('pty', wintypes.LONG), ('gmCellIncX', ctypes.c_short), ('gmCellIncY', ctypes.c_short)]


class FIXED(ctypes.Structure):
    _fields_ = [('fract', wintypes.WORD), ('value', ctypes.c_short)]


class MAT2(ctypes.Structure):
    _fields_ = [('eM11', FIXED), ('eM12', FIXED), ('eM21', FIXED), ('eM22', FIXED)]


class SIZE(ctypes.Structure):
    _fields_ = [('cx', wintypes.LONG), ('cy', wintypes.LONG)]


gdi32.CreateCompatibleDC.restype = wintypes.HDC
gdi32.CreateCompatibleDC.argtypes = [wintypes.HDC]
gdi32.CreateFontIndirectW.restype = wintypes.HFONT
gdi32.CreateFontIndirectW.argtypes = [ctypes.POINTER(LOGFONTW)]
gdi32.SelectObject.restype = wintypes.HGDIOBJ
gdi32.SelectObject.argtypes = [wintypes.HDC, wintypes.HGDIOBJ]
gdi32.GetTextMetricsW.argtypes = [wintypes.HDC, ctypes.POINTER(TEXTMETRICW)]
gdi32.GetCharWidth32W.argtypes = [wintypes.HDC, wintypes.UINT, wintypes.UINT, ctypes.POINTER(wintypes.INT)]
gdi32.GetGlyphOutlineW.restype = wintypes.DWORD
gdi32.GetGlyphOutlineW.argtypes = [wintypes.HDC, wintypes.UINT, wintypes.UINT, ctypes.POINTER(GLYPHMETRICS),
                                   wintypes.DWORD, ctypes.c_void_p, ctypes.POINTER(MAT2)]
gdi32.GetTextExtentPoint32W.argtypes = [wintypes.HDC, wintypes.LPCWSTR, ctypes.c_int, ctypes.POINTER(SIZE)]
gdi32.GetTextFaceW.argtypes = [wintypes.HDC, ctypes.c_int, wintypes.LPWSTR]

GGO_METRICS = 0
GGO_GRAY8_BITMAP = 6
SHIFTJIS_CHARSET = 128
DEFAULT_CHARSET = 1
_IDENT = MAT2(FIXED(0, 1), FIXED(0, 0), FIXED(0, 0), FIXED(0, 1))


class Font:
    def __init__(self, face, height, quality=0, charset=SHIFTJIS_CHARSET, weight=400):
        self.dc = gdi32.CreateCompatibleDC(None)
        lf = LOGFONTW()
        lf.lfHeight = height
        lf.lfWeight = weight
        lf.lfCharSet = charset
        lf.lfQuality = quality
        lf.lfFaceName = face
        self.h = gdi32.CreateFontIndirectW(ctypes.byref(lf))
        gdi32.SelectObject(self.dc, self.h)
        tm = TEXTMETRICW()
        gdi32.GetTextMetricsW(self.dc, ctypes.byref(tm))
        self.tm = {n: getattr(tm, n) for n, _ in TEXTMETRICW._fields_ if n.startswith('tm') and n not in (
            'tmFirstChar', 'tmLastChar', 'tmDefaultChar', 'tmBreakChar')}
        buf = ctypes.create_unicode_buffer(64)
        gdi32.GetTextFaceW(self.dc, 64, buf)
        self.realface = buf.value
        self._cache = {}

    def adv(self, ch):
        if ch not in self._cache:
            w = wintypes.INT(0)
            gdi32.GetCharWidth32W(self.dc, ord(ch), ord(ch), ctypes.byref(w))
            self._cache[ch] = w.value
        return self._cache[ch]

    def width(self, s):
        return sum(self.adv(c) for c in s)

    def extent(self, s):
        sz = SIZE()
        gdi32.GetTextExtentPoint32W(self.dc, s, len(s), ctypes.byref(sz))
        return sz.cx, sz.cy

    def ggo(self, ch, fmt=GGO_METRICS):
        gm = GLYPHMETRICS()
        r = gdi32.GetGlyphOutlineW(self.dc, ord(ch), fmt, ctypes.byref(gm), 0, None, ctypes.byref(_IDENT))
        if r == 0xFFFFFFFF:
            return None
        return gm.gmBlackBoxX, gm.gmBlackBoxY, gm.ptx, gm.pty, gm.gmCellIncX


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    for face in ('ＭＳ 明朝', 'ＭＳ Ｐ明朝', 'ＭＳ ゴシック', 'ＭＳ Ｐゴシック'):
        for h in (16, 20, 22, 25, 30, -25, -30):
            f = Font(face, h)
            t = f.tm
            print('%s h=%d real=%s  tmHeight %d asc %d desc %d intLead %d extLead %d ave %d max %d | i %d W %d a %d sp %d あ %d ― %d 　 %d | ggo a %s ggo8 a %s' % (
                face, h, f.realface, t['tmHeight'], t['tmAscent'], t['tmDescent'], t['tmInternalLeading'],
                t['tmExternalLeading'], t['tmAveCharWidth'], t['tmMaxCharWidth'], f.adv('i'), f.adv('W'), f.adv('a'),
                f.adv(' '), f.adv('あ'), f.adv('―'), f.adv('　'), f.ggo('a'), f.ggo('a', GGO_GRAY8_BITMAP)))
