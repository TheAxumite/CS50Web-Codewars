jaden = ''
string = "How can mirrors be real if our 5 eyes aren't real"
counter = 0
for letter in string:
    if counter > -1:
        jaden += letter.upper()
        counter = -1
    else:
        if letter.isalpha:
            jaden += letter
        if letter == " ":
            jaden += letter
            counter = 1
           

print(jaden)