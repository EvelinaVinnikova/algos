ordered_characters = {
    '(': 15, ')': 16,
    '++': 14, '--': 14,
    '~': 13, '!': 13, 'not': 13,
    '**': 12,
    '*': 11, '/': 11, '//': 11, '%': 11,
    '+': 10, '-': 10,
    '<<': 9, '>>': 9,
    '&': 8,
    '^': 7,
    '|': 6,
    '<': 5, '<=': 5, '>': 5, '>=': 5, '!=': 5, '==': 5,
    'is': 4, 'not is': 4, 'in': 4, 'not in': 4,
    'and': 3,
    'or': 2,
    ',': 1,
    '1': 0, '2': 0, '3': 0, '4': 0, '5': 0,
    '6': 0, '7': 0, '8': 0, '9': 0
}


def implementation(line: str)-> list:
    '''This function takes one character from input, and creates a reverse Polish expression'''
    line += ' '
    result = []
    character = ''
    operations = []
    for i in range(len(line)):
        symb = line[i]
        if symb == ' ':
            if character == '':
                continue
            
            if 0 < ordered_characters[character] < 17:
                if ordered_characters[character] == 15: # открывающаяся скобка
                    result.append(character)
                elif ordered_characters[character] == 16: # закрывающая скобка
                    while(1):
                        if operations == 0:
                            break
                        temp = operations.pop()
                        if temp == '(':
                            break
                        result.append(temp)
                elif len(operations) and (ordered_characters[operations[-1]] != 15) and  (ordered_characters[operations[-1]] > ordered_characters[character]):
                    result.append(operations.pop())

                operations.append(character)
            
            elif ordered_characters[character] == 0:
                result.append(character)

            character = ''
            continue
        else:
            character += symb

    if character:
        result.append(character)
    while operations:
        result.append(operations.pop())
    return result


print("Enter the math expression (spaces necessary): \n")
line1 = "6 ++ * ( 4 - 2 ** 3 )"
result1 = implementation(line1)
assert ' '.join(result1) == "6 ++ ( 4 2 3 ** - ) *", "Incorrect output 1"
line2 = "5 >> 2 * 7 - 1 ++"
result2 = implementation(line2)
assert ' '.join(result2) == "5 2 7 * 1 ++ - >>", "Incorrect output 2"
line3 = "6 - 1 * ( 7 - 3 ** 2 * 5 ** 4 ** 2 ++ )"
result3 = implementation(line3)
assert ' '.join(result3) == "6 1 ( 7 3 2 ** 5 4 2 ++ ** ** * - ) * -", "Incorrect output 3"
line4 = "5 ** 2 ** 3"
result4 = implementation(line4)
assert ' '.join(result4) == "5 2 3 ** **", "Incorrect output 4"
#print(' '.join(result4))
