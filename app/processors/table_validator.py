def is_good_table(table_data):

    if not table_data:
        return False

    if not isinstance(table_data[0], dict):
        return False

    headers = list(table_data[0].keys())

    if len(headers) < 2:
        return False

    for row in table_data:

        filled = sum(
            1
            for value in row.values()
            if str(value).strip()
        )

        if filled >= len(headers) // 2:
            return True

    return False