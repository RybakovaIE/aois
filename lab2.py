arguments = {'x1': [0,0,0,0,1,1,1,1], 'x2': [0,0,1,1,0,0,1,1], 'x3' : [0,1,0,1,0,1,0,1]}
args_number = 3

def negative(truth_list):
    res = []
    for i in range(len(truth_list)):
        if truth_list[i] == 0:
            res.append(1)
        else:
            res.append(0)
    return res

def lengh(line):
    brackets = 1
    i = 0
    while brackets > 0:
        if line[i] == '(':
            brackets+=1
        elif line[i] == ')':
            brackets-=1
        i+=1
    return i

def conjunction(a,b):
    res = [0 for i in range(8)]
    for i in range(8):
        if a[i] == 1 and b[i] == 1:
            res[i] = 1
    return res

def disjunction(a,b):
    res = [1 for i in range(8)]
    for i in range(8):
        if a[i] == 0 and b[i] == 0:
            res[i] = 0
    return res

def implication(a,b):
    res = [1 for i in range(8)]
    for i in range(8):
        if a[i] == 1 and b[i] == 0:
            res[i] = 0
    return res

def equivalence(a,b):
    res = [0 for i in range(8)]
    for i in range(8):
        if a[i] == b[i]:
            res[i] = 1
    return res

def solve(arg1, arg2, operation):
    if operation == '*':
        res = [conjunction(arg1,arg2)]
    if operation == '+':
        res = [disjunction(arg1,arg2)]
    if operation == '->':
        res = [implication(arg1,arg2)]
    if operation == '~':
        res = [equivalence(arg1,arg2)]
    return res

def truth_table(line):
    args = []
    i = 0
    while i < len(line):
        if line[i] == '(':
            start = i + 1
            i = i + lengh(line[start:])
            args.append(truth_table(line[start:i]))
        elif line[i] == '!':
            if line[i+1] == 'x':
                args.append(negative(arguments[line[i+1:i+3]]))
                i+=2
            elif line[i+1] == '(':
                start = i + 2
                i = i + lengh(line[start:]) + 1
                args.append(negative(truth_table(line[start:i])))
        elif line[i] == 'x':
            args.append(arguments[line[i:i+2]])
            i+=1
        else:
            operation = line[i]
            if operation == '-':
                i+=1
                operation = operation + line[i]
        if len(args) == 2:
            args = solve(args[0], args[1], operation)
        i+=1
    return args[0]

def to_decimal(num_bin):
    i = 0
    num_dec = 0
    while i < len(num_bin):
        num_dec = num_dec + (2**(len(num_bin)-i-1))*num_bin[i]
        i+=1
    return num_dec

def PCNF(table):
    res = ''
    for i in range(len(table)):
        if table[i] == 0:
            if res != '':
                res = res + '*'
            res = res + '('
            arg_index = 1
            for x in arguments.values():
                if x[i] == 1:
                    res = res + '!'
                res = res + 'x' + str(arg_index)
                arg_index+=1
                if arg_index <= args_number:
                    res = res + '+'
            res = res + ')'
    return res

def number_PCNF(table):
    numbers = []
    for i in range(len(table)):
        if table[i] == 0:
            numbers.append(0)
            if arguments['x1'][i] == 1:
                numbers[-1] += 4
            if arguments['x2'][i] == 1:
                numbers[-1] += 2
            if arguments['x3'][i] == 1:
                numbers[-1] += 1
            numbers[-1] = str(numbers[-1])
    number_form = ','.join(numbers)
    number_form = '/\\(' + number_form + ')'
    return number_form

def PDNF(table):
    res = ''
    for i in range(len(table)):
        if table[i] == 1:
            if res != '':
                res = res + '+'
            res = res + '('
            arg_index = 1
            for x in arguments.values():
                if x[i] == 0:
                    res = res + '!'
                res = res + 'x' + str(arg_index)
                arg_index+=1
                if arg_index <= args_number:
                    res = res + '*'
            res = res + ')'
    return res
            
def number_PDNF(table):
    numbers = []
    for i in range(len(table)):
        if table[i] == 1:
            numbers.append(0)
            if arguments['x1'][i] == 1:
                numbers[-1] += 4
            if arguments['x2'][i] == 1:
                numbers[-1] += 2
            if arguments['x3'][i] == 1:
                numbers[-1] += 1
            numbers[-1] = str(numbers[-1])
    number_form = ','.join(numbers)
    number_form = '\\/(' + number_form + ')'
    return number_form

line = input("введите выражение: ")
res = truth_table(line)
print('\nТаблица истинности:')
print('x1:  ' + '  '.join(str(el) for el in arguments['x1']))
print('x2:  ' + '  '.join(str(el) for el in arguments['x2']))
print('x3:  ' + '  '.join(str(el) for el in arguments['x3']))
print('f:   ' + '  '.join(str(el) for el in res))
print('\nИндексная форма: ' + str(to_decimal(res)))
print('Числовая форма: ' + number_PCNF(res) + ' = ' + number_PDNF(res))
print('\nСКНФ:' + PCNF(res))
print('СДНФ:' + PDNF(res) + '\n')