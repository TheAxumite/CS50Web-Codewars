import re

sentence = '### Start a ***sent#ence*** #and then **bring** it **to** an _end_'

converter_dict ={
       '**':      ['<b>', '</b>'],
       '*':      ['<b>', '</b>'], 
        '_':      ['<i>', '</i>'], 
       '\n':      '<br>',
        '#':      ['<h5>','</h5>'],
       '##':      ['<h4>','</h4>'],
      '###':      ['<h3>','</h3>'],
     '####':      ['<h2>','</h2>'],
    '#####':      ['<h1>','</h1>'],
    '\r': '<br>'
}

pattern_list = [ "r'\*{3}|\*{2}|\*{1}'"] 

found_list = []

for list in pattern_list:
    pattern = re.compile(list)
    words = re.split(' ', sentence)
    print(words)
    for word in words:
        matched = pattern.finditer(word)
        for match in matched:
            group = {f'{match.group()}': [match.start(), match.end()]}
            found_list.append(group)
    

    
print(found_list)