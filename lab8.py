table_len = 16
Vlen = 3
Alen = 4
Slen = 5

def print_table(table):
    for raw in table:
        print(' '.join(str(raw[i]) for i in range(Vlen)), end = '|')
        print(' '.join(str(raw[i]) for i in range(Vlen, Vlen+Alen)), end = '|')
        print(' '.join(str(raw[i]) for i in range(Vlen+Alen, Vlen+Alen*2)), end = '|')
        print(' '.join(str(raw[i]) for i in range(Vlen+Alen*2, table_len)), end = '\n')

def next_index(current_index, shift):
    index = current_index + shift
    if index >= table_len:
        index -= table_len
    return index

def diagonal(normal_table):
    diagonal_table = [[0 for i in range(table_len)] for j in range(table_len)]
    for i in range(len(normal_table)):
        for j in range(table_len):
            diagonal_table[next_index(j, i)][i] = normal_table[j][i]
    return diagonal_table

def add(normal_table, diagonal_table, word):
    for i in range(table_len):
        if normal_table[i] == [0 for k in range(table_len)]:
            normal_table[i] = word
            break
    for j in range(table_len):
        diagonal_table[next_index(i, j)][j] = word[j]

def addition(normal_table, diagonal_table, V):
    V = [int(V[i]) for i in range(len(V))]
    suit = []
    for i in range(len(normal_table)):
        if [normal_table[i][j] for j in range(len(V))] == V:
            suit.append(i)
    for index in suit:

        plusone = 0
        for i in range(Alen):
            res = diagonal_table[next_index(index, Vlen+Alen*2-i-1)][table_len-1-i-Slen] + diagonal_table[next_index(index, Vlen+Alen-i-1)][table_len-1-i-Slen-Alen] + plusone
            plusone = 0
            if res >= 2:
                res -= 2
                plusone = 1
            normal_table[index][table_len-1-i] = res
            diagonal_table[next_index(index, table_len-1-i)][table_len-1-i] = res
        normal_table[index][table_len-Slen] = plusone
        diagonal_table[next_index(index, table_len-Slen)][table_len-Slen] = plusone

def read_word(diagonal_table, index):
    word = [diagonal_table[next_index(index, i)][i] for i in range(table_len)]
    return word

def f7(word1, word2):
    result = []
    for i in range(len(word1)):
        if word1[i] == 1 or word2[i] == 1:
            result.append(1)
        else:
            result.append(0)
    return result

def f8(word1, word2):
    result = []
    for i in range(len(word1)):
        if not(word1[i] == 1 or word2[i] == 1):
            result.append(1)
        else:
            result.append(0)
    return result

def f2(word1, word2):
    result = []
    for i in range(len(word1)):
        if word1[i] == 1 and word2[i] == 0:
            result.append(1)
        else:
            result.append(0)
    return result

def f13(word1, word2):
    result = []
    for i in range(len(word1)):
        if word1[i] == 0 or word2[i] == 1:
            result.append(1)
        else:
            result.append(0)
    return result

def compare(word_1, word_2):
    g = False
    l = False
    word1, word2 = [],[]
    for i in range(len(word_1)):
        if word_1[i] == 0: word1.append(False)
        else: word1.append(True)
        if word_2[i] == 0: word2.append(False)
        else: word2.append(True)
    for i in range(len(word_1)):
        g1 = g or (not(word2[i]) and word1[i] and not(l))
        l1 = l or (word2[i] and not(word1[i]) and not(g))
        g = g1
        l = l1
    if g and not(l): return 'bigger'
    elif not(g) and l: return 'smaller'
    else: return 'equal'

def range_search(diagonal_table, lower_border, upper_border):
    between = []
    for i in range(table_len):
        word = read_word(diagonal_table, i)
        if compare(word, lower_border) == 'bigger' and compare(word, upper_border) == 'smaller':
            between.append(word)
    return between

normal_table = [[0 for i in range(table_len)] for j in range(table_len)]
diagonal_table = diagonal(normal_table)
while True:
    operation = input('\n1 - add new word\n2 - addition\n3 - read a word\n4 - bool operation\n5 - search in range\n6 - show the tables\n')
    match(operation):
        case '1':
            word = input()
            word = word.split(' ')
            word = [int(el) for el in word]
            add(normal_table, diagonal_table, word)
        case '2':
            V = input('input V: ')
            addition(normal_table, diagonal_table, V)
        case '3':
            index = int(input('Index of word: '))
            print(read_word(diagonal_table, index))
        case '4':
            op = input('choose operation: f7, f8, f2 or f13: ')
            index1 = int(input('index of first word: '))
            index2 = int(input('index of second word: '))
            word1 = read_word(diagonal_table, index1)
            word2 = read_word(diagonal_table, index2)
            match(op):
                case 'f7':
                    add(normal_table, diagonal_table, f7(word1, word2))
                case 'f8':
                    add(normal_table, diagonal_table, f8(word1, word2))
                case 'f2':
                    add(normal_table, diagonal_table, f2(word1, word2))
                case 'f13':
                    add(normal_table, diagonal_table, f13(word1, word2))
        case '5':
            lower_border = input('lower border: ')
            lower_border = lower_border.split(' ')
            lower_border = [int(el) for el in lower_border]
            upper_border = input('upper border: ')
            upper_border = upper_border.split(' ')
            upper_border = [int(el) for el in upper_border]
            between = range_search(diagonal_table, lower_border, upper_border)
            if between == []:
                print('no words within this range\n')
            else:
                for word in between:
                    print(word)
        case '6':
            print('\nNormal table:')
            print_table(normal_table)
            print('\nDiagonal table:\n')
            print_table(diagonal_table)