def to_nano(value) -> int:
    return int(float(value) * (10 ** 9))

def from_nano(value) -> float:
    return round(int(value) / 10 ** 9, 9)