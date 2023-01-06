import re

converter_dict ={
       '**':      ['<b>', '</b>'],
       '***':      ['<b><i>', '</i></b>'],
       '*':      ['<li>', '</li>'], 
        '__':      ['<b>', '</b>'], 
        '_':      ['<i>', '</i>'], 
       '\n':      '<br>',
        '#':      ['<h5>','</h5>'],
       '##':      ['<h4>','</h4>'],
      '###':      ['<h3>','</h3>'],
     '####':      ['<h2>','</h2>'],
    '#####':      ['<h1>','</h1>'],
    '\r': '<br>'
}


sentence = "Django is a web framework written using [Python] (/wiki/Python) that allows for the design of web applications that generate [HTML] (/wiki/HTML) dynamically."
lines = ' '.join(re.split('[\n] ', sentence))
words = re.split(' ', lines)
print(words)
pattern = re.compile(r'^\#{2}$|\#{3}$|\#{1}|\#{4}$')
second_pattern = re.compile(r"^\*{3}|\*{3}$|^\*{2}|\*{2}|^\*{1}|\*{1}$|\_")
pattern_3 = re.compile(r"\[(.*?)\]|\((.*?)\)")
pattern_4 = re.compile(r'^\+{1}$|^\*{1}$')
new_sentence = []
second_word = ''
length = 0

if re.search(pattern, words[0]) is not None:
    temp_hold = words[0]
    print(temp_hold)
    words[0] = words[0].replace(temp_hold, converter_dict[temp_hold][0])
    words.append(converter_dict[temp_hold][1])   

for word in words:
    length = length + 1
    if re.search(second_pattern, word) is not None:
        matches = second_pattern.finditer(word)   
       
        for match in matches:
            holder = {f'{match.group()}': [match.start(), match.end()]}
            all_markup_found = len(re.findall(second_pattern, word))
            print(all_markup_found)
            for key, value in holder.items():
                if all_markup_found == 1:
                    if value[0]== 0:
                        new_word = word.replace(str(key), converter_dict[key][0],1) 
                        new_sentence.append(new_word)   
                    else:
                        second_word = word.replace(str(key), converter_dict[key][1],1)
                        new_sentence.append(second_word)     
                if all_markup_found == 2:
                     new_word = word.replace(str(key), converter_dict[key][0],1)
                     second_word = new_word.replace(str(key), converter_dict[key][1],1)
                     new_sentence.append(second_word) 
    elif not re.search(pattern_3, word):
        new_sentence.append(word)
    if re.search(pattern_3, word) is not None:
      
        print(word)
        if words[length][0] == '(' and  words[length][1] == '/':
            switch_value = '<a href ="' + words[length].strip("()") + '"' + " " + words[length-1].strip("[]") + '</a>'
            new_sentence.append(switch_value)  

        
    
    
print(" ".join(new_sentence))
        

                
                


    


