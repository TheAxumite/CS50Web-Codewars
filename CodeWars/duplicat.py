
lst = "rararararaarararararararararrarararararararr321aaaaaaa"
list = [] 
list_2 = []
greater = False 
keys = []
values = []
convert = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
          6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',
          11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
          15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',
          19 : 'nineteen', 20 : 'twenty',
          30 : 'thirty', 40 : 'forty', 50 : 'fifty', 60 : 'sixty',
          70 : 'seventy', 80 : 'eighty', 90 : 'ninety' }
for l in lst:
    array = {}
    array[l] = lst.count(l)
    list.append(array)
for dic in list:
    for key, value in dic.items():
        if value > 1 and dic not in list_2:
            list_2.append(dic)
            if value > 2:
                greater = True



if not list_2:
    print("no characters repeats more than once")
if len(list_2) == 2 and greater == False:
    for dic in list_2:
        for key, value in dic.items():
            keys.append(key)
    print(f"{keys[0]} and {keys[1]}")
if len(list_2) == 2 and greater == True:
    for dic in list_2:
        for key, value in dic.items():
            keys.append(key)
            if (value < 20):
                values.append(convert[value])
            if(value > 20 and value < 100):
                if value % 10 == 0: 
                    values.append(convert[value])
                else:
                    values.append(convert[value // 10 * 10] + '-' + convert[value % 10])
    print(f"{keys[0]} occures {values[0]} times and {keys[1]} occures {values[1]}")

if (len(list_2) < 2):
    for dic in list_2:
        for key, value in dic.items():
            print(f"{key} occures {value} times")
    

