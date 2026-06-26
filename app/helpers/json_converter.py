def rows_to_json(rows):

    if not rows:
        return []

    # Already JSON
    if isinstance(rows[0], dict):
        return rows

    headers = rows[0]

    result = []

    for row in rows[1:]:

        obj = {}

        for i, col in enumerate(headers):
            obj[col] = row[i] if i < len(row) else ""

        result.append(obj)

    return result