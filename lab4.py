import pdnf

def summator_table():
    arguments_number = 3
    arguments = pdnf.create_dictionary(arguments_number)
    b = [0 for i in range(len(arguments['x1']))]
    d = b.copy()
    for i in range(len(arguments['x1'])):
        sum = arguments['x1'][i] + arguments['x2'][i] + arguments['x3'][i]
        if sum >= 2:
            b[i] = 1
            sum -= 2
        if sum == 1:
            d[i] = 1
    return d, b

def plus_five():
    arguments_number = 4
    arguments = pdnf.create_dictionary(arguments_number)
    five_bin = [0, 1, 0, 1]
    five_dec = 5
    y = [[0 for m in range(len(arguments['x1']))] for n in range(arguments_number)]
    for i in range(len(arguments['x1']) - five_dec):
        index = arguments_number
        plusone = 0
        while index > 0:
            sum = arguments['x'+str(index)][i] + five_bin[index-1] + plusone
            plusone = 0
            if sum >= 2:
                sum -= 2
                plusone = 1
            y[index-1][i] = sum
            index -= 1
    return y

print('\nПервое задание\nодноразрядный двоичный сумматор на 3 входа:\n')
arguments_number = 3
d, b = summator_table()
arguments = pdnf.create_dictionary(arguments_number)
print('x1: ' + ' '.join([str(el) for el in arguments['x1']]))
print('x2: ' + ' '.join([str(el) for el in arguments['x2']]))
print('x3: ' + ' '.join([str(el) for el in arguments['x3']]))
print('d:  ' + ' '.join([str(el) for el in d]))
print('b:  ' + ' '.join([str(el) for el in b]))

d_pdnf = pdnf.PDNF(d, arguments_number)
print('\nPDNF(d): ' + pdnf.string_formula(d_pdnf))
d_simplified = pdnf.simplify(d_pdnf)
d_simplified = pdnf.string_formula(d_simplified)
print('TDNF(d): ' + d_simplified)
logism_grammar = d_simplified.replace('!', '~')
logism_grammar = logism_grammar.replace('*', '&')
print('TDNF(d) for logism: ' + logism_grammar)

b_pdnf = pdnf.PDNF(b, arguments_number)
print('\nPDNF(d): ' + pdnf.string_formula(b_pdnf))
b_simplified = pdnf.simplify(b_pdnf)
b_simplified = pdnf.string_formula(b_simplified)
print('TDNF(d): ' + b_simplified)
logism_grammar = b_simplified.replace('!', '~')
logism_grammar = logism_grammar.replace('*', '&')
print('TDNF(b) for logism: ' + logism_grammar)

print('\nВторое задание:\nn = 5\n')
arguments_number = 4
arguments = pdnf.create_dictionary(arguments_number)
for i in range(arguments_number):
    print('x' + str(i+1) +': ' + ' '.join([str(el) for el in arguments['x'+str(i+1)]]))
result = plus_five()
print('-----------------------------------')
for i in range(arguments_number):
    print('y' + str(i+1) + ': ' + ' '.join([str(el) for el in result[i]]))

for i in range(arguments_number):
    y_pdnf = pdnf.PDNF(result[i], arguments_number)
    print('\nPDNF(y' + str(i+1) + '): ' + pdnf.string_formula(y_pdnf))
    y_simplified = pdnf.simplify(y_pdnf)
    y_simplified = pdnf.string_formula(y_simplified)
    print('TDNF(y' + str(i+1) + '): ' + y_simplified)
    logism_grammar = y_simplified.replace('!', '~')
    logism_grammar = logism_grammar.replace('*', '&')
    print('TDNF(y' + str(i+1) + ') for logism: ' + logism_grammar)