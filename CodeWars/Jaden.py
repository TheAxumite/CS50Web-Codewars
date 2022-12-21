jaden = ''
string = "How can mirrors be real if our eyes aren't real"
counter = 0
for letter in string:
    if counter > 0:
        jaden += letter.upper()
        counter = 0
    else:
        if letter.isalpha:
            jaden += letter
        if letter == " ":
            jaden += letter
            counter = 1
           

print(jaden)