import pdfplumber

from app.helpers.text_cleaner import clean_text
from app.extractors.key_value_extractor import extract_kv_from_line
from app.extractors.transaction_extractor import extract_transactions


def process_pdf(pdf_path):

    outside_data = {}

    with pdfplumber.open(pdf_path) as pdf:

        table_data = extract_transactions(pdf)

        for page in pdf.pages:

            words = page.extract_words()

            tables = page.find_tables()

            table_bbox = tables[0].bbox if tables else None

            lines_map = {}

            for word in words:

                x0 = word["x0"]
                x1 = word["x1"]
                top = word["top"]

                if table_bbox:

                    tx0, ty0, tx1, ty1 = table_bbox

                    if (
                        x0 >= tx0
                        and x1 <= tx1
                        and top >= ty0
                        and top <= ty1
                    ):
                        continue

                key = round(top, 1)

                lines_map.setdefault(key, []).append((x0, word["text"]))

            for _, line_words in sorted(lines_map.items()):

                line_words.sort(key=lambda x: x[0])

                line = " ".join(word for _, word in line_words)

                line = clean_text(line)

                key, value = extract_kv_from_line(line)

                if key and value:
                    outside_data[key] = value

    return table_data, outside_data