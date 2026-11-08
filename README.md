# Smart OCR Pipeline: Automated Polish Receipt (Paragon Fiskalny) Data Extraction

A highly optimized, modular Python computer vision and data engineering pipeline designed to automate financial data entry from physical documents. The system processes scanned and smartphone-photographed retail receipts, applies advanced image enhancement to handle mixed-lighting scenarios, and performs robust Optical Character Recognition (OCR) tailored to non-uniform layouts and custom font sizes.

## 🚀 Key Architectural Breakthroughs
- **Custom Page Segmentation Mode (PSM 6):** Standard OCR engines often mistake large, bold total summary lines (`SUMA PLN`) for graphical logos or banner headers, causing complete data omission. This project resolves that by enforcing a strict unified block text segmentation mode (`--psm 6`), ensuring large font variations are accurately captured.
- **Adaptive Contrast Enhancement (OpenCV CLAHE):** Implements Contrast Limited Adaptive Histogram Equalization rather than destructive global binarization, preserving crisp text edges across both light scans and shadowed smartphone photographs.
- **Strict Multi-Tiered Polish Business Logic Parsing:** The extraction algorithm is built specifically around European/Polish accounting layouts, accurately separating transactional index IDs, chronological print dates, and net final cash totals while filtering out systemic metadata, timestamps, and regional tax brackets (SUMA PTU/VAT).

## 🛠 Tech Stack
- **OS Environment:** Native integration on **Fedora Linux** using core system packages.
- **Core Engine:** Python 3, Tesseract OCR (`pol` language module).
- **Libraries:** OpenCV (`cv2`), `pytesseract`, `pandas`, `openpyxl`.

## 📂 Project Structure
```text
smart-ocr-pipeline/
├── core/
│   ├── __init__.py
│   ├── ocr.py          # Handles CLAHE enhancement and forced PSM 6 block analysis
│   ├── parser.py       # Implements targeted regex and context-based line logic
│   └── writer.py       # Generates Excel frames and saves raw diagnostic text files
├── input_images/       # Directory for input scans/photos (.jpg, .png)
├── main.py             # Pipeline execution orchestrator
└── README.md           # Professional documentation
```

## 📈 Real-World Validation Benchmarks
The pipeline was validated using real-world retail receipts under two distinct conditions:

| Metadata Target | Photo Receipt (`paragon_photo.jpg`) | Scanned Receipt (`paragon_scanned.jpg`) | Status |
| :--- | :--- | :--- | :--- |
| **Data Wydruku (Date)** | `2019-03-12` | `2024-08-02` | **100% Accurate** |
| **Numer Paragonu (ID)** | `166031` | `000013346` | **100% Accurate** |
| **Suma PLN (Total)** | `26,30` | `88,20` | **100% Accurate** |

*Note: The system successfully managed to isolate the actual `88,20 PLN` total on the scanned receipt, completely bypassing adjacent lines containing system phone lines and fractional tax totals (`SUMA PTU 11,56`).*
