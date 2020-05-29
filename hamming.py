from math import ceil, log2
from operator import add
import random
import pandas as pd

# преобразует строку в двоичное число
def stringToBinary (data):
    binary = ''.join ([bin (ord (i))[2:].zfill (8) for i in data])
    binary = list (int (i) for i in binary)
    print ("Binary representation of input data:\n", *binary, '\n')
    return binary

# вычисляет число контрольных бит
def controlBitsCounter (m):
    return ceil (log2 (m + 1 + ceil (log2 (m + 1)))) 

# вычисляет позицию контрольного бита
def bitPosition (position):
    return (position + ceil (log2 (position + 2 + ceil (log2 (position + 2)))))

# меняет значение бита с 1 на 0 и наоборот
def changeBit (value):  
    return 0 if value == 1 else 1

# добавляет контроольные биты в сообщение
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

# выполняет кодирование сообщения
def encode (binary, k, n):
    extendedData = addControlBits (n, binary)
    print ("Data with added control bits:\n", *extendedData, '\n')

    controlBits = findValues (extendedData, k, n)
    print ("Control bits values:\n", *controlBits, '\n')
    
    for i in range (k):
        extendedData[2**i - 1] = controlBits[i]   
    return extendedData

# генерирует ошибку в кдированном сообщении
def generateError (encodedData, n):
    errorPosition = random.randint (0, n - 1)
    print ("Generated error position: ", errorPosition + 1, '\n')
    dataWithError = encodedData.copy ()
    dataWithError[errorPosition] = changeBit (encodedData[errorPosition])
    return dataWithError

# определяет позицию ошибочноого бита в сообщении
def findErrorPosition (syndrome):
    syndrome.reverse ()
    position = ''.join (map (str, syndrome))
    return int (position, 2)

# исправляет ошибку в кдированном сообщении
def fixError (dataWithError, k, n):
    syndrome = findValues (dataWithError, k, n)
    print ("Syndrome:\n", *syndrome, '\n')

    errorPosition = findErrorPosition (syndrome) - 1
    print ("Detected error position: ", errorPosition + 1, '\n')
    
    fixedData = dataWithError.copy ()
    fixedData[errorPosition] = changeBit (dataWithError[errorPosition])
    return fixedData
    
# генерирует и исправляет ошибку
def generateAndFixError (encodedData, k, n):
    dataWithError = generateError (encodedData, n)
    print ("Data with error:\n", *dataWithError, '\n')
    
    fixedData = fixError (dataWithError, k, n)
    print ("Fixed data:\n", *fixedData, '\n')
    
    return fixedData

# преобразует двоичное число в строку
def binaryToString (binary):
    stringBinary = ''.join (map (str, binary))
    return (''.join ([chr (int (stringBinary[i:i + 8], 2)) for i in range (0, len (stringBinary), 8)]))

# выполняет декодирование
def decode (encodedData, k):
    decodedData = encodedData.copy ()
    for j in list (i for i in range(k))[::-1]:
        del decodedData[2**j - 1]
    print ("Decoded binary message:\n", *decodedData, '\n')
    stringBinary = binaryToString (decodedData)
    return stringBinary


data = input ("Input your data: ")
print ('\n')
binary = stringToBinary (data)

while 1:
    toGenerateError = input ("Do you want to generate an error during encoding? [y/n] ")
    if (toGenerateError  == 'y' or toGenerateError == 'n'):
        break
print ('\n')
        
m = len (binary) 
print ("Length of binary data: ", m, '\n')

k = controlBitsCounter (m) 
print ("Amount of control symbols: ", k, '\n')

n = m + k

encodedData = encode (binary, k, n)
print ("Encoded message:\n", *encodedData, '\n')

if toGenerateError == 'y':
    dataToDecode = generateAndFixError (encodedData, k, n)
else:
    dataToDecode = encodedData.copy ()

decodedData = decode (dataToDecode, k)
print ("Decoded message: ", decodedData, '\n')
