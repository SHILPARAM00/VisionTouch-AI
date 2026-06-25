import pyttsx3
import threading
import queue
import time



class VoiceAssistant:



    def __init__(self):


        self.messages = queue.Queue()



        self.running = True



        self.last_text = ""

        self.last_time = 0


        self.cooldown = 2.0



        self.lock = threading.Lock()



        self.engine = pyttsx3.init()



        self.thread = threading.Thread(

            target=self.worker,

            daemon=True

        )


        self.thread.start()





    # -------------------------
    # VOICE THREAD
    # -------------------------

    def worker(self):



        while self.running:


            try:


                text = self.messages.get(
                    timeout=0.2
                )


            except queue.Empty:


                continue




            if text is None:

                break





            with self.lock:


                try:


                    self.engine.say(text)

                    self.engine.runAndWait()



                except Exception as e:


                    print(
                        "Voice error:",
                        e
                    )







    # -------------------------
    # SEND VOICE
    # -------------------------

    def speak(self,text):



        now = time.time()



        if (

            text == self.last_text

            and

            now - self.last_time < self.cooldown

        ):

            return




        self.last_text = text

        self.last_time = now





        # clear old messages

        while not self.messages.empty():

            try:

                self.messages.get_nowait()


            except:

                break






        self.messages.put(text)







    # -------------------------
    # CLOSE
    # -------------------------

    def stop(self):


        self.running=False


        self.messages.put(None)