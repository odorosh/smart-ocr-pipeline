import os
from core.ocr import OCREngine
from core.parser import DataParser
from core.writer import ExcelWriter

def main():
    input_dir = "input_images"
    output_file = "raport_fiskalny.xlsx"

    ocr = OCREngine()
    dataset = []

    supported_formats = (".png", ".jpg", ".jpeg", ".tiff")
    if not os.path.exists(input_dir) or not os.listdir(input_dir):
        print(f"[INFO] Proszę utworzyć folder '{input_dir}' i umieścić tam zdjęcia paragonów.")
        return

    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_formats)]
    print(f"[START] Znaleziono {len(image_files)} zdjęć do przetworzenia.")

    for img_file in image_files:
        full_path = os.path.join(input_dir, img_file)

        # 1. Krok OCR
        lines = ocr.get_text_lines(full_path)

        # --- NOWOŚĆ: Zapis surowego wyniku OCR do pliku .txt ---
        # Tworzymy nazwę pliku tekstowego na podstawie nazwy obrazka (np. paragon_photo.txt)
        txt_filename = os.path.splitext(img_file)[0] + ".txt"
        ExcelWriter.save_raw_text(lines, txt_filename)
        # ------------------------------------------------------

        # 2. Krok Parsowania
        parsed_data = DataParser.parse_polish_receipt(lines)
        parsed_data["Nazwa_Pliku"] = img_file

        dataset.append(parsed_data)

    # 3. Zapis zbiorczego raportu do Excel
    ExcelWriter.save_records(dataset, output_file)

if __name__ == "__main__":
    main()
