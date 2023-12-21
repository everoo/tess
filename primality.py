from math import sqrt, pow
import re

def findPrime(primes, n, i):
    while n % i == 0:
        if i in primes:
            primes[i] += 1
        else:
            primes[i] = 1
        n //= i
    return primes, n

def primeFactors(n):
    if n == 1:
        return {2: 0}
    if n == 0:
        return {2: '-inf'}
    primes, n = findPrime({}, n, 2)
    for i in range(3, int(sqrt(n))+1, 2):
        primes, n = findPrime(primes, n, i)             
    if n > 2:
        primes[n] = 1
    return primes

def primality(n):
    return sum(primeFactors(n).values())
          
# n = 2*3*5*7*7
# print(primality(n))

test = '2^4 * 3^6 * 5^4'

def getNum(strPrime):
    strs = strPrime.replace(' ', '').split('*')
    n = 1
    for chunk in strs:
        try:
            b, e = chunk.split('^')
            exp = 1
            if '(' in e:
                e = e[1:-1]
                den, div = e.split('/')
                exp = int(den)/int(div)
            else:
                exp = int(e)
            n *= pow(int(b), exp)
        except:
            n *= int(chunk)
    return n

def getComplexNum(strPrime):
    strs = strPrime.split('+')
    total = 0
    for s in strs:
        total += getNum(s)
    return total

# print(getComplexNum('1+5^(1/2)'))


# def strPrimality(s):
#     n = getNum(s)
#     return primality(n)

# print(strPrimality(test))

# a/b = a*1/b
# p(a/b) = p(a) - p(b)

#p(5^(1/2)/2) = p(5^(1/2)*1/2) = p(5^(1/2)) + p(1/2)
#p(1/2) = p(1) + p(1/2)

#p(3/2) = p(3) + p(1/2)
#p(1/2+5^(1/2)/2)

#p(2^-1 + 5^(1/2) * 2^-1)
#p(2^-1 * (1 + 5^(1/2)) )
#p(2^-1) + p(1+5^(1/2))
#p(2^-1) + p(2^0+5^1/2)
#p(2^-1) + p(5^0+5^1/2)

#a^b+a^c
#c = log(-a^b)/log(a)
#1/2 = log(-5^0)/log(5) = 1.95i

#2^0=5^0
#sqrt(a*b) = sqrt(a) + sqrt(b)
#(a^b)^c = a^(b*c)

#p(1+5^(1/2)) = 1.5 assuming phi = 0.5

#p(prime) = 1 p(prime^-1) = -1
#so a fraction of primes will always = 0
#thus p(1+prime/prime) = 1+p(prime/prime)
# our equation is p(1+n/prime)
# which I think still works because that becomes
# p((prime+n)/prime) = p((prime+n)*prime^-1) = 1+p(n)-1 = p(n)
# p(1+n/prime) = p(n) = p((n+prime)/prime)
# now do it with p(1/2+5^0.5/2)
# p((1+n)/2) = p(1+n)-p(2)
# p(1+n/prime^0)
# would this equal p((prime^0+n)/prime^0) and can that be proven to equal p(n)

#p(7^2) = 2
#p(4) = 2
#p(4^(1/2)) = 1
#p(88^(1/2)) = 4
#p(36) = 4
#p(n^(1/2)) = p(n)/2

#example
#p(50^1/2) = p(2^1/2*5^1/2*5^1/2) = 3^1/2? fairly certain its 1.5
#p(5^0+5^1+5^2) = p(31) = 1
#p(1+3^8+7^2) = p(6611) = 2

for n in range(30):
    print(primality(1+5**n))
