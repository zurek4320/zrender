from zrender import *

def main():
    tx = 1
    td = 1

    #                 width height title                      resizeable?
    window = win_make(800,  600,   "beutiful zrender window", True)

    # Main loop
    while not win_closing(window):
        # Get events
        win_get_events()

        # Clear screen and paint it pink :D
        win_clear(255, 147, 203, 0.8)
        #          x    y    r  g    b  a  size degree

        # zkóer (rendered before traiangle so it is kind of a background now)
        win_rsquare(400, 300, 0, 255, 0, 1, 80, 0, 800, 600)
        # Render a damn traiangle!!!
        #             x   y    r    g  b  a  size degree window: width height
        win_rtriangle(tx, 300, 255, 0, 0, 1, 100, td,            800,  600)


        # Renders the damn window by swapping buffers
        win_render(window)

        # Gently move and rotate the traiangle
        tx += 1
        td += 1

    # Finish this beutiful program
    win_finish()

if __name__ == "__main__":
    main()