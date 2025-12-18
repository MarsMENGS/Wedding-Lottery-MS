def contains_digit_4(n: int) -> bool:
    return '4' in str(n)

def filter_numbers_without_4(start: int, end: int) -> list[int]:
    return [n for n in range(start, end + 1) if not contains_digit_4(n)]

def is_valid_gap(selected: list[int], candidate: int, min_gap: int = 5) -> bool:
    return all(abs(candidate - x) >= min_gap for x in selected)