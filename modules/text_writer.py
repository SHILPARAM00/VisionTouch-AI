import cv2
import numpy as np

from utils.smoothing import Smoother



class TextWriter:


    def __init__(self):

        self.canvas = None

        self.smoother = Smoother()

        self.last_position = None

        self.color = (255,255,255)

        self.size = 3





    def create_canvas(self, frame):

        if self.canvas is None:

            self.canvas = np.zeros_like(frame)







    def write(
        self,
        frame,
        landmarks,
        active
    ):


        self.create_canvas(frame)




        # not writing

        if not active:


            self.last_position = None

            self.smoother.reset()


            return cv2.add(
                frame,
                self.canvas
            )







        if landmarks:


            point = landmarks[0][8]


            x = point["x"]

            y = point["y"]





            x,y = self.smoother.smooth(
                x,
                y
            )





            # first point fix

            if self.last_position is None:


                self.last_position = (
                    x,
                    y
                )


                # sync smoother

                self.smoother.prev_x = x
                self.smoother.prev_y = y



                return cv2.add(
                    frame,
                    self.canvas
                )







            cv2.line(

                self.canvas,

                self.last_position,

                (x,y),

                self.color,

                self.size

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








    def clear(self):


        if self.canvas is not None:


            self.canvas[:] = 0



        self.last_position = None

        self.smoother.reset()