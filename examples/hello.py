from zrender import *

def main():
    window = win_make(800, 600, "Hello, World!", False)

    while not win_closing(window):
        win_get_events()
        win_clear(0, 0, 0, 1)
        
        #         x    y     text            r    g    b    a  font size  window: width height
        win_rtext(300, 320, "Hello, World!", 255, 255, 255, 1, 32,                800,  600)

        win_render(window)
    win_finish()

if __name__ == "__main__":
    main()