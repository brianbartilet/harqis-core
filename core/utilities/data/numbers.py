def safe_number(value):
    """
    Safely cast values to int or float.
    Returns 0 if casting fails.
    """
    try:
        # remove commas like "1,200.00"
        value = str(value).replace(",", "").strip()

        # auto-detect int or float
        if "." in value:
            return float(value)
        else:
            return int(value)
    except:
        return 0
