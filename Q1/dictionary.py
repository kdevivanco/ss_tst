# Write a function in Python that forms a dictionary from the input string. The data separator is the symbol ":";
# Example string:
# "key1:val1:key2:val2";
# It is very important that the function does not fall 
# and always returns a result by which the string can be restored up 
# to the order of the fields (the order is not important).

inp = 'key1:val1:key2:val2'

def string_to_dictionary(input_string):
    data = input_string.split(":")
    dictionary = {}
    print(data)
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            key = data[i].strip()
            value = data[i + 1].strip()
            dictionary[key] = value
    print(type(data))

    #if the sentence has impair amount of keys and values...
    if len(data) % 2 !=0:
        key = data[-1]
        value = ''
        dictionary[key] = value
    

    return dictionary

dicta = string_to_dictionary(inp)
print(dicta)

def reconstruct_sentence(dictionary):
    sentence = '"'
    for key, value in dictionary.items():
        sentence += key + ':' + value + ':'
    sentence = sentence[:-2]
    sentence += '"'
    return sentence

print(reconstruct_sentence(dicta))