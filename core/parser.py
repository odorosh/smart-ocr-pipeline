import re
from datetime import datetime

class DataParser:
    @staticmethod
    def parse_polish_receipt(text_lines):
        extracted = {
            "Data_Wydruku": "N/A",
            "Numer_Paragonu": "N/A",
            "Suma_PLN": "N/A"
        }

        full_text = "\n".join(text_lines)

        # 1. Szukanie daty
        date_patterns = [
            r'\b\d{4}-\d{2}-\d{2}\b',
            r'\b\d{2}\.\d{2}\.\d{4}\b'
        ]
        for pattern in date_patterns:
            date_match = re.search(pattern, full_text)
            if date_match:
                extracted["Data_Wydruku"] = date_match.group(0)
                break

        # 2. Szukanie numeru paragonu
        for line in text_lines:
            nr_match = re.search(r'(?:NR|Nr|No|ID)[:\s]*([0-9]{4,9})\b|\b([0-9]{5,9})\b', line)
            if nr_match:
                val = nr_match.group(1) or nr_match.group(2)
                if val and not val.startswith("2024") and "nip" not in line.lower():
                    extracted["Numer_Paragonu"] = val
                    break

        # 3. Szukanie kwoty w linii zawierającej SUMA lub RAZEM
        for line in text_lines:
            line_lower = line.lower()
            if "ptu" in line_lower:
                continue  # ignorujemy podatki

            if "suma" in line_lower or "razem" in line_lower or "pln" in line_lower:
                match = re.search(r'\d+[\s\.,]\d{2}', line)
                if match:
                    extracted["Suma_PLN"] = match.group(0).strip()
                    # Jeśli znaleźliśmy wartość przy słowie kluczowym, przerywamy pętlę
                    if "suma" in line_lower:
                        break

        return extracted
