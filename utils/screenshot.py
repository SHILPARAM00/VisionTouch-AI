import cv2
import os
from datetime import datetime



class Screenshot:


    def __init__(self):

        os.makedirs(
            "outputs/screenshots",
            exist_ok=True
        )



    def save(self, frame):


        filename = (
            "outputs/screenshots/"
            +
            datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
            +
            ".png"
        )


        cv2.imwrite(
            filename,
            frame
        )


        print(
            "Screenshot saved:",
            filename
        )