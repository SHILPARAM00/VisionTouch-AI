import time


class ModeManager:


    def __init__(self):

        self.modes = [
            "DRAW",
            "TEXT",
            "ZOOM",
            "MOUSE"
        ]


        self.index = 0

        self.mode = self.modes[0]


        self.last_change = 0

        self.delay = 1.5


        self.lock = False





    def change_mode(self, gesture):


        now = time.time()



        if gesture == "CHANGE_MODE":



            if not self.lock:



                if now - self.last_change > self.delay:



                    self.index += 1



                    if self.index >= len(self.modes):

                        self.index = 0



                    self.mode = self.modes[
                        self.index
                    ]



                    self.last_change = now


                    self.lock = True







        else:


            # unlock when gesture removed

            self.lock = False






        return self.mode






    def get_mode(self):

        return self.mode