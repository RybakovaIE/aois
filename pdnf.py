def string_formula(formula):
    arg_length = 3
    inside = '*'
    outside = '+'
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

def PDNF(table, arguments_number):
    formula = []
    arguments = create_dictionary(arguments_number)
    for i in range(len(table)):
        if table[i] == 1:
            bracket = []
            for arg_index in range(1, arguments_number+1):
                bracket.append(arguments['x'+str(arg_index)][i])
            formula.append(bracket)
    return formula

def create_dictionary(arguments_number):
    dictionary = []
    for i in range(arguments_number):
        index = i+1
        same = 2**(arguments_number-index)
        array = [0 for j in range(same)]
        array += [1 for j in range(same)]
        while len(array) < 2**(arguments_number):
            array += array
        dictionary.append(['x'+str(index), array])
    dictionary = dict(dictionary)
    return dictionary

def summator_table():
    arguments_number = 3
    arguments = create_dictionary(arguments_number)
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

def is_mergable(constit1, constit2, arg_index, arguments_number):
    mergability = True
    for i in range(arguments_number):
        if i != arg_index and constit1[i] != constit2[i]:
            mergability = False
            break
        if i == arg_index and constit1[i] == constit2[i]:
            mergability = False
            break
    return mergability

def merge(formula, arguments_number):
    merged = []
    unmerged = []
    used = [False for i in range(len(formula))]
    for i in range(arguments_number):
        for j in range(len(formula)-1):
            for k in range(j+1, len(formula)):
                if is_mergable(formula[j], formula[k], i, arguments_number):
                    used[j] = True
                    used[k] = True
                    merged.append(formula[j].copy())
                    merged[-1].pop(i)
                    merged[-1].insert(i, -1)
                    break
    for i in range(len(used)):
        if not(used[i]):
            unmerged.append(formula[i])
    return merged, unmerged

def substitute(values, formula):
    for i in range(len(values)):
        if values[i] == -1:
            missed_value = i
    for i in range(len(formula)):
        if formula[i] != -1 and i != missed_value:
            existing_arg = i
    res = []
    res.append(formula[missed_value])
    if formula[existing_arg] == values[existing_arg]:
        res.append(1)
    else:
        res.append(0)
    return res
                
def delete_excess(formula):
    new_formula = formula.copy()
    no_change = 1
    i = 0
    while i < len(new_formula):
        res= []
        for other in new_formula:
            if new_formula[i] != other:
                sub = substitute(new_formula[i], other)
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

def delete_identical(formula):
    i = 0
    while i < len(formula)-1:
        same = False
        for j in range(i+1, len(formula)):
            if formula[i] == formula[j]:
                same = True
        if same:
            formula.pop(i)
        else:
            i+=1
    return formula

def simplify(formula):
    arguments_number = len(formula[0])
    i = arguments_number
    simplified = []
    merged = formula
    while i > 1:
        merged, unmerged = merge(merged, arguments_number)
        merged = delete_excess(merged)
        simplified += unmerged
        i -= 1
    simplified += merged
    formula = delete_identical(simplified)
    return simplified