import time


class SystemController:


    def __init__(self,drawing,screen):

        self.drawing=drawing
        self.screen=screen

        self.last=0



    def handle(self,gesture,frame):


        now=time.time()


        if now-self.last < 1:
            return



        if gesture=="ERASER":

            self.drawing.toggle_eraser()

            self.last=now



        elif gesture=="OPEN_HAND":

            pass



        return