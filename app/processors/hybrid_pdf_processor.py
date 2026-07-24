from app.processors.pdf_processor import process_pdf
from app.processors.table_validator import is_good_table
from app.pdf_table_extractor.extractor import process_borderless_table


def process_hybrid_pdf(pdf_path):

    print("\n" + "=" * 60)
    print("Trying Structured Extraction")
    print("=" * 60)

    table_data, outside_data = process_pdf(pdf_path)

    print(f"Structured rows found: {len(table_data)}")

    if is_good_table(table_data):

        print("Structured Table Found")
        print("Skipping OCR...")

        return table_data, outside_data

    print("Structured Extraction Failed")
    print("Running OCR...")

    records = process_borderless_table(pdf_path)

    if not records:
        return [], outside_data

    return records, outside_data