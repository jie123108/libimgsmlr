from ctypes import *
import os.path
import logging
import filetype
import logging
import math

so_name = "libimgsmlr.so"
so_path_name = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + so_name
try:
    libimgsmlr = cdll.LoadLibrary(so_path_name)
except OSError as ex:
    logging.error("ctypes.cdll.LoadLibrary(%s) failed! ex: %s", so_path_name, ex)
    raise ex

g_precision = 6
def set_sim_float_precision(precision):
    global g_precision
    g_precision = precision


"""
typedef struct
{
    float values[PATTERN_SIZE][PATTERN_SIZE];
} Pattern;

typedef float Signature[SIGNATURE_SIZE];
int shuffle_pattern(Pattern* patternDst, Pattern* patternSrc);
int pattern2signature(Pattern* pattern, Signature signature);
Pattern* jpeg2pattern(void* img, int size, Pattern* pattern);
Pattern* png2pattern(void* img, int size, Pattern* pattern);
Pattern* gif2pattern(void* img, int size, Pattern* pattern);
Pattern* webp2pattern(void* img, int size, Pattern* pattern);
"""

PATTERN_SIZE = 64
SIGNATURE_SIZE = 16

class Pattern(Structure):
    _fields_ = [("values", c_float * PATTERN_SIZE * PATTERN_SIZE)]
    def as_array(self):
        arr = []
        for i in range(PATTERN_SIZE):
            arr2 = []
            for j in range(PATTERN_SIZE):
                arr2.append(round(self.values[i][j], g_precision))
            arr.append(arr2)
        return arr

    def is_empty(self):
        for i in range(PATTERN_SIZE):
            arr2 = []
            for j in range(PATTERN_SIZE):
                if not math.isnan(self.values[i][j]):
                    return False
        return True

Pattern_p = POINTER(Pattern)
Signature = c_float * SIGNATURE_SIZE

def initImg2PatternFunc(func):
    func.argtypes = (c_void_p, c_int, Pattern_p)
    func.restype = Pattern_p
    return func

def initJpeg2patternFunc():
    return initImg2PatternFunc(libimgsmlr.jpeg2pattern)

def initPng2patternFunc():
    return initImg2PatternFunc(libimgsmlr.png2pattern)

def initGif2patternFunc():
    return initImg2PatternFunc(libimgsmlr.gif2pattern)

def initWebp2patternFunc():
    return initImg2PatternFunc(libimgsmlr.webp2pattern)

def initPattern2signatureFunc():
    pattern2signature = libimgsmlr.pattern2signature
    pattern2signature.argtypes = (Pattern_p, Signature)
    pattern2signature.restype = c_int
    return pattern2signature

def initShufflePatternFunc():
    shuffle_pattern = libimgsmlr.shuffle_pattern
    shuffle_pattern.argtypes = (Pattern_p, Pattern_p)
    shuffle_pattern.restype = c_int
    return shuffle_pattern

c_jpeg2pattern = initJpeg2patternFunc()
c_png2pattern = initPng2patternFunc()
c_gif2pattern = initGif2patternFunc()
c_webp2pattern = initWebp2patternFunc()
c_pattern2signature = initPattern2signatureFunc()
c_shuffle_pattern = initShufflePatternFunc()

def jpeg2pattern(img: bytes):
    patternBuf = Pattern()
    pattern = c_jpeg2pattern(img, len(img), patternBuf)
    if pattern:
        # If the pattern is empty, it may be because the image is a solid color image.
        if patternBuf.is_empty():
            return False, "not supported solid color image"
        return True, patternBuf
    return False, "not a valid jpeg file"

def png2pattern(img: bytes):
    patternBuf = Pattern()
    pattern = c_png2pattern(img, len(img), patternBuf)
    if pattern:
        # If the pattern is empty, it may be because the image is a solid color image.
        if patternBuf.is_empty():
            return False, "not supported solid color image"
        return True, patternBuf
    return False, "not a valid png file"

def gif2pattern(img: bytes):
    patternBuf = Pattern()
    pattern = c_gif2pattern(img, len(img), patternBuf)
    if pattern:
        # If the pattern is empty, it may be because the image is a solid color image.
        if patternBuf.is_empty():
            return False, "not supported solid color image"
        return True, patternBuf
    return False, "not a valid gif file"

def webp2pattern(img: bytes):
    patternBuf = Pattern()
    pattern = c_webp2pattern(img, len(img), patternBuf)
    if pattern:
        # If the pattern is empty, it may be because the image is a solid color image.
        if patternBuf.is_empty():
            return False, "not supported solid color image"
        return True, patternBuf
    return False, "not a valid webp file"


def img2pattern(img: bytes):
    if type(img) != bytes:
        raise ValueError("Need a bytes")

    kind = filetype.guess(img)
    if not kind:
        raise ValueError("not a valid image file")

    pattern = None
    if kind.mime == "image/jpeg":
        ok, pattern = jpeg2pattern(img)
    elif kind.mime == "image/png":
        ok, pattern = png2pattern(img)
    elif kind.mime == "image/gif":
        ok, pattern = gif2pattern(img)
    # elif kind.mime == "image/webp":
    #     ok, pattern = webp2pattern(img)
    else:
        raise ValueError("'%s' not supported" % kind.mime)
    if not ok:
        raise ValueError(pattern)

    return pattern

def pattern2signature(pattern):
    if not pattern:
        raise ValueError("pattern cannot be None")

    c_signature = Signature()
    c_pattern2signature(pattern, c_signature)
    signature = []
    for sign in c_signature:
        signature.append(round(sign, g_precision))
    return signature

def shuffle_pattern(pattern):
    if not pattern:
        raise ValueError("pattern cannot be None")
    patternOut = Pattern()
    c_shuffle_pattern(patternOut, pattern)
    return patternOut
