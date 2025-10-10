from zrender import *
import time

def main():
    window = win_make(600, 800, "Clever Clicker", False)

    clicks = 0
    clicked = False

    sx = 300
    sy = 400

    price = 15
    buy_clicked = False

    clicks_per_second = 0

    last_time = time.time()
    second_timer = 0

    while not win_closing(window):
        win_get_events()

        # delta handling
        now = time.time()
        delta = now - last_time
        last_time = now
        second_timer += delta

        mouse_x, mouse_y = win_get_mouse_pos(window)
        mouse_y = 800 - mouse_y

        win_clear(0, 0, 0, 1)
                
        win_rtext(21, 750, f"Clicks: {clicks}", 255, 255, 255, 1, 32, 600, 800)
        win_rtext(21, 700, f"Clicks per Second: {clicks_per_second}", 255, 255, 255, 1, 32, 600, 800)
        win_rsquare(sx, sy, 255, 100, 100, 1, 100, 0, 600, 800)
        win_rtext(215, 390, "Click me!", 0, 255, 0, 1, 42, 600, 800)

        # square clicking
        if not clicked:
            if win_mouse_state(glfw.MOUSE_BUTTON_LEFT) in (wmouse.PRESS, wmouse.HOLD) \
            and mouse_x <= sx+100 and mouse_x >= sx-100 and \
            mouse_y >= sy-100 and mouse_y <= sy+100:
                clicked = True
                clicks += 1
        elif win_mouse_state(glfw.MOUSE_BUTTON_LEFT) == wmouse.RELEASE:
            clicked = False
        
        win_rrectangle(300, 100, 150, 150, 150, 1, 300, 100, 0, 600, 800)
        win_rrectangle(300, 153, 255, 255, 255, 1, 250, 20, 0, 600, 800)
        win_rtext(56, 135, f"+1 click per second: {price}", 0, 0, 0, 1, 32, 600, 800)

        # +1 clicks per second button handling
        if not buy_clicked:
            if win_mouse_state(glfw.MOUSE_BUTTON_LEFT) in (wmouse.PRESS, wmouse.HOLD) \
                and mouse_x <= 550 and mouse_x >= 50 and \
                mouse_y >= 134 and mouse_y <= 174:
                    buy_clicked = True
                    if clicks >= price:
                        clicks -= price
                        clicks_per_second += 1
                        price *= 1.2
                        price = int(f"{price:.0f}")
        elif win_mouse_state(glfw.MOUSE_BUTTON_LEFT) == wmouse.RELEASE:
             buy_clicked = False

        win_render(window)
        if second_timer >= 1.0:
            clicks += clicks_per_second
            second_timer -= 1.0
    win_finish()

if __name__ == "__main__":
    main()
