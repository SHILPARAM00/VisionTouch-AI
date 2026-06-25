import cv2
import mediapipe as mp



class HandTracker:


    def __init__(self):


        self.base_options = mp.tasks.BaseOptions(
            model_asset_path="hand_landmarker.task"
        )



        self.options = mp.tasks.vision.HandLandmarkerOptions(

            base_options=self.base_options,

            running_mode=mp.tasks.vision.RunningMode.VIDEO,

            num_hands=1,

            min_hand_detection_confidence=0.7,

            min_hand_presence_confidence=0.7,

            min_tracking_confidence=0.7

        )



        self.detector = (
            mp.tasks.vision.HandLandmarker
            .create_from_options(
                self.options
            )
        )



        self.timestamp = 0


        self.hand_present = False







    # ==========================
    # HAND DETECTION
    # ==========================

    def find_hands(
            self,
            frame,
            draw=True
    ):


        h,w,_ = frame.shape



        rgb = cv2.cvtColor(

            frame,

            cv2.COLOR_BGR2RGB

        )



        image = mp.Image(

            image_format=mp.ImageFormat.SRGB,

            data=rgb

        )



        self.timestamp += 1



        result = self.detector.detect_for_video(

            image,

            self.timestamp

        )



        landmarks = []

        self.hand_present = False





        if result.hand_landmarks:



            self.hand_present = True



            for hand in result.hand_landmarks:



                points = []



                for i,lm in enumerate(hand):



                    x = int(lm.x*w)

                    y = int(lm.y*h)



                    points.append(

                        {
                            "id": i,
                            "x": x,
                            "y": y,
                            "z": lm.z
                        }

                    )



                landmarks.append(points)



                if draw:

                    self.draw_hand(
                        frame,
                        points
                    )





        return frame, landmarks







    # ==========================
    # DRAW HAND
    # ==========================

    def draw_hand(
            self,
            frame,
            points
    ):



        for p in points:


            cv2.circle(

                frame,

                (
                    p["x"],
                    p["y"]
                ),

                4,

                (0,255,0),

                -1

            )





        lines = [

            (0,1),(1,2),(2,3),(3,4),

            (0,5),(5,6),(6,7),(7,8),

            (5,9),(9,10),(10,11),(11,12),

            (9,13),(13,14),(14,15),(15,16),

            (13,17),(17,18),(18,19),(19,20)

        ]



        for a,b in lines:


            cv2.line(

                frame,

                (
                    points[a]["x"],
                    points[a]["y"]
                ),

                (
                    points[b]["x"],
                    points[b]["y"]
                ),

                (0,255,0),

                2

            )







    # ==========================
    # GET POINT
    # ==========================

    def get_point(
            self,
            landmarks,
            index
    ):


        if not landmarks:

            return None



        point = landmarks[0][index]



        return (

            point["x"],

            point["y"]

        )








    # ==========================
    # RAW LANDMARK
    # ==========================

    def get_raw_point(
            self,
            landmarks,
            index
    ):


        if not landmarks:

            return None



        return landmarks[0][index]









    # ==========================
    # FINGER POSITIONS
    # ==========================

    def get_finger_positions(
            self,
            landmarks
    ):



        if not landmarks:

            return None




        hand = landmarks[0]



        return {


            "thumb":

            (
                hand[4]["x"],
                hand[4]["y"]
            ),



            "index":

            (
                hand[8]["x"],
                hand[8]["y"]
            ),



            "middle":

            (
                hand[12]["x"],
                hand[12]["y"]
            ),



            "ring":

            (
                hand[16]["x"],
                hand[16]["y"]
            ),



            "pinky":

            (
                hand[20]["x"],
                hand[20]["y"]
            )

        }









    # ==========================
    # HAND CENTER
    # ==========================

    def get_hand_center(
            self,
            landmarks
    ):



        if not landmarks:

            return None



        x = 0

        y = 0



        for p in landmarks[0]:

            x += p["x"]

            y += p["y"]



        total = len(
            landmarks[0]
        )



        return (

            x//total,

            y//total

        )







    # ==========================
    # STATUS
    # ==========================

    def is_hand_detected(self):

        return self.hand_present