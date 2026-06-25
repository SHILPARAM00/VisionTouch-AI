from utils.distance import calculate_distance


class GestureController:

    def __init__(self):

        self.current_gesture = "NO_HAND"
        self.last_gesture = ""
        self.counter = 0
        self.required = 4


    def detect_gesture(self, landmarks):

        if not landmarks:
            return "NO_HAND"


        hand = landmarks[0]

        thumb = hand[4]
        index = hand[8]


        pinch = calculate_distance(
            (thumb["x"], thumb["y"]),
            (index["x"], index["y"])
        )


        if pinch < 40:

            gesture = "PINCH"


        else:

            fingers = []


            # thumb
            if thumb["x"] < hand[3]["x"]:
                fingers.append(1)
            else:
                fingers.append(0)



            # fingers
            for tip in [8,12,16,20]:

                if hand[tip]["y"] < hand[tip-2]["y"]:
                    fingers.append(1)
                else:
                    fingers.append(0)



            count = sum(fingers)



            if count == 0:
                gesture = "ERASER"


            elif count == 1:
                gesture = "PEN"


            elif count == 2:
                gesture = "WRITE"


            elif count == 3:
                gesture = "CHANGE_MODE"


            elif count == 5:
                gesture = "OPEN_HAND"


            else:
                gesture="UNKNOWN"



        if gesture == self.last_gesture:
            self.counter += 1
        else:
            self.counter = 0


        self.last_gesture = gesture



        if self.counter >= self.required:

            self.current_gesture = gesture



        return self.current_gesture