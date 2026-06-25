import cv2
import numpy as np
import os
from datetime import datetime

from utils.smoothing import Smoother



class DrawingMode:


    def __init__(self):

        self.canvas = None

        self.smoother = Smoother()


        self.color = (0,0,255)


        self.brush_size = 8
        self.eraser_size = 40


        self.last_position = None


        self.eraser = False


        self.undo_stack = []
        self.redo_stack = []

        self.history = 40





    def create_canvas(self, frame):

        if self.canvas is None:

            self.canvas = np.zeros_like(frame)






    def save_state(self):

        if self.canvas is not None:


            self.undo_stack.append(
                self.canvas.copy()
            )


            if len(self.undo_stack) > self.history:

                self.undo_stack.pop(0)



            self.redo_stack.clear()







    def draw(self, frame, landmarks, gesture):


        self.create_canvas(frame)





        # stop drawing

        if gesture == "OPEN_HAND":


            self.last_position = None

            self.smoother.reset()


            return cv2.add(
                frame,
                self.canvas
            )







        # eraser

        if gesture == "ERASER":


            self.eraser = True



        elif gesture in [

            "PEN",
            "PINCH",
            "WRITE"

        ]:


            self.eraser = False







        if landmarks and gesture in [

            "PEN",
            "PINCH",
            "WRITE",
            "ERASER"

        ]:



            point = landmarks[0][8]


            x = point["x"]
            y = point["y"]




            x,y = self.smoother.smooth(
                x,
                y
            )







            # first writing point fix

            if self.last_position is None:


                self.last_position = (
                    x,
                    y
                )


                self.smoother.prev_x = x
                self.smoother.prev_y = y



                return cv2.add(
                    frame,
                    self.canvas
                )







            # erase

            if self.eraser:


                cv2.circle(

                    self.canvas,

                    (x,y),

                    self.eraser_size,

                    (0,0,0),

                    -1

                )






            # draw

            else:


                cv2.line(

                    self.canvas,

                    self.last_position,

                    (x,y),

                    self.color,

                    self.brush_size

                )





            self.last_position = (
                x,
                y
            )







        else:


            self.last_position = None

            self.smoother.reset()






        return cv2.add(
            frame,
            self.canvas
        )










    # =====================
    # ERASER
    # =====================


    def toggle_eraser(self):

        self.eraser = not self.eraser







    # =====================
    # UNDO
    # =====================


    def undo(self):


        if self.undo_stack:


            self.redo_stack.append(
                self.canvas.copy()
            )


            self.canvas = self.undo_stack.pop()







    # =====================
    # REDO
    # =====================


    def redo(self):


        if self.redo_stack:


            self.undo_stack.append(
                self.canvas.copy()
            )


            self.canvas = self.redo_stack.pop()








    # =====================
    # CLEAR
    # =====================


    def clear(self):


        if self.canvas is not None:


            self.save_state()


            self.canvas[:] = 0



        self.last_position = None

        self.smoother.reset()










    # =====================
    # BRUSH SIZE
    # =====================


    def increase_size(self):


        sizes = [

            3,
            5,
            8,
            12,
            18,
            25,
            35,
            45

        ]



        for size in sizes:


            if size > self.brush_size:


                self.brush_size = size

                break







    def decrease_size(self):


        sizes = [

            3,
            5,
            8,
            12,
            18,
            25,
            35,
            45

        ]



        for size in reversed(sizes):


            if size < self.brush_size:


                self.brush_size = size

                break










    # =====================
    # SAVE
    # =====================


    def save(self):


        if self.canvas is None:

            return




        os.makedirs(

            "outputs/drawings",

            exist_ok=True

        )




        path = (

            "outputs/drawings/"

            +

            datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            +

            ".png"

        )




        cv2.imwrite(

            path,

            self.canvas

        )



        print(
            "Saved:",
            path
        )









    # =====================
    # AI TEXT
    # =====================


    def get_ai_text(self):

        return ""