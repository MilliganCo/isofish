import numpy as np
import OpenGL.GL as gl

# Таблица символов (от тёмного к светлому)
ASCII_CHARS = "@%#*+=-:. "

def brightness_to_char(brightness: float) -> str:
    """
    Превращает яркость (0..1) в символ из ASCII_CHARS.
    0 = самый тёмный символ, 1 = самый светлый (пробел).
    """
    idx = int(brightness * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[idx]

def read_framebuffer(width: int, height: int) -> np.ndarray:
    """
    Считывает пиксели из текущего OpenGL-фреймбуфера в numpy-массив RGBA (shape=(h,w,4)).
    """
    data = gl.glReadPixels(0, 0, width, height, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE)
    arr = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 4))
    return arr

def frame_to_ascii(arr: np.ndarray) -> list[str]:
    """
    Конвертирует массив пикселей (height, width, 4) в список ASCII-строк.
    """
    h, w, _ = arr.shape
    ascii_lines = []
    for y in range(h):
        row_chars = []
        for x in range(w):
            r, g, b, a = arr[y, x]
            # Простейшая яркость — среднее по каналам
            brightness = (r + g + b) / (3.0 * 255.0)
            c = brightness_to_char(brightness)
            row_chars.append(c)
        ascii_lines.append("".join(row_chars))
    return ascii_lines
