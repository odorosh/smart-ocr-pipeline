import cv2
import pytesseract
import os

class OCREngine:
    def __init__(self):
        self.lang = 'pol'

    def preprocess_image(self, image_path):
        """Minimalna obróbka, aby nie zniszczyć dużych, grubych czcionek."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Nie znaleziono pliku: {image_path}")

        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Zamiast agresywnego thresholdingu, używamy lekkiego wyrównania histogramu (CLAHE)
        # To pozwala zachować czytelność zarówno małych, jak i bardzo dużych liter
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)

        return enhanced

    def get_text_lines(self, image_path):
        """Pobiera tekst przy użyciu wymuszonego trybu segmentacji blokowej (PSM 6)."""
        try:
            prepared_img = self.preprocess_image(image_path)

            # Wymuszamy tryb PSM 6 (Assume a single uniform block of text)
            # Zapobiega to wycinaniu dużych czcionek jako rzekomej grafiki
            custom_config = r'--psm 6'

            raw_text = pytesseract.image_to_string(prepared_img, lang=self.lang, config=custom_config)
            return [line.strip() for line in raw_text.split('\n') if line.strip()]
        except Exception as e:
            print(f"[OCR ERROR] {image_path}: {e}")
            return []
