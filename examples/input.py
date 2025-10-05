from zrender import *

def main():
    sx = 400
    sy = 300

    window = win_make(800, 600, "I have input now!!! ", False)

    while not win_closing(window):
        win_get_events()

        mouse_x, mouse_y = win_get_mouse_pos(window)
        mouse_y = 600 - mouse_y # Now mouse y will be handled correctly (we need to flip y by subtracting mouse_y by window height)

        # Moving a square
        if win_key_state(glfw.KEY_D) in (wkey.PRESS, wkey.HOLD):
            sx += 10
        if win_key_state(glfw.KEY_A) in (wkey.PRESS, wkey.HOLD):
            sx -= 10
        if win_key_state(glfw.KEY_W) in (wkey.PRESS, wkey.HOLD):
            sy += 10
        if win_key_state(glfw.KEY_S) in (wkey.PRESS, wkey.HOLD):
            sy -= 10
        
        sx = max(80, min(sx, 720))
        sy = max(80, min(sy, 520))

        # If square is on the right side of the screen make it red otherways make it black (window)
        if sx > 400:
            win_clear(255, 0, 0, 1)
        else:
            win_clear(0, 0, 0, 1)
        # If left mouse button is clicked and mouse is touching 160x160 (size=80) square turn it green otherways make it blue (square)
        if win_mouse_state(glfw.MOUSE_BUTTON_LEFT) in (wmouse.PRESS, wmouse.HOLD) \
        and mouse_x <= sx+80 and mouse_x >= sx-80 and \
        mouse_y >= sy-80 and mouse_y <= sy+80:
            win_rsquare(sx, sy, 0, 255, 0, 1, 80, 0, 800, 600)
        else:
            win_rsquare(sx, sy, 0, 0, 255, 1, 80, 0, 800, 600)
        win_render(window)

    win_finish()

if __name__ == "__main__":
    main()
