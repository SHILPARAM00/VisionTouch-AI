import time



class Cooldown:


    def __init__(self, delay=1.0):

        self.delay = delay
        self.last_time = {}



    def allow(self, key):

        current = time.time()



        if key not in self.last_time:

            self.last_time[key] = current

            return True



        if current - self.last_time[key] > self.delay:

            self.last_time[key] = current

            return True



        return False