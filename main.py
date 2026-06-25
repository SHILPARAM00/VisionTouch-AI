import cv2
import time


from modules.hand_tracking import HandTracker
from modules.gesture_control import GestureController
from modules.drawing_mode import DrawingMode
from modules.zoom_control import ZoomController
from modules.mouse_control import MouseController
from modules.mode_manager import ModeManager
from modules.system_control import SystemController


from utils.color_selector import ColorSelector
from utils.voice_feedback import VoiceAssistant
from utils.screenshot import Screenshot
from utils.ui_panel import UIPanel
from utils.cooldown import Cooldown





# =====================
# CAMERA
# =====================

cap = cv2.VideoCapture(0)

cap.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    1280
)

cap.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    720
)



cv2.namedWindow(
    "VisionTouch AI",
    cv2.WINDOW_NORMAL
)






# =====================
# OBJECTS
# =====================


tracker = HandTracker()

gesture = GestureController()


drawing = DrawingMode()


zoom = ZoomController()


mouse = MouseController()



mode_manager = ModeManager()



voice = VoiceAssistant()


screen = Screenshot()


ui = UIPanel()



colors = ColorSelector()



cooldown = Cooldown(1.0)



system = SystemController(
    drawing,
    screen
)





prev_time = 0







while True:



    ok, frame = cap.read()


    if not ok:

        break





    # mirror camera

    frame = cv2.flip(
        frame,
        1
    )







    # =====================
    # FPS
    # =====================


    now = time.time()


    fps = int(
        1 /
        (now - prev_time + 0.0001)
    )


    prev_time = now








    # =====================
    # HAND TRACKING
    # =====================


    frame, landmarks = tracker.find_hands(
        frame,
        True
    )








    # =====================
    # GESTURE
    # =====================


    action = gesture.detect_gesture(
        landmarks
    )








    # =====================
    # MODE
    # =====================


    mode = mode_manager.change_mode(
        action
    )









    # =====================
    # SYSTEM CONTROL
    # disabled in mouse mode
    # =====================


    if mode != "MOUSE":


        if cooldown.allow(action):

            system.handle(
                action,
                frame
            )









    # =====================
    # DRAW MODE
    # =====================


    if mode == "DRAW":


        frame = drawing.draw(
            frame,
            landmarks,
            action
        )









    # =====================
    # TEXT MODE
    # =====================


    elif mode == "TEXT":


        frame = drawing.draw(
            frame,
            landmarks,
            action
        )









    # =====================
    # ZOOM MODE
    # =====================


    elif mode == "ZOOM":


        if action == "WRITE":


            frame = zoom.zoom(
                frame,
                landmarks
            )











    # =====================
    # MOUSE MODE
    # =====================


    elif mode == "MOUSE":



        if action == "OPEN_HAND":


            mouse.move(
                landmarks,
                frame.shape
            )



        elif action == "PINCH":


            mouse.click()










    # =====================
    # COLOR PALETTE
    # =====================


    colors.draw_palette(
        frame
    )


    colors.select_color(
        landmarks
    )


    drawing.color = (
        colors.selected_color
    )









    # =====================
    # DASHBOARD UI
    # =====================


    frame = ui.draw_panel(

        frame,

        mode,

        action,

        fps,

        drawing.brush_size,

        drawing.color

    )









    # =====================
    # TOUCH BUTTONS
    # =====================


    if landmarks:


        point = landmarks[0][8]


        button = ui.check_button(

            point["x"],

            point["y"]

        )



        if button == "UNDO":


            drawing.undo()



        elif button == "REDO":


            drawing.redo()



        elif button == "CLEAR":


            drawing.clear()










    # =====================
    # DISPLAY
    # =====================


    cv2.imshow(
        "VisionTouch AI",
        frame
    )









    # =====================
    # KEYBOARD
    # =====================


    key = cv2.waitKey(10)



    # CTRL + C

    if key == 3:

        drawing.clear()

        print(
            "Canvas Cleared"
        )




    key = key & 0xff





    if key == ord('c'):


        drawing.clear()

        print(
            "Canvas Cleared"
        )





    elif key == ord('u'):


        drawing.undo()

        print(
            "Undo"
        )






    elif key == ord('r'):


        drawing.redo()

        print(
            "Redo"
        )






    elif key == ord('+'):


        drawing.increase_size()






    elif key == ord('-'):


        drawing.decrease_size()







    elif key == ord('s'):


        drawing.save()

        print(
            "Saved"
        )






    elif key == ord('q'):


        break










cap.release()

cv2.destroyAllWindows()