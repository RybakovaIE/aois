table_len = 20
alphabet_len = 26
key_index = 1
v_index = 2
h_index = 3
info_index = 4
collision_index = 5

def print_row(row):
    print(str(row[0]).center(3), end='|')
    print(row[key_index].center(14), end='|')
    print(str(row[v_index]).center(5), end='|')
    print(str(row[h_index]).center(6), end='|')
    print(str(row[collision_index]).center(5), end='|')
    print(' ' + row[info_index])

def print_table(table):
    print('\n № |     term     |  V  | h(V) |  C  | definition')
    print('---+--------------+-----+------+-----+-------------------------------------------------------------------')
    for i in range(len(table)):
        print_row(table[i])
    print('---------------------------------------------------------------------------------------------------------')

def calculate_value(key):
    first_letter = ord(key[0])-ord('a')
    second_letter = ord(key[1])-ord('a')
    value = first_letter*alphabet_len + second_letter
    return value

def calculate_address(value):
    address = value%table_len
    return address

def find_empty(table):
    for i in range(len(table)):
        if table[i][key_index] == '':
            return i
        
def find_last(table, address):
    if table[address][collision_index] == '':
        return address
    else:
        return find_last(table, table[address][collision_index])
        
def add(table, key, info):
    value = calculate_value(key)
    address = calculate_address(value)
    if table[address][key_index] == '':
       table[address] = [address, key, value, address, info, '']
    elif table[address][h_index] != address:
        other_key = table[address][key_index]
        other_info = table[address][key_index]
        delete_row(other_key, table)
        table[address] = [address, key, value, address, info, '']
        add(table, other_key, other_info)
    else:
        index = find_empty(table)
        last = find_last(table, address)
        table[last][collision_index] = index
        table[index] = [index, key, value, address, info, '']

def find_row(key, table, address = ''):
    if address == '':
        value = calculate_value(key)
        address = calculate_address(value)
    if table[address][key_index] == key:
        return table[address]
    if table[address][collision_index] != '':
        return find_row(key, table, address=table[address][collision_index])

    return None

def find_previous(table, address):
    for i in range(table_len):
        if table[i][collision_index] == address:
            return i
            
def delete_row(key, table, address=''):
    if address == '':
        value = calculate_value(key)
        address = calculate_address(value)
    if table[address][key_index] == key:
        if table[address][collision_index] == '' and address == table[address][h_index]:
            table[address] = [address,'','','','','']
        elif table[address][collision_index] != '':
            next_index = table[address][collision_index]
            table[address] = table[next_index]
            table[address][0] = address
            table[next_index] = [next_index,'','','','','']
        else:
            prev_index = find_previous(table, address)
            table[prev_index][collision_index] = table[address][collision_index]
            table[address] = [address,'','','','','']
    else:
        delete_row(key, table, address=table[address][collision_index])
        
table = []
for i in range(table_len):
    table.append([i,'','','','',''])
information = open('physics.txt')
lines = information.readlines()
collisions = []
for line in lines:
    key, info = line.split(', ')
    info = info.replace('\n','')
    value = calculate_value(key)
    address = calculate_address(value)
    row = [address, key, value, address, info, '']
    if table[address][key_index] == '':
       table[address] = row
    else:
       collisions.append(row)
for row in collisions:
    add(table, row[key_index], row[info_index])
print_table(table)
while True:  
    opt = input('\n1 - show the table\n2 - add new term\n3 - find a term\n4 - delete a term\n')
    match opt:
        case '1':
            print_table(table)
        case '2':
            key = input('\nterm: ')
            if find_row(key, table) != None:
                print('this term already exists')
            else:
                info = input('definition: ')
                add(table, key, info)
        case '3':
            key = input('\nterm: ')
            term = find_row(key, table)
            if term == None:
                print('term not found')
            else:
                print_table([term])
        case '4':
            key = input('\nterm: ')
            delete_row(key, table)

