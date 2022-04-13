def prime_factors(n):
    """
    Input: a number x < 1000000
    Output: a list containing all the prime factors of x in ascending order
    """
    # The ideas used in the below code:
    # 1. There can be atleast one prime factor that would be less than √n in case of n is not a prime number.
    # 2. There can be at most 1 prime factor of n greater than √n.
    # First, I check for 2 as a prime factor and then the odd numbers (using a for loop).
    # Reference for the theory used: https://www.javatpoint.com/python-program-to-print-prime-factor-of-given-number
    t = n # made a copy just to keep n intact
    primefactors = []
    if t % 2 == 0:
        primefactors.append(2)
        while t % 2 == 0:
            t /= 2
    for i in range(3, int(t ** 0.5) + 1, 2):
        if (t % i == 0):
            primefactors.append(i)
            while(t % i == 0):
                t /= i            
    if t > 2:
        primefactors.append(int(t))

    primefactors = sorted(primefactors)
    return primefactors

if __name__ == "__main__":
    fin = open("q4_test.txt")
    n = int(fin.read().splitlines()[0])
    fin.close()

    # Add your code here
    a = prime_factors(n)
    # Final output printed as a list
    print(a)
