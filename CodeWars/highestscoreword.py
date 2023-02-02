#Given a string of words, you need to find the highest scoring word.
def high(x):
    max_word = ""
    max_sum = 0
    curr_word = ""
    curr_sum = 0
    
    for char in x:
        if char.isalpha():
            curr_word += char
            curr_sum += ord(char.upper())-64
        else:
            if curr_sum > max_sum:
                max_sum = curr_sum
                max_word = curr_word
            curr_word = ""
            curr_sum = 0
    
    if curr_sum > max_sum:
        max_word = curr_word
    
    return max_word

print(high("what time are we climbing up the volcano"))
