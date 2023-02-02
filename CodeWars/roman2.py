def to_roman(num):
    values = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    symbols = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    result = ""
    for value, symbol in zip(values, symbols):
        while num >= value:
            print(num)
            result += symbol
            num -= value
    return result


