def safe_get(data, key, default="N/A"):
    value = data.get(key)
    return str(value) if value not in [None, ""] else default
