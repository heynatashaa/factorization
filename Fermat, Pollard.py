import math 
import random
import time

# Simple factorization
def factorization (N):
    a = 2
    while (N%a != 0 and a <= math.sqrt (N)):
        a += 1
    if (a > math.sqrt (N) ): 
        return N
    else:
        return a

# Fermat factorization
def Fermat (N):
    if (N > pow (2, 64)):
        return -1
    # h is the smallest integer greater than the square root of N
    h = math.ceil (math.sqrt (N))
    while (math.sqrt (h*h - N).is_integer () == False):
        h += 1
    return int (h - math.sqrt (h*h - N))
    
# Pollard's p-1 factorization
def Pollard_p_1 (N): 
    # base and exponent
    a = 2
    i = 2
    # runs until any divider is found
    while (True):
        # a^i mod N
        a = pow (a, i, N)
        # d = GCD (a^i - 1, N)
        d = math.gcd ((a - 1), N)
        # check if divider is found
        if (d > 1):
            return d
            break
        i += 1
    
# Pollard's rho factorization
def Fx (x, N):
    # choosing a random number from 1 to N
    c = random.randint (1, N - 1)
    return ((x*x)%N + c)%N   
def gcd (m, N):
    if (N != 0):
        return math.gcd (N, m%N)
    return m
def PollardRho (N):
    x = 2 
    y = 2
    d = 1
    while (d == 1):
        x = Fx (x, N) 
        y = Fx (y, N) 
        d = gcd (abs (x - y), N)
    if (d != N):
        return d
    
# Updated Pollard's rho factorization    
def updatedPollardRho (N):
    # choosing a random number from 1 to N-1
    x = random.randint (1, N - 2)
    y = 1
    i = 0
    stage = 2
    while (math.gcd (N, abs (x - y)) == 1):
        if (i == stage):
            y = x
            stage *= 2
        x = ((x*x)%N + 1)%N
        i += 1
    return math.gcd (N, abs (x - y))

# N is a number that is analyzed on having dividers
for N in [10001, pow (2, 64) - 1, pow (2, 64) + 1, 234567890876545676537289347638290847567839223674895439583934563289836432097456392643829]:

    print ("\033[1;32mN = %s\033[0m\n"% N)

    factStart = time.time ()
    print ("\033[1;2m\nSimple factorization:\033[0m\nCommon divider = \033[1;36m%d\033[0m\nTime = %f seconds" % (factorization (N), time.time () - factStart))

    f = Fermat (N)
    if (f > 0):
        FermatStart = time.time ()
        print ("\033[1;2m\nFermat:\033[0m\nCommon divider = \033[1;36m%d\033[0m\nTime = %f seconds" % (f, time.time () - FermatStart))
    else:
        print ("\033[1;35m\nFerma's algorithm can't work with numbers > 2^64\033[0m")
        
    Pollard_p_1_Start = time.time ()
    print ("\033[1;2m\nPollard's p-1:\033[0m\nCommon divider = \033[1;36m%d\033[0m\nTime = %f seconds" % (Pollard_p_1 (N), time.time () - Pollard_p_1_Start))
        
    PollardRhoStart = time.time ()
    print ("\033[1;2m\nPollard's rho:\033[0m\nCommon divider = \033[1;36m%d\033[0m\nTime = %f seconds" % (PollardRho (N), time.time () - PollardRhoStart))

    updatedPollardRhoStart = time.time ()
    print ("\033[1;2m\nUpdated Pollard's rho:\033[0m\nCommon divider = \033[1;36m%d\033[0m\nTime = %f seconds" % (updatedPollardRho (N), time.time () - updatedPollardRhoStart))
    
    print ("\n\n------------------------------------------")