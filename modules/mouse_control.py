import pyautogui
import time



class MouseController:



    def __init__(self):


        self.screen_w, self.screen_h = pyautogui.size()



        pyautogui.FAILSAFE = False



        self.prev_x = None
        self.prev_y = None



        self.smooth = 0.7



        self.last_click = 0

        self.click_delay = 0.8






    # -------------------------
    # MOVE CURSOR
    # -------------------------

    def move(self, landmarks, frame_shape=None):


        if not landmarks:

            return




        point = landmarks[0][8]



        x = point[1]

        y = point[2]




        if frame_shape:


            h,w,_ = frame_shape


        else:


            w,h = 640,480






        target_x = int(

            x / w * self.screen_w

        )


        target_y = int(

            y / h * self.screen_h

        )






        # smoothing

        if self.prev_x is None:


            self.prev_x = target_x

            self.prev_y = target_y





        smooth_x = int(

            self.prev_x*self.smooth

            +

            target_x*(1-self.smooth)

        )



        smooth_y = int(

            self.prev_y*self.smooth

            +

            target_y*(1-self.smooth)

        )





        pyautogui.moveTo(

            smooth_x,

            smooth_y,

            duration=0.01

        )



        self.prev_x = smooth_x

        self.prev_y = smooth_y







    # -------------------------
    # CLICK
    # -------------------------

    def click(self):


        now = time.time()



        if now - self.last_click > self.click_delay:


            pyautogui.click()


            self.last_click = now







    # -------------------------
    # DOUBLE CLICK
    # -------------------------

    def double_click(self):


        pyautogui.doubleClick()