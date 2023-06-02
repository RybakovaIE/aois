import random

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

def find_biggest(words):
    if words == []: return []
    current = words.copy()
    for i in range(len(words[0])):
        biggest = []
        for word in current:
            if word[i] == 1:
                biggest.append(word)
        if len(biggest) > 0:
            current = biggest
    return current

def find_smallest(words):
    if words == []: return []
    current = words.copy()
    for i in range(len(words[0])):
        smallest = []
        for word in current:
            if word[i] == 0:
                smallest.append(word)
        if len(smallest) > 0:
            current = smallest
    return current

def find_nearest_bigger(words, keyword):
    bigger = []
    for word in words:
        if compare(word, keyword) == 'bigger':
            bigger.append(word)
    nearest = find_smallest(bigger)
    return nearest

def find_nearest_smaller(words, keyword):
    smaller = []
    for word in words:
        if compare(word, keyword) == 'smaller':
            smaller.append(word)
    nearest = find_biggest(smaller)
    return nearest

def within_range(words, lower, top):
    within = []
    smaller = []
    smaller_flag = [1 for i in range(len(words))]
    for i in range(len(words)):
        if compare(words[i], top) != 'smaller':
            smaller_flag[i] = 0
    for i in range(len(words)):
        if smaller_flag[i] == 1:
            smaller.append(words[i])
    bigger_flag = [1 for i in range(len(smaller))]
    for i in range(len(smaller)):
        if compare(smaller[i], lower) != 'bigger':
            bigger_flag[i] = 0
    for i in range(len(smaller)):
        if bigger_flag[i] == 1:
            within.append(smaller[i])
    return within

words = []
while True:
    if words == []:
        words_num = int(input('number of words: '))
        word_len = int(input('length of words: '))
        words = [[random.randint(0,1) for n in range(word_len)] for m in range(words_num)]
        for word in words:
            print(word)
    operation = input('\n1 - new array of words\n2 - find nearest smaller\n3 - find nearest bigger\n4 - find words in range\n\n')
    match(operation):
        case '1':
            words_num = int(input('number of words: '))
            word_len = int(input('length of words: '))
            words = [[random.randint(0,1) for n in range(word_len)] for m in range(words_num)]
            for word in words:
                print(word)
        case '2':
            keyword = input('enter your word: ')
            keyword = keyword.replace(' ','')
            keyword = [int(el) for el in keyword.split(',')]
            nearest = find_nearest_smaller(words, keyword)
            if nearest == []:
                print('no words smaller than this')
            else:
                for word in nearest:
                    print(word)
        case '3':
            keyword = input('enter your word: ')
            keyword = keyword.replace(' ','')
            keyword = [int(el) for el in keyword.split(',')]
            nearest = find_nearest_bigger(words, keyword)
            if nearest == []:
                print('no words bigger than this')
            else:
                for word in nearest:
                    print(word)
        case '4':
            lower_border = input('lower border: ')
            lower_border = lower_border.replace(' ','')
            lower_border = [int(el) for el in lower_border.split(',')]
            top_border = input('top border: ')
            top_border = top_border.replace(' ','')
            top_border = [int(el) for el in top_border.split(',')]
            within = within_range(words, lower_border, top_border)
            if within == []:
                print('no words in this range')
            else:
                for word in within:
                    print(word)