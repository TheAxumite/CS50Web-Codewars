#Replaces string with its alphabet position
def alphabet_position(text):
    position = []
    for l in text:
        if l.isalpha():
            position.append(str(ord(l.upper())-64))
    return ' '.join(position)



print(alphabet_position("The sunset sets at twelve o' clock."))