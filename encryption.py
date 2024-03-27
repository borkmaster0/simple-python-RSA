import math
import random

def factor(num: int): ## Factor
    factors = []
    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)
    return factors

def isPrime(num: int): ## Prime number detection
    factors = factor(num)
    if num <= 1:
        return False
    elif factors[0] == 1 and factors[-1] == num and len(factors) == 2:
        return True
    else:
        return False

def nextPrimeTo(num: int): ## Find the next prime number to a number
    counter = 1
    while not(isPrime(num + counter)):
        out = num + counter
        counter += 1
    out = num + counter
    return out

def randomPrime(low: int, high: int): ## Get a random prime number between the bounds
    list = [1]
    while not(list[-1] > high):
        list.append(nextPrimeTo(list[-1]))
        print(f'Generating primes... {list[-1]}/{high}')
    
    return list[random.randint(0, len(list))]

def gcf(num1: int, num2: int): ## Get the GCF of 2 numbers
    if num1 > num2:
        x = num2
    else:
        x = num1
    while x > 1:
        if num1 % x == 0 and num2 % x == 0:
            break
        x -= 1
    return x

def lcm(num1: int, num2: int): ## Get the LCM of 2 numbers
    return (num1 * num2) / gcf(num1, num2)

def carmichael(num1: int, num2: int): ## Get the Carmichael value of 2 numbers
    return lcm(num1 - 1, num2 - 1)

def isCoprime(num1: int, num2: int): ## Check if 2 numbers are co-prime
    return gcf(num1, num2) == 1

def nextCoprimeTo(num: int, num2: int): ## Get the next co-prime number to a value
    counter = 1
    while not(isCoprime(num + counter, num2)):
        out = num + counter
        counter += 1
    out = num + counter
    return out

def generateCoprime(max: int, num: int): ## Geneerate a list of co-prime values from 1 to the max, checking against the number
    a = [2]
    while not(a[-1] > max):
        a.append(nextCoprimeTo(a[-1], num))
        print(f'Generating co-primes... {a[-1]}/{max}')
    return a

def modInverse(a: int, m: int): ## Get the modular inverse of 2 numbers
    m0 = m
    x = 1
    y = 0
    if m == 1:
        return 0
    while a > 1:
        q = math.floor(a/m)
        t = m
        m = a % m
        a = t
        t = y
        y = x - (q * y)
        x = t
    if x < 0:
        x += m0
    return x

def rsaKey(low: int, high: int): ## Generate the RSA key
    p = randomPrime(1, low)
    q = randomPrime(low, high)
    n = p * q
    carmichaelValue = carmichael(p, q)
    coprimes = generateCoprime(carmichaelValue, carmichaelValue)
    coprimes = coprimes[random.randint(0, len(coprimes))]
    modInv = modInverse(coprimes, carmichaelValue)
    return [['public', n, coprimes], ['private', n, modInv]]

def encrypt(text: str, key: list): ## Encrypt a text with a public key
    splitText = list(text)
    a = []
    b = []
    for letter in splitText:
        a.append(ord(letter))
    for unicode in a:
        b.append(str((unicode ** key[1]) % key[0]))
    return ' '.join(b)

def decrypt(entext: str, privkey: list): ## Decrypt a text with a private key
    splitText = entext.split()
    a = []
    b = []
    c = []
    for word in splitText:
        c.append(int(word))
    for number in c:
        a.append((number ** privkey[1]) % privkey[0])
    for number in a:
        b.append(chr(number))
    return ''.join(b)

def keyCheck(public: list, private: list): ## Check if the public and private keys are a match (e.g. Text that can be encrypted and decrypted while staying the same)
    a = 'Hello, world!'
    return a == decrypt(encrypt(a, public), private)

def keyBruteforce(start: int, batchSize: int, pubKey: list): ## Check validity of key pairs to bruteforce the private key
    if batchSize < 5:
        return ValueError("Batch size must be greater than or equal to 5")
    a = start
    b = []
    while any(b) == False:
        b = []
        for i in range(a, a + batchSize - 1):
            try:
                print(f'{i}: {decrypt(encrypt('Hello, world!', pubKey), [pubKey[0], i])}')
            except:
                None
            b.append(keyCheck(pubKey, [pubKey[0], i]))
        a += batchSize
    return ['private', pubKey[0], a + b.index(True) - batchSize]
