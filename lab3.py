import lab2 as p

arguments_number = 3
table_width = 4
table_height = 2

def read_bracket(line):
    i = 0
    konst = []
    while line[i] != ')':
        if line[i] == 'x':
            if line[i-1] == '!':
                konst.append(0)
            else:
                konst.append(1)
        i += 1
    return konst

def read_line(line):
    perfect_form = []
    i = 0
    while i < len(line):
        if line[i] == '(':
            perfect_form.append(read_bracket(line[i:]))
        i+=1
    return perfect_form

def type(line):
    i = 0
    while i < len(line):
        if line[i] == '+':
            return 'con'
        elif line[i] == '*':
            return 'dis'
        i+=1

def mergable(constit1, constit2, arg_index):
    mergability = True
    for i in range(arguments_number):
        if i != arg_index and constit1[i] != constit2[i]:
            mergability = False
            break
        if i == arg_index and constit1[i] == constit2[i]:
            mergability = False
            break
    return mergability

def merge(formula):
    merged = []
    used = [False for i in range(len(formula))]
    for i in range(arguments_number):
        for j in range(len(formula)-1):
            for k in range(j+1, len(formula)):
                if mergable(formula[j], formula[k], i):
                    used[j] = True
                    used[k] = True
                    merged.append(formula[j].copy())
                    merged[-1].pop(i)
                    merged[-1].insert(i, -1)
                    break
    for el in used:
        if not(el):
            return None
    return merged

def merge2(formula):
    merged = []
    used = [False for i in range(len(formula))]
    for i in range(arguments_number):
        for j in range(len(formula)-1):
            for k in range(j+1, len(formula)):
                if mergable(formula[j], formula[k], i):
                    used[j] = True
                    used[k] = True
                    merged.append(formula[j].copy())
                    merged[-1].pop(i)
                    merged[-1].insert(i, -1)
                    break
    for i in range(len(used)):
        if not(used[i]):
            merged.append(formula[i])
    return merged

def substitute(values, formula, ftype):
    for i in range(len(values)):
        if values[i] == -1:
            missed_value = i
    for i in range(len(formula)):
        if formula[i] != -1 and i != missed_value:
            existing_arg = i
    res = []
    res.append(formula[missed_value])
    if formula[existing_arg] == values[existing_arg]:
        if ftype == 'dis':
            res.append(1)
        else:
            res.append(0)
    else:
        if ftype == 'dis':
            res.append(0)
        else:
            res.append(1)
    return res
                
def delete_excess(formula, ftype):
    new_formula = formula.copy()
    if ftype == 'dis':
        no_change = 1
    else:
        no_change = 0
    i = 0
    while i < len(new_formula):
        res= []
        for other in new_formula:
            if new_formula[i] != other:
                sub = substitute(new_formula[i], other, ftype)
                if sub[1] == no_change:
                    res.append(sub[0])
        pos, neg = False, False
        for arg in res:
            if arg == 0: neg = True
            if arg == 1: pos = True
        if pos and neg:
            new_formula.pop(i)
        else:
            i+=1
    return new_formula
                
def string_formula(formula, type):
    arg_length = 3
    if type == 'dis':
        inside = '*'
        outside = '+'
    else:
        inside = '+'
        outside = '*'
    substring = []
    for i in range(len(formula)):
        args = []
        for j in range(len(formula[i])):
            if formula[i][j] == 0:
                args.append('!x'+str(j+1))
            if formula[i][j] == 1:
                args.append('x'+str(j+1))
        substring.append(inside.join(args))
        if len(substring[-1]) > arg_length:
            substring[-1] = '(' + substring[-1] + ')'
    output = outside.join(substring)
    return output

def table(implicants, constituents):
    tabl = [['x' for i in range(len(constituents))] for j in range(len(implicants))]
    for impl in range(len(implicants)):
        for con in range(len(constituents)):
            for i in range(arguments_number):
                if implicants[impl][i] != -1 and implicants[impl][i] != constituents[con][i]:
                    tabl[impl][con] = ' '
    return tabl

def find_x(table, missing, index):
    find = False
    for i in range(len(table)):
        if i != missing:
            if table[i][index] == 'x':
                find = True
    return find


def quine(table, implicants):
    i = 0
    reduced = implicants.copy()
    table2 = table.copy()
    while i < len(reduced):
        excess = True
        for j in range(len(table2[i])):
            if not(find_x(table2, i, j)):
                excess = False
        if excess:
            reduced.pop(i)
            table2.pop(i)
        else:
            i+=1
    return reduced

def table_method(formula, ftype):
    tabl = [[0 for j in range(table_width)] for i in range(table_height)]
    for constituent in formula:
        if ftype == 'con':
            constituent = reverse(constituent)
        x1 = constituent[0]
        if constituent[1] == 0 and constituent[2] == 0:
            x2x3 = 0
        elif constituent[1] == 0 and constituent[2] == 1:
            x2x3 = 1
        elif constituent[1] == 1 and constituent[2] == 1:
            x2x3 = 2
        else:
            x2x3 = 3
        tabl[x1][x2x3] = 1
    if ftype == 'con':
        for constituent in formula:
            constituent = reverse(constituent)
    return tabl


