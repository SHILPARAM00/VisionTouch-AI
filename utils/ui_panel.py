import cv2
import time



class UIPanel:


    def __init__(self):

        self.title = "VisionTouch AI"

        self.buttons=[]

        self.start=time.time()





    def draw_panel(
            self,
            frame,
            mode,
            gesture,
            fps,
            brush,
            color
    ):


        h,w,_ = frame.shape



        # top glass panel

        overlay = frame.copy()


        cv2.rectangle(
            overlay,
            (15,15),
            (330,190),
            (0,0,0),
            -1
        )


        frame = cv2.addWeighted(
            overlay,
            0.45,
            frame,
            0.55,
            0
        )





        # title

        cv2.putText(

            frame,

            self.title,

            (30,45),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0,255,255),

            2

        )






        info=[

            "Mode : "+mode,

            "Gesture : "+gesture,

            "FPS : "+str(fps),

            "Brush : "+str(brush)

        ]



        y=80


        for text in info:


            cv2.putText(

                frame,

                text,

                (30,y),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.55,

                (255,255,255),

                2

            )


            y+=25






        self.draw_buttons(frame)


        return frame






    def draw_buttons(self,frame):


        self.buttons=[]



        data=[

            ("UNDO",20),

            ("REDO",120),

            ("CLEAR",220)

        ]



        for name,x in data:


            cv2.rectangle(

                frame,

                (x,210),

                (x+80,250),

                (30,30,30),

                -1

            )


            cv2.putText(

                frame,

                name,

                (x+8,236),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.45,

                (255,255,255),

                1

            )


            self.buttons.append(

                (
                    name,
                    x,
                    x+80,
                    210,
                    250
                )

            )







    def check_button(self,x,y):


        for name,x1,x2,y1,y2 in self.buttons:


            if x1<x<x2 and y1<y<y2:


                return name



        return None