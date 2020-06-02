import numpy as np
import random
from colorama import Fore, Style

# меняет значение бита с 1 на 0 и наоборот
def changeBit (value):  
    return 0 if value == 1 else 1

# определяет длины блоков, на которые разделяется сообщение, и число контрольных бит  для каждого блока
def howToDivideData (H):
    controlBitsCounter = np.shape (H)[0]
    blockLength = np.shape (H)[1]
    return controlBitsCounter, blockLength
    
# делит сообщение на блоки
def splitIntoBlocks (data, n):
    blocks = []
    for i in range(0, len (data), n):
        blocks.append (data[i:i + n])
    if (len (data)%n != 0):
        blocks[len (blocks) - 1] += [0] * (n - len (blocks[len (blocks) - 1]))
    return blocks

# преобразует строку в двоичное число
def stringToBinary (data):
    binary = ''.join ([bin (ord (i))[2:].zfill (8) for i in data])
    binary = list (int (i) for i in binary)
    print (Fore.YELLOW + "[Binary representation of  input data]:\n" + Style.RESET_ALL, *binary, '\n')
    return binary

# преобразует двоичное число в строку
def binaryToString (binary):
    stringBinary = ''.join (map (str, binary))
    return (''.join ([chr (int (stringBinary[i:i + 8], 2)) for i in range (0, len (stringBinary), 8)]))

# кодирует один блок
def encodeBlock (H, block):
    block = np.array (block)
    controlBits = block @ H.T % 2
    extendedBlock = list (np.concatenate ([block.astype (int), controlBits.astype (int)]))
    return extendedBlock

# генерирует ошибку в кдированном сообщении
def generateError (encodedData):
    n = len (encodedData)
    errorPosition = 3
    errorPosition = random.randint (0, n - 1)
    print (Fore.YELLOW + "[Generated error position]:\n" + Style.RESET_ALL, errorPosition + 1, '\n')
    dataWithError = encodedData.copy ()
    dataWithError[errorPosition] = changeBit (encodedData[errorPosition])
    return dataWithError

# декодирует один блок
def decodeBlock (H, block, controlBitsCounter, blockLength, iterations, blockNumber):
    valueBitsAmount = np.zeros (blockLength)
    for row in H:
        valueBitsAmount += row

    controlBits = np.array (block[-controlBitsCounter:])
    block = np.array (block[:-controlBitsCounter])

    errorIsFound = False
    changedBits = False
    for iteration in range (iterations):
        newControlBits = block @ H.T % 2
        print (Fore.CYAN + "[BLOCK", blockNumber + 1, "-", iteration + 1, "DECODE ITERATION]" + Style.RESET_ALL,
               Fore.YELLOW + "\nBlock:\n" + Style.RESET_ALL, *block,
               Fore.YELLOW + "\nControl bits:\n" + Style.RESET_ALL, *controlBits,
               Fore.YELLOW + "\nNew control bits:\n" + Style.RESET_ALL, *newControlBits, '\n')

        falseBitsPostitions = []
        for i in range (len (controlBits)):
            if controlBits[i] != newControlBits[i]:
                errorIsFound = True
                falseBitsPostitions.append(i)

        if len (falseBitsPostitions) == 0:
            break
        else:
            print (Fore.RED + "[Detected wrong control bits positions]:\n" + Style.RESET_ALL, *[(i + 1) for i in falseBitsPostitions], '\n')

        newValueBitsAmount = np.zeros (blockLength)
        for position in falseBitsPostitions:
            newValueBitsAmount += H[position]
        print (Fore.YELLOW + "[Amount of original value bits]:\n" + Style.RESET_ALL, valueBitsAmount.astype (int))
        print (Fore.YELLOW + "[Amount of new value bits]:\n" + Style.RESET_ALL, newValueBitsAmount.astype (int), '\n')

        for i in range (len (newValueBitsAmount)):
            if (newValueBitsAmount[i] == valueBitsAmount[i]):
                print (Fore.YELLOW + "[Changing bit in a position]:\n" + Style.RESET_ALL, i + 1, '\n')
                block[i] = changeBit (block[i])
                changedBits = True
        if not changedBits:
            break
        
    if not errorIsFound:
        print (Fore.GREEN + "[No errors detected in this block]\n" + Style.RESET_ALL, '\n')
    else:
        if changedBits:
            print (Fore.GREEN + "[Error found and fixed in this block]\n" + Style.RESET_ALL, '\n')
        else:
            print (Fore.GREEN + "[Error occured among control bits]\n" + Style.RESET_ALL)
    return list (block)

# кодирует сообщение
def encode (H, data):
    controlBitsCounter, blockLength = howToDivideData (H)
    blocks = splitIntoBlocks (stringToBinary (data), blockLength)
    encodedData = []
    for block in blocks:
        encodedData += encodeBlock (H, block)
    return encodedData

# декодирует сообщение
def decode (H, encodedData, iterations):
    controlBitsCounter, blockLength = howToDivideData (H)
    blocks = list (splitIntoBlocks (encodedData, blockLength + controlBitsCounter))
    decodedData = []
    for i in range (len (blocks)):
        decodedData += decodeBlock (H, blocks[i], controlBitsCounter, blockLength, iterations, i)
    decodedData = binaryToString (decodedData)
    return decodedData

# матрица Галлагера
HG = np.array ([
    [1,1,1,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,1,1,1],
    [1,0,1,0,0,1,0,0,0,1,0,0],
    [0,1,0,0,0,0,1,1,0,0,0,1],
    [0,0,0,1,1,0,0,0,1,0,1,0],
    [1,0,0,1,0,0,1,0,0,1,0,0],
    [0,1,0,0,0,1,0,1,0,0,1,0],
    [0,0,1,0,1,0,0,0,1,0,0,1],
])

print (Fore.YELLOW + "Input your data: " + Style.RESET_ALL)
data = input ()
print ('\n')

encodedData = encode (HG, data)
print (Fore.YELLOW + "[Encoded data]:\n" + Style.RESET_ALL, *encodedData, '\n')

print (Fore.YELLOW + "Choose the  amount of errors you want to generate: " + Style.RESET_ALL)
errorsAmount = input ()
print ('\n')

dataWithError = encodedData. copy ()
for i  in range (int (errorsAmount)):
    dataWithError = generateError (dataWithError)
    print (Fore.YELLOW + "[Data with error]:\n" + Style.RESET_ALL, *dataWithError, '\n')

print (Fore.YELLOW + "Choose the  amount of decode iterations per block: " + Style.RESET_ALL)
iterations = input ()
print ('\n')

decodedData = decode (HG, dataWithError, int (iterations))
print (Fore.YELLOW + "[Decoded data]:\n" + Style.RESET_ALL, decodedData, '\n')