def clip(val: int, a: int, b: int) -> int:
    # Clips `val` to range [min(a, b), max(a, b)]
    if a > b:
        a, b = b, a
    return min(max(val, a), b)