def reverse(formula):
    for i in range(len(formula)):
        if formula[i] == 0:
            formula[i] = 1
        elif formula[i] == 1:
            formula[i] = 0
    return formula

def next(index, list_len):
    if index == list_len-1:
        return 0
    else:
        return index+1
    
def number(i, j):
    return 4*i + j

def find_implicants(tabl, ftype):
    pairs = []
    for i in range(table_height):
        for j in range(table_width):
            if tabl[i][j] == 1 and tabl[i][next(j, table_width)] == 1:
                    pairs.append([number(i, j), number(i, next(j, table_width))])
    for j in range(table_width):
        if tabl[0][j] == 1 and tabl[1][j] == 1:
            pairs.append([number(0, j), number(1, j)])
    i = 0
    while i < len(pairs):
        if is_excess(pairs[i], pairs):
            pairs.pop(i)
        else:
            i+=1
    implicants = []
    for pair in pairs:
        implicants.append(pair_to_implicant(pair, ftype))
    return implicants

def pair_to_implicant(pair, ftype):
    formula = []
    zero_range = 3
    for i in range(len(pair)):
        if pair[i] > zero_range:
            x1 = 1
            pair[i]-=table_width
        else:
            x1 = 0
        if pair[i] == 0:
            x2, x3 = 0, 0
        if pair[i] == 1:
            x2, x3 = 0, 1
        if pair[i] == 2:
            x2, x3 = 1, 1
        if pair[i] == 3:
            x2, x3 = 1, 0
        formula.append([x1,x2,x3])
    implicant = merge(formula)[0]
    if ftype == 'con':
        implicant = reverse(implicant)
    return implicant

def is_excess(pair, pairs):
    first_find = False
    second_find = False
    for other in pairs:
        if other != pair:
            if other[1] == pair[0] or other[0] == pair[0]:
                first_find = True
            if other[0] == pair[1] or other[1] == pair[1]:
                second_find = True
    return first_find and second_find

def change_table(tabl, formula_type):
    if formula_type == 'con':
        for i in range(len(tabl)):
            tabl[i] = reverse(tabl[i])
        for i in range(len(tabl)):
            for j in range(len(tabl[i])):
                if tabl[i][j] == 1:
                    tabl[i][j] = ' '
    else:
        for i in range(len(tabl)):
            for j in range(len(tabl[i])):
                if tabl[i][j] == 0:
                    tabl[i][j] = ' '
    return tabl


line = input("введите выражение: ")
truth = p.truth_table(line)
perfect = [p.PDNF(truth), p.PCNF(truth)]
for line in perfect:
    formula = read_line(line)
    formula_type = type(line)
    if formula_type == 'dis':
        str_impl = 'CДНФ: '
        final = 'ТДНФ: '
    else:
        str_impl = 'СКНФ: '
        final = 'ТКНФ: '
    implicants = merge(formula)
    print('\n' + str_impl, end = '')
    print(line)
    if implicants != None:
        print('\nрасчетный метод:')
        reduced = delete_excess(implicants, formula_type)
        reduced_again = merge2(reduced)
        print(str_impl + string_formula(implicants, formula_type))
        print(final + string_formula(reduced, formula_type))
        print(final + string_formula(reduced_again, formula_type))

        print('\n\nрасчетно-табличный метод:')
        if formula_type == 'dis':
            constituents = line.split('+')
        else:
            constituents = line.split('*')
        tablet = table(implicants, formula)
        reduced2 = quine(tablet, implicants)
        reduced_again2 = merge2(reduced2)
        print('\n\t\t\t\t\tконституенты')
        print('импликанты\t', end='')
        for constit in constituents:
            print(constit.center(15), end='')
        print('')
        for i in range(len(implicants)):
            print(string_formula([implicants[i]], formula_type).ljust(16), end='')
            for j in range(len(tablet[i])):
                print(tablet[i][j].center(15), end='')
            print('')
        print('\n' + final + string_formula(reduced2, formula_type))
        print(final + string_formula(reduced_again2, formula_type))

        print('\nтабличный метод:')
        tabl = table_method(formula, formula_type)
        implicants = find_implicants(tabl, formula_type)
        print('\nx1^', end='')
        tabl = change_table(tabl, formula_type)
        i = len(tabl)-1
        while i >= 0:
            print('\n' + str(i) + ' |', end='  ')
            for j in range(len(tabl[i])):
                print(tabl[i][j], end='  ')
            i-=1
        print('\n   ------------->\n     00 01 11 10  x2 x3')
        print('\n' + final + string_formula(implicants, formula_type))
        reduced_again3 = merge2(implicants)
        print(final + string_formula(reduced_again3, formula_type))
    else:
        print('не удалось склеить все конституенты')