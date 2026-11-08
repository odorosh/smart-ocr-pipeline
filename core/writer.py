import pandas as pd
from openpyxl.utils import get_column_letter

class ExcelWriter:
    @staticmethod
    def save_records(records, output_path="raport_fiskalny.xlsx"):
        if not records:
            print("[WARNING] Brak danych do zapisu w Excelu.")
            return False

        df = pd.DataFrame(records)

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Dane_OCR")

            worksheet = writer.sheets["Dane_OCR"]
            for col_idx, col in enumerate(worksheet.columns, start=1):
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = get_column_letter(col_idx)
                worksheet.column_dimensions[col_letter].width = max(max_len + 3, 15)

        print(f"[SUCCESS] Dane pomyślnie zapisane do Excela: {output_path}")
        return True

    @staticmethod
    def save_raw_text(text_lines, output_txt_path):
        """Zapisuje surowe linie tekstu z OCR do osobnego pliku tekstowego."""
        try:
            with open(output_txt_path, "w", encoding="utf-8") as f:
                for line in text_lines:
                    f.write(line + "\n")
            print(f"[DEBUG TXT] Zapisano surowy tekst do: {output_txt_path}")
            return True
        except Exception as e:
            print(f"[ERROR TXT] Nie udało się zapisać pliku {output_txt_path}: {e}")
            return False
