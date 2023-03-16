import math

"""
def is_prime(n):
    
    if n < 2:
        return False
    if 0 in [n % i for i in range(2, n-1,1)]:
        return False
    else:
        return True  

"""
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        print(int(math.sqrt(n)))
        if n % i == 0:
            return False
    return True


print(is_prime(11))