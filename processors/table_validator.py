def is_good_table(table_data):

    if not table_data:
        return False

    if len(table_data) == 0:
        return False

    # Structured extractor returns list of dictionaries
    if isinstance(table_data[0], dict):

        headers = list(table_data[0].keys())

        if len(headers) < 2:
            return False

        valid_rows = 0

        for row in table_data:

            filled = sum(
                1
                for value in row.values()
                if str(value).strip()
            )

            if filled >= max(1, len(headers) // 2):
                valid_rows += 1

        return valid_rows > 0

    # OCR extractor returns list[list]

    header = table_data[0]

    if len(header) < 2:
        return False

    valid_rows = 0

    for row in table_data[1:]:

        filled = sum(
            1
            for cell in row
            if str(cell).strip()
        )

        if filled >= max(1, len(header) // 2):
            valid_rows += 1

    return valid_rows > 0