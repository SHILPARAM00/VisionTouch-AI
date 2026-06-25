import math



class Smoother:



    def __init__(self):


        self.prev_x = None
        self.prev_y = None


        # faster + smoother response
        self.smoothing = 0.45





    # =========================
    # SMOOTH HAND MOVEMENT
    # =========================


    def smooth(self, x, y):


        # first detection

        if self.prev_x is None:


            self.prev_x = x
            self.prev_y = y


            return x, y





        new_x = int(

            self.prev_x * self.smoothing

            +

            x * (1 - self.smoothing)

        )



        new_y = int(

            self.prev_y * self.smoothing

            +

            y * (1 - self.smoothing)

        )





        self.prev_x = new_x
        self.prev_y = new_y



        return new_x, new_y







    # =========================
    # RESET
    # =========================


    def reset(self):


        self.prev_x = None
        self.prev_y = None








    # =========================
    # MOVEMENT CHECK
    # =========================


    def movement_amount(self, x, y):


        if self.prev_x is None:

            return 0




        distance = math.sqrt(

            (x - self.prev_x) ** 2

            +

            (y - self.prev_y) ** 2

        )



        return distance