import cv2


class ColorSelector:


    def __init__(self):


        self.colors = {

            "RED": (0,0,255),
            "GREEN": (0,255,0),
            "BLUE": (255,0,0),
            "YELLOW": (0,255,255),
            "WHITE": (255,255,255),
            "PURPLE": (255,0,255),
            "ORANGE": (0,165,255),
            "CYAN": (255,255,0),
            "PINK": (180,105,255)

        }


        self.selected_color = (0,0,255)

        self.selected_name = "RED"

        self.boxes = []




    def draw_palette(self, frame):


        h, w, _ = frame.shape


        self.boxes = []


        # bottom palette position

        start_x = 20
        y = h - 80



        # dark transparent bar

        overlay = frame.copy()


        cv2.rectangle(

            overlay,

            (10,y-10),

            (700,y+65),

            (0,0,0),

            -1

        )


        frame[:] = cv2.addWeighted(
            overlay,
            0.4,
            frame,
            0.6,
            0
        )





        x = start_x



        for name,color in self.colors.items():


            cv2.rectangle(

                frame,

                (x,y),

                (x+50,y+50),

                color,

                -1

            )



            # selected border

            if name == self.selected_name:

                cv2.rectangle(

                    frame,

                    (x-3,y-3),

                    (x+53,y+53),

                    (255,255,255),

                    3

                )



            self.boxes.append(

                (
                    name,
                    x,
                    y,
                    x+50,
                    y+50
                )

            )



            x += 70





        cv2.putText(

            frame,

            "COLOR: "+self.selected_name,

            (start_x,y-20),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (255,255,255),

            2

        )





    def select_color(self, landmarks):


        if not landmarks:

            return




        finger = landmarks[0][8]


        x = finger["x"]

        y = finger["y"]





        for name,x1,y1,x2,y2 in self.boxes:


            if x1 <= x <= x2 and y1 <= y <= y2:



                self.selected_name = name


                self.selected_color = self.colors[name]


                return name



        return None