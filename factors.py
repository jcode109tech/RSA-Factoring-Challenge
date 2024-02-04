#!/usr/bin/python3 

import random
import math
import sys
import signal

# cheacks if its prime
def is_prime(number):
    if number < 2:
        return False
    
    for i in range(2, int(number // 2) + 1):
        if number % i == 0:
            return False
        
    return True


# genrate a prime number 
def generate_prime(min_val, max_val):
    prime = random.randint(min_val, max_val)

    while not is_prime(prime):
        prime = random.randint(min_val, max_val)

    return prime

# find mod inverse multiple
def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    
    raise ValueError("mod_inverse does not exist")


# Generate keys
def generate_rsa_keys():
    p, q = generate_prime(1000, 5000), generate_prime(1000, 5000)

    while p == q:
        q = generate_prime(1000, 5000)

    n = p * q
    phi_n = (p-1) * (q-1)

    e = random.randint(3, phi_n - 1)

    while math.gcd(e, phi_n) != 1:
        e = random.randint(3, phi_n - 1)

    d = mod_inverse(e, phi_n)

    return n, e, d


# Pollards algorthim
def pollards_rho(n, max_iterations=1000):
    if n % 2 == 0:
        return [2, n // 2]

    x = random.randint(1, n - 1)
    y = x
    c = random.randint(1, n - 1)
    d = 1

    f = lambda x: (x ** 2 + c) % n

    for _ in range(max_iterations):
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), n)

        if d != 1:
            return [d, n // d]

    # If the loop completes without finding a factor, return n itself
    return [n]


# Optimize 
def factorize(n):
    if is_prime(n):
        return [n]
    
    factors = []
    while not is_prime(n):
        divisor, n = pollards_rho(n)
        factors.extend(factorize(divisor))
    
    factors.append(n)
    return factors

def timeout_handler(signum, frame):
    print("Timeout reached. Exiting.")
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: rsa_factors.py <file>")
        sys.exit(1)

    input_file = sys.argv[1]

    n, e, d = generate_rsa_keys()

    # print("Public Key:", e)
    # print("Private Key:", d)
    # print("n:", n)

    # Set a timeout of 5 seconds
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(5)

    try:
        with open(input_file, 'r') as file:
            for line in file:
                number = int(line.strip())
                factors = factorize(number)
                print('{}'.format(number) + '=' + '*'.join(map(str, factors)))
    except KeyboardInterrupt:
        print("Execution interrupted.")
    finally:
        # Reset the alarm
        signal.alarm(0)

if __name__ == "__main__":
    main()
