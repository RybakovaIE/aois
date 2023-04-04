def binary(num_dec):
    i = 6
    bits_num = 8
    num_bin = [0 for i in range(8)]
    if num_dec < 0:
        num_bin[0] = 1
        num_dec = -num_dec
    while i > -1:
        if num_dec >= 2**i:
            num_bin[bits_num-i-1] = 1
            num_dec = num_dec - 2**i
        i = i - 1
    return num_bin

def reverse(num_dec):
    num_bin = binary(num_dec)
    return switch(num_bin)

def switch(bin_num):
    reversed = [0 for i in range(len(bin_num))]
    reversed[0] = bin_num[0]
    i = 1
    while i < len(bin_num):
        if bin_num[i] == 0:
            reversed[i] = 1
        else:
            reversed[i] = 0
        i = i + 1
    return reversed

def plusone(number):
    if number >= 0:
        return binary(number)
    else:
        return plus_one(reverse(number))
    
def plus_one(bin_num):
    one = [0 for i in range(len(bin_num))]
    one[len(bin_num)-1] = 1
    return summ(bin_num, one)

def add(num_1, num_2, flag):
    sum = [0 for i in range(len(num_1))]
    i = 7
    while i > -1:
        if num_1[i]+num_2[i] < 2:
            sum[i] = num_1[i]+num_2[i]
        else:
            sum[i] = num_1[i]+num_2[i]-2
            if i > 0:
                num_1[i-1] = num_1[i-1]+1
            elif flag:
                sum = plus_one(sum)
        i = i - 1
    return sum

def decimal(num_bin):
    i = 1
    num_dec = 0
    while i < 8:
        num_dec = num_dec + (2**(7-i))*num_bin[i]
        i = i + 1
    if num_bin[0] == 1:
        num_dec = -num_dec
    return num_dec

def to_decimal(num_bin):
    i = 0
    num_dec = 0
    while i < len(num_bin):
        num_dec = num_dec + (2**(len(num_bin)-i-1))*num_bin[i]
        i+=1
    return num_dec

def to_binary(number):
    arr = []
    while number > 0:
        arr.insert(0,number%2)
        number = number//2
    return arr    

def multiply(num_1,num_2):
    for i in range(len(num_1)-1):
        num_2.append(0)
    num_2.insert(0,0)
    res = [0 for i in range(len(num_2))]
    for i in range(len(num_1)):
        if num_1[i] == 1:
            res = summ(res,shift(num_2,i))
    return res

def devide(num_1,num_2):
    if len(num_1) >= len(num_2) and compare(num_1,num_2):
        count = 1
        while len(num_1) > len(num_2):
            num_2.append(0)
            count+=1
        int_part = []
        for i in range(count):
            if compare(num_1,num_2):
                int_part.append(1)
                num_1 = reduct(num_1,num_2)
            else:
                int_part.append(0)
            if i != count-1:
                num_2.pop(-1)  
    else:
        int_part = [0]
    fract_part = fract_devide(num_1, num_2)
    return int_part, fract_part

def fract_devide(num_1, num_2):
    fract_part = []
    for i in range(30):
        num_1.append(0)
        if compare(num_1,num_2):
            fract_part.append(1)
            num_1 = reduct(num_1,num_2)
        else:
            fract_part.append(0)
    return fract_part

def round_num(number):
    plus = False
    digits_number = 5
    base = 10
    number = str(number)
    dot = number.find('.')
    if dot == -1:
        simbols_number = digits_number
    else:
        simbols_number = digits_number + 1
    if len(number) <= simbols_number:
        return float(number)
    if int(number[simbols_number]) >= 5:
        plus = True
    number = float(number[:simbols_number])
    if plus:
        if dot != -1:
            e = dot - digits_number
        else:
            e = 0
        number = number + base**e
    return number


