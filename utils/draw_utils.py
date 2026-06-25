import cv2
import numpy as np



def draw_point(
        canvas,
        x,
        y,
        color,
        size
):


    if canvas is None:
        return



    # smooth brush circle

    cv2.circle(

        canvas,

        (int(x), int(y)),

        size,

        color,

        -1,

        cv2.LINE_AA

    )





def draw_line(
        canvas,
        start,
        end,
        color,
        size
):


    if canvas is None:
        return



    cv2.line(

        canvas,

        start,

        end,

        color,

        size,

        cv2.LINE_AA

    )





def erase_point(
        canvas,
        x,
        y,
        size=40
):


    if canvas is None:
        return



    cv2.circle(

        canvas,

        (int(x),int(y)),

        size,

        (0,0,0),

        -1,

        cv2.LINE_AA

    )





def create_blank_canvas(frame):


    return np.zeros_like(frame)