import math
roman = []
"""
def solution(n):

    number = n
    convert = str(number)
    if int(number) > 0:
        if number > 999:
            roman.append('M')
        if number < 1000 and number > 100:
            c = int(str(convert[1])) * 100
            if c > 700:
                calculate = (int((1000-c)/100))
                roman.append('C' * calculate)
                roman.append('M')
        if number < 100 and number > 10:
            print(convert)
            c = int(str(convert[1])) * 10

            if c == 50:
                roman.append('L')
            if c < 50:
                roman.append('I' * int(c/10))



        solution(int(number/10))

    return roman

solution(4840)
print(''.join(roman))
"""


def reverse(n):
    num = n
    reversed_num = 0

    while num != 0:
        digit = num % 10
        reversed_num = reversed_num * 10 + digit
        num //= 10
    print(reversed_num)
    return reversed_num


def solution(n):

    reversed_num = n
    convert = str(reversed_num)
    
    if int(reversed_num) > 0:

        if reversed_num > 999:
            roman.append('M' * int(convert[3]))

        if reversed_num < 1000 and reversed_num > 100:
            c = (int(convert[2])) * 100
            if c == 500:
                roman.append('D')
            if c > 500 and c < 900:
                calculate = (int(convert[2]) - 5)
                roman.append('D')
                roman.append('C' * calculate)
            if c > 99 and c < 400:
                roman.append('C' * int(str(convert[2])))

        if reversed_num < 100 and reversed_num > 10:
            c = int(convert[1]) * 10
        
            if c >= 50:
                roman.append('L')
            if c < 50:
                roman.append('I' * int(convert[1]))
            if c > 50 and c < 90:
                roman.append('X' * (int(convert[1])-5))
        if reversed_num * 10 == 10:
            roman.append('X')
        if reversed_num <= 10:
    
            if reversed_num >= 5:
                roman.append('V')
                calculate = reversed_num - 5
                roman.append('I' * calculate)
            else:
                roman.append('I' * reversed_num)
        

        solution(int(reversed_num/10))

    return roman


solution(reverse(3121))
print(''.join(roman))