def floating(number):
    parts = number.split('.')
    intpart = int(parts[0])
    fractpart = float('0.' + parts[1])
    negative_power = 0.5
    if number[0] == '-':
        sign = 1
        intpart = -intpart
    else:
        sign = 0
    if intpart != 0:
        arr = to_binary(intpart)
        e = len(arr) - 1
    else:
        arr = []
        e = -1
        while fractpart < negative_power:
            e = e - 1
            negative_power = negative_power/2
    return floating2(arr, fractpart, e, sign, negative_power)

def floating2(arr, fractpart, e, sign, negative_power):
    exp_shift = 127
    mant_len = 23
    while len(arr) < mant_len+1:
        if fractpart >= negative_power:
            arr.append(1)
            fractpart = fractpart - negative_power
        else:
            arr.append(0)
        negative_power = negative_power/2
    arr.pop(0)
    e = exp_shift + e
    i = 0
    while i < 8:
        if e >= 2**(7-i):
            arr.insert(i,1)
            e = e - 2**(7-i)
        else:
            arr.insert(i,0)
        i = i + 1
    arr.insert(0,sign)
    return arr


def float_to_dec(bin):
    i = 1
    e = 0
    m = 0
    mant_shift = 127
    mant_bits = 23
    total_bits = 32
    exp_bits = 8
    while i < 9:
        e = e + (2**(exp_bits-i))*bin[i]
        i = i + 1
    while i < 32:
        m = m + (2**(total_bits-i-1))*bin[i]
        i = i + 1
    dec = 2**(e-mant_shift)*(1+m/2**mant_bits)
    if bin[0] == 1:
        dec = -dec
    return dec

def get_exp(float_num):
    exp = []
    exp_end = 9
    i = 1
    while i < exp_end:
        exp.append(float_num[i])
        i+=1
    return exp

def get_mantissa(float_num):
    mantissa = []
    exp_end = 9
    total_bits = 32
    while exp_end < total_bits:
        mantissa.append(float_num[exp_end])
        exp_end+=1
    return mantissa

def shift(bin_num, shift_num):
    res = []
    i = 0
    while i < shift_num:
        res.append(0)
        i+=1
    while i < len(bin_num):
        res.append(bin_num[i-shift_num])
        i+=1
    return res
    
def summ(num_1, num_2):
    i = len(num_1) - 1
    res = []
    while i > -1:
        if num_1[i]+num_2[i] < 2:
            res.insert(0, num_1[i]+num_2[i])
        else:
            res.insert(0, num_1[i]+num_2[i]-2)
            if i > 0:
                num_1[i-1] = num_1[i-1]+1
        i = i - 1
    return res

def reduct(num_1, num_2):
    num1 = num_1.copy()
    num2 = num_2.copy()
    while len(num2) < len(num1):
        num2.insert(0,0)
    num1.insert(0,0)
    num2.insert(0,1)
    num2 = plus_one(switch(num2))
    res = summ(num1,num2)
    res.pop(0)
    return res

def compare(num_1,num_2):
    i = 0
    num2 = num_2.copy()
    if len(num_1) < len(num_2):
        return False
    while len(num_1) > len (num2):
        num2.insert(0,0)
    while i < len(num_1):
        if num_1[i] > num2[i]:
            return True
        elif num_1[i] == num2[i]:
            i+=1
        else:
            return False
    return True

def mantis_sum(mantissa1, mantissa2, sign1, sign2):
    if sign1 == 1:
        mantissa1 = plus_one(switch(mantissa1))
        mantissa1[0] = 1
    if sign2 == 1:
        mantissa2 = plus_one(switch(mantissa2))
        mantissa2[0] = 1
    res_m = summ(mantissa1, mantissa2)
    if res_m[0] == 1:
        res_m = plus_one(switch(res_m))
    return res_m 

def float_sum(num_1, num_2):
    exp1 = to_decimal(get_exp(num_1))
    exp2 = to_decimal(get_exp(num_2))
    mantissa1 = [0, 0, 1] + get_mantissa(num_1)
    mantissa2 = [0, 0, 1] + get_mantissa(num_2)
    diff = abs(exp1-exp2)
    res_e = get_exp(num_1)
    if diff != 0:
        if exp1 > exp2:
            mantissa2 = shift(mantissa2, diff)
        else:
            res_e = get_exp(num_2)
            mantissa1 = shift(mantissa1, diff)
    res_m = mantis_sum(mantissa1, mantissa2, num_1[0], num_2[0])
    sign = 0
    if res_m[0] == 1:
        sign = 1
    res_m.pop(0)
    if res_m[0] == 1:
        res_m = shift(res_m, 1)
        res_e = plus_one(res_e)
    elif res_m[1] == 0:
        while res_m[1] == 0:
            res_m.pop(0)
            res_m.append(0)
            res_e = reduct(res_e, [1])
    res_m.pop(0)
    res_m.pop(0)
    return [sign] + res_e + res_m
    
    
while True:  
    opt = input('выберите операцию\n1 - сложение\n2 - умножение\n3 - деление\n4 - сложение с плавающей точкой\n')
    match opt:
        case '1':
            a = int(input('input а: '))
            b = int(input('input b: '))
            if a >= 0 and b >= 0:
                a = binary(a)
                b = binary(b)
                print('a: ' + str(a))
                print('b: ' + str(b))
                res = add(a, b, True)
            elif a < 0 and b < 0:
                a = reverse(a)
                b = reverse(b)
                print('a:   ' + str(a))
                print('b:   ' + str(b))
                res = add(a, b, True)
                res = switch(res)
            else:
                c = a + b
                a = plusone(a)
                b = plusone(b)
                print('a: ' + str(a))
                print('b: ' + str(b))
                res = add(a, b, False)
                if c < 0:
                    res = plus_one(switch(res))
            print('res: ' + str(res))
            print('decimal res: ' + str(decimal(res)))
        case '2':
            a = int(input('input а: '))
            b = int(input('input b: '))
            sign = 0
            if a < 0:
                sign += 1
                a = -a
            if b < 0:
                sign +=1
                b = -b
            a = to_binary(a)
            b = to_binary(b)
            print('a:   ' + ''.join(str(el) for el in a))
            print('b:   ' + ''.join(str(el) for el in b))
            res = multiply(a,b)
            print('res: ' + ''.join(str(el) for el in res))
            res = to_decimal(res)
            if sign == 1:
                res = -res
            print('decimal res: ' + str(res))
        case '3':
            a = int(input('input а: '))
            b = int(input('input b: '))
            sign = 0
            if a < 0:
                sign += 1
                a = -a
            if b < 0:
                sign +=1
                b = -b
            a = to_binary(a)
            b = to_binary(b)
            print('a:   ' + ''.join(str(el) for el in a))
            print('b:   ' + ''.join(str(el) for el in b))
            intpart, fractpart = devide(a,b)
            res = to_decimal(intpart) + to_decimal(fractpart)/2**30
            str_res = ''.join(str(el) for el in intpart) + '.' +''.join(str(el) for el in fractpart)
            print('res: ' + str_res)
            res = round_num(res)
            if sign == 1:
                res = -res
            print('decimal res: ' + str(res))
        case '4':
            a = input('input а: ')
            b = input('input b: ')
            a = floating(a)
            b = floating(b)
            print('a:    s= '+str(a[0]) + '  e= '+''.join(str(a[i]) for i in range(1,9))
                  +'  m= '+''.join(str(a[i]) for i in range(10,32)))
            print('b:    s= '+str(b[0]) + '  e= '+''.join(str(b[i]) for i in range(1,9))
                  +'  m= '+''.join(str(b[i]) for i in range(10,32)))
            res = float_sum(a, b)
            print('res:  s= '+str(res[0]) + '  e= '+''.join(str(res[i]) for i in range(1,9))
                  +'  m= '+''.join(str(res[i]) for i in range(10,32)))
            print('decimal res: ' + str(float_to_dec(res)))
