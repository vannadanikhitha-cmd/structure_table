from processors.pdf_processor import (
    process_pdf
)

from processors.table_validator import (
    is_good_table
)

from pdf_table_extractor.extractor import (
    process_borderless_table
)


def process_hybrid_pdf(pdf_path):

    print()

    print("=" * 60)

    print("Trying Structured Extraction")

    print("=" * 60)

    table_data, outside_data = process_pdf(
        pdf_path
    )

    # ----------------------------
    # Axis
    # SBI
    # HDFC
    # ----------------------------

    if is_good_table(table_data):

        print("Structured Table Found")

        return table_data, outside_data

    # ----------------------------
    # OCR
    # Bank of Baroda
    # ----------------------------

    print("Structured Extraction Failed")

    print("Running OCR")

    records = process_borderless_table(
        pdf_path
    )

    if not records:

        return [], outside_data

    return records, outside_data