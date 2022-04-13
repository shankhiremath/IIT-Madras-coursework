class BinaryNumber():
    """Minimalist binary number class"""
    '''
    Input: a string containing '1's and '0's which represents a binary number
    '''
    def __init__(self, a):
        self.base2 = int(a)
        self.binary_num = [int(x) for x in list(a)]
    
    def base10(self):
        """Finds the numerical value (base 10) of the input"""
        numbase10 = self.base10valonly()
        print(numbase10)
        return numbase10
    
    def base10valonly(self):
        """Finds the numerical value (base 10) of the input"""
        numbase10 = 0
        l = len(self.binary_num)
        powerof2 = 2 ** l
        for i in range(l):
            powerof2 //= 2
            numbase10 += (powerof2) * self.binary_num[i]
        return numbase10
    
    def __str__(self):
        """Prints number in base 2 and base 10 notation to the screen with the base of the number subscripted"""
        base10val = self.base10valonly()
        return (f'{self.base2}' + u'\u2082 ' + f'{base10val}' + u'\u2081\u2080')

# TEST:
# testbinary = BinaryNumber('101001')
# print(testbinary)
# Expected output is 101001₂ 41₁₀