import cv2
import pytesseract


class OCRReader:


    def __init__(self):

        # update this path if needed
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        self.last_text = ""



    def extract_text(self, canvas):


        if canvas is None:

            return ""



        # convert to grayscale

        gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)



        # threshold for better OCR

        _, thresh = cv2.threshold(
            gray,
            120,
            255,
            cv2.THRESH_BINARY_INV
        )



        # OCR

        text = pytesseract.image_to_string(
            thresh,
            config="--psm 7"
        )



        text = text.strip()



        if text:

            self.last_text = text



        return self.last_text