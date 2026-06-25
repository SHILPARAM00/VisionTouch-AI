import cv2

from utils.distance import calculate_distance




class ZoomController:



    def __init__(self):


        self.zoom_factor = 1.0


        self.previous_distance = None


        self.min_zoom = 1.0

        self.max_zoom = 2.5



        self.sensitivity = 0.08






    # -------------------------
    # ZOOM ENGINE
    # -------------------------

    def zoom(self, frame, landmarks):


        if not landmarks:

            self.reset()

            return frame




        points = landmarks[0]



        index = points[8]

        middle = points[12]





        distance = calculate_distance(

            (
                index["x"],
                index["y"]
            ),

            (
                middle["x"],
                middle["y"]
            )

        )





        if self.previous_distance is None:


            self.previous_distance = distance


            return frame






        change = (

            distance -

            self.previous_distance

        )





        # zoom in

        if change > 4:


            self.zoom_factor += self.sensitivity




        # zoom out

        elif change < -4:


            self.zoom_factor -= self.sensitivity





        self.zoom_factor = max(

            self.min_zoom,

            min(
                self.zoom_factor,
                self.max_zoom
            )

        )



        self.previous_distance = distance






        return self.apply_zoom(frame)







    # -------------------------
    # APPLY CAMERA ZOOM
    # -------------------------

    def apply_zoom(self, frame):


        h,w,_ = frame.shape



        if self.zoom_factor <= 1:


            return frame





        new_w = int(
            w / self.zoom_factor
        )

        new_h = int(
            h / self.zoom_factor
        )



        x1 = (w-new_w)//2

        y1 = (h-new_h)//2



        crop = frame[

            y1:y1+new_h,

            x1:x1+new_w

        ]



        frame = cv2.resize(

            crop,

            (w,h),

            interpolation=cv2.INTER_LINEAR

        )





        cv2.putText(

            frame,

            f"ZOOM {self.zoom_factor:.1f}x",

            (30,220),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (0,255,0),

            2

        )



        return frame






    # -------------------------
    # RESET
    # -------------------------

    def reset(self):


        self.previous_distance = None