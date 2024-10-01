def convert_fa_numbers(fa_number: str) -> int:
    persians = '۰۱۲۳۴۵۶۷۸۹'
    number = 0
    for fa_digit in fa_number:
        number = number*10 + persians.index(fa_digit)
    return number