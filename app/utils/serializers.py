def serial(value):
    if isinstance(value, dict):
        return {key: serial(item) for key, item in value.items()}
    if hasattr(value, "__float__"):
        try:
            return float(value)
        except Exception:
            pass
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def row_serial(row):
    return {key: serial(value) for key, value in row.items()}
