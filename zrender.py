import glfw, math
from OpenGL.GL import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# -----------------------
# Window & input helpers
# -----------------------

# Key states
_key_states = {}
_mouse_states = {}

# Key/mouse constants
class wkey:
    RELEASE = 0
    PRESS = 1
    HOLD = 2

class wmouse:
    RELEASE = 0
    PRESS = 1
    HOLD = 2

def win_rtext(x, y, text, r, g, b, a, font_size=32, window_width=800, window_height=600):
    # Load font
    font = ImageFont.truetype("arial.ttf", font_size)

    # Measure text size
    dummy_img = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0,0), text, font=font)  # (x0, y0, x1, y1)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Create an image for the text
    img = Image.new("RGBA", (text_width, text_height), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.text((-bbox[0], -bbox[1]), text, font=font, fill=(int(r), int(g), int(b), int(a*255)))

    # Convert to numpy array
    data = np.array(img, dtype=np.uint8)

    # Create OpenGL texture
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    glEnable(GL_TEXTURE_2D)

    # Convert pixel coordinates to OpenGL coordinates
    s_x = img.width / window_width * 2
    s_y = img.height / window_height * 2
    cx = (x / window_width) * 2 - 1
    cy = (y / window_height) * 2 - 1

    glColor4f(1, 1, 1, 1)

    # Draw textured quad
    glBegin(GL_QUADS)
    glTexCoord2f(0,1); glVertex2f(cx, cy)
    glTexCoord2f(1,1); glVertex2f(cx + s_x, cy)
    glTexCoord2f(1,0); glVertex2f(cx + s_x, cy + s_y)
    glTexCoord2f(0,0); glVertex2f(cx, cy + s_y)
    glEnd()

    # Clean up
    glDeleteTextures([tex])

# -----------------------
# Window functions
# -----------------------
def win_closing(window):
    data = glfw.get_window_user_pointer(window)
    return data["closing"]

def win_make(width, height, title, resizable=True):
    print("Made with use of ZRender. Github: https://github.com/zurek4320/zrender")

    if not glfw.init():
        raise Exception("GLFW could not be initialized")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_ANY_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, glfw.TRUE if resizable else glfw.FALSE)

    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window could not be created")

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glfw.set_window_user_pointer(window, {"closing": False})
    glfw.set_window_close_callback(window, lambda w: _close_callback(w))
    
    # Input callbacks
    glfw.set_key_callback(window, lambda w,k,s,a,m: _key_callback(w,k,s,a,m))
    glfw.set_mouse_button_callback(window, lambda w,b,a,m: _mouse_callback(w,b,a,m))

    return window

def _close_callback(window):
    data = glfw.get_window_user_pointer(window)
    data["closing"] = True
    glfw.set_window_user_pointer(window, data)

def win_clear(r, g, b, a):
    glClearColor(r/255, g/255, b/255, a)
    glClear(GL_COLOR_BUFFER_BIT)

def win_get_events():
    glfw.poll_events()
    # Update key states: PRESS -> HOLD
    for key, state in _key_states.items():
        if state == wkey.PRESS:
            _key_states[key] = wkey.HOLD
    # Update mouse states: PRESS -> HOLD
    for button, state in _mouse_states.items():
        if state == wmouse.PRESS:
            _mouse_states[button] = wmouse.HOLD

def win_render(window):
    glfw.swap_buffers(window)

def win_finish():
    glfw.terminate()

# -----------------------
# Input handling
# -----------------------
def _key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        _key_states[key] = wkey.PRESS
    elif action == glfw.REPEAT:
        _key_states[key] = wkey.HOLD
    elif action == glfw.RELEASE:
        _key_states[key] = wkey.RELEASE

def win_key_state(key):
    return _key_states.get(key, wkey.RELEASE)

def _mouse_callback(window, button, action, mods):
    if action == glfw.PRESS:
        _mouse_states[button] = wmouse.PRESS
    elif action == glfw.REPEAT:
        _mouse_states[button] = wmouse.HOLD
    elif action == glfw.RELEASE:
        _mouse_states[button] = wmouse.RELEASE

def win_mouse_state(button):
    return _mouse_states.get(button, wmouse.RELEASE)

def win_get_mouse_pos(window):
    return glfw.get_cursor_pos(window)

# -----------------------
# Rendering shapes
# -----------------------
def win_rtriangle(x, y, r, g, b, a, size=50, deg=0, window_width=800, window_height=600):
    glColor4f(r/255, g/255, b/255, a)
    glBegin(GL_TRIANGLES)

    cx = (x / window_width) * 2 - 1
    cy = (y / window_height) * 2 - 1
    s_x = (size / window_width) * 2
    s_y = (size / window_height) * 2

    vertices = [(0, s_y), (-s_x, -s_y), (s_x, -s_y)]
    rad = math.radians(deg)

    for vx, vy in vertices:
        rx = vx * math.cos(rad) - vy * math.sin(rad) + cx
        ry = vx * math.sin(rad) + vy * math.cos(rad) + cy
        glVertex2f(rx, ry)

    glEnd()

def win_rsquare(x, y, r, g, b, a, size=50, deg=0, window_width=800, window_height=600):
    glColor4f(r/255, g/255, b/255, a)
    glBegin(GL_QUADS)

    cx = (x / window_width) * 2 - 1
    cy = (y / window_height) * 2 - 1
    s_x = (size / window_width) * 2
    s_y = (size / window_height) * 2

    vertices = [(-s_x, s_y), (s_x, s_y), (s_x, -s_y), (-s_x, -s_y)]
    rad = math.radians(deg)

    for vx, vy in vertices:
        rx = vx * math.cos(rad) - vy * math.sin(rad) + cx
        ry = vx * math.sin(rad) + vy * math.cos(rad) + cy
        glVertex2f(rx, ry)

    glEnd()

def win_rrectangle(x, y, r, g, b, a, sizex=100, sizey=50, deg=0, window_width=800, window_height=600):
    glColor4f(r/255, g/255, b/255, a)
    glBegin(GL_QUADS)

    cx = (x / window_width) * 2 - 1
    cy = (y / window_height) * 2 - 1
    s_x = (sizex / window_width) * 2
    s_y = (sizey / window_height) * 2

    vertices = [(-s_x, s_y), (s_x, s_y), (s_x, -s_y), (-s_x, -s_y)]
    rad = math.radians(deg)

    for vx, vy in vertices:
        rx = vx * math.cos(rad) - vy * math.sin(rad) + cx
        ry = vx * math.sin(rad) + vy * math.cos(rad) + cy
        glVertex2f(rx, ry)

    glEnd()
