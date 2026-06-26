import pdfplumber

from helpers.text_cleaner import clean_text

from extractors.key_value_extractor import (
    extract_kv_from_line
)

from extractors.transaction_extractor import (
    extract_transactions
)


def process_pdf(pdf_path):

    """
    Returns

    table_data -> Structured transactions

    outside_data -> Header / footer key-values
    """

    outside_data = {}

    # ----------------------------
    # Structured transaction extraction
    # ----------------------------

    table_data = extract_transactions(
        pdf_path
    )

    # ----------------------------
    # Outside data extraction
    # ----------------------------

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            words = page.extract_words()

            tables = page.find_tables()

            table_bbox = (
                tables[0].bbox
                if tables
                else None
            )

            lines_map = {}

            for word in words:

                x0 = word["x0"]
                x1 = word["x1"]
                top = word["top"]

                # Ignore table area

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

                if key not in lines_map:

                    lines_map[key] = []

                lines_map[key].append(
                    (
                        x0,
                        word["text"]
                    )
                )

            # rebuild text

            for _, line_words in sorted(
                lines_map.items()
            ):

                line_words.sort(
                    key=lambda x: x[0]
                )

                line = " ".join(
                    w[1]
                    for w in line_words
                )

                line = clean_text(line)

                key, value = extract_kv_from_line(
                    line
                )

                if key and value:

                    outside_data[key] = value

    return table_data, outside_data