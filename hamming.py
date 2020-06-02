from math import ceil, log2
from operator import add
import random
import pandas as pd
from colorama import Fore, Back, Style

# преобразует строку в двоичное число
def stringToBinary (data):
    binary = ''.join ([bin (ord (i))[2:].zfill (8) for i in data])
    binary = list (int (i) for i in binary)
    print (Fore.YELLOW + "[Binary representation of  input data]:\n" + Style.RESET_ALL, *binary, '\n')
    return binary

# вычисляет число контрольных бит
def controlBitsCounter (m):
    return ceil (log2 (m + 1 + ceil (log2 (m + 1)))) 

# вычисляет позицию бита сообщения
def bitPosition (position):
    return (position + ceil (log2 (position + 2 + ceil (log2 (position + 2)))))

# меняет значение бита с 1 на 0 и наоборот
def changeBit (value):  
    return 0 if value == 1 else 1

# добавляет контрольные биты в сообщение
def addControlBits (n, binary):
    controlBitsData = list (int (bit) for bit in '0' * n)
    for j in range (len (binary)):
        controlBitsData[bitPosition (j)] = binary[j]
    return controlBitsData

# генерирует строку длины n с i единицами с i-й позиции через каждые i бит
def bitRow (n, i):
    row = [0] * n
    for position in range (n):
        if ((position + 1) // i)%2 == 1:
            row[position] = 1
    return row

# вычисляет значение заданного контрольного бита
def controlBitValue (extendedData, row):
    rowsMultiplication = list (map (lambda x, y: (x * y), extendedData, row))
    return ((rowsMultiplication.count (1))%2)

# вычисляет значение всех контрольных бит
def findValues (extendedData, k, n):
    values = []
    pd.options.display.max_columns = n
    table = pd.DataFrame ({'data': extendedData})
    table.index = range (1, len (table) + 1)
    for i in range (k):
        row = bitRow (n, 2**i)
        value = controlBitValue (extendedData, row)
        values.append (value)
        table['r%i'%(i)] = row
    table = table.T
    display (table)
    return values

# кодирует сообщение
def encode (binary, k, n):
    extendedData = addControlBits (n, binary)
    print (Fore.YELLOW + "[Data with added control bits]:\n" + Style.RESET_ALL, *extendedData, '\n')

    controlBits = findValues (extendedData, k, n)
    print (Fore.YELLOW + "[Control bits values]:\n" + Style.RESET_ALL, *controlBits, '\n')
    
    for i in range (k):
        extendedData[2**i - 1] = controlBits[i]   
    return extendedData

# генерирует ошибку в кдированном сообщении
def generateError (encodedData, n):
    errorPosition = random.randint (0, n - 1)
    print (Fore.YELLOW + "[Generated error position]:\n" + Style.RESET_ALL, errorPosition + 1, '\n')
    dataWithError = encodedData.copy ()
    dataWithError[errorPosition] = changeBit (encodedData[errorPosition])
    return dataWithError

# определяет позицию ошибочноого бита в сообщении
def findErrorPosition (syndrome):
    syndrome.reverse ()
    position = ''.join (map (str, syndrome))
    return int (position, 2)

# исправляет ошибку в кодированном сообщении
def fixError (dataWithError, k, n):
    syndrome = findValues (dataWithError, k, n)
    print (Fore.YELLOW + "[Syndrome]:\n" + Style.RESET_ALL, *syndrome, '\n')

    errorPosition = findErrorPosition (syndrome) - 1
    print (Fore.YELLOW + "[Detected error position]:\n" + Style.RESET_ALL, errorPosition + 1, '\n')
    
    fixedData = dataWithError.copy ()
    fixedData[errorPosition] = changeBit (dataWithError[errorPosition])
    return fixedData
    
# генерирует и исправляет ошибку
def generateAndFixError (encodedData, k, n):
    dataWithError = generateError (encodedData, n)
    print (Fore.YELLOW + "[Data with error]:\n" + Style.RESET_ALL, *dataWithError, '\n')
    
    fixedData = fixError (dataWithError, k, n)
    print (Fore.YELLOW + "[Fixed data]:\n" + Style.RESET_ALL, *fixedData, '\n')
    
    return fixedData

# преобразует двоичное число в строку
def binaryToString (binary):
    stringBinary = ''.join (map (str, binary))
    return (''.join ([chr (int (stringBinary[i:i + 8], 2)) for i in range (0, len (stringBinary), 8)]))

# декодирует сообщение
def decode (encodedData, k):
    decodedData = encodedData.copy ()
    for j in list (i for i in range(k))[::-1]:
        del decodedData[2**j - 1]
    print (Fore.YELLOW + "[Decoded binary data]:\n" + Style.RESET_ALL, *decodedData, '\n' + Style.RESET_ALL)
    stringBinary = binaryToString (decodedData)
    return stringBinary

print (Fore.YELLOW + "Input your data: " + Style.RESET_ALL)
data = input ()
print ('\n')
binary = stringToBinary (data)

while 1:
    print (Fore.YELLOW + "Do you want to generate an error during encoding? [y/n] " + Style.RESET_ALL)
    toGenerateError = input ()
    if (toGenerateError == 'y' or toGenerateError == 'n'):
        break
print ('\n')
        
m = len (binary) 
print (Fore.YELLOW + "[Length of binary data]:\n" + Style.RESET_ALL, m, '\n')

k = controlBitsCounter (m) 
print (Fore.YELLOW + "[Amount of control symbols]:\n" + Style.RESET_ALL, k, '\n')

n = m + k

encodedData = encode (binary, k, n)
print (Fore.YELLOW + "[Encoded data]:\n" + Style.RESET_ALL, *encodedData, '\n')

if toGenerateError == 'y':
    dataToDecode = generateAndFixError (encodedData, k, n)
else:
    dataToDecode = encodedData.copy ()

decodedData = decode (dataToDecode, k)
print (Fore.YELLOW + "[Decoded data]:\n" + Style.RESET_ALL, decodedData, '\n')
