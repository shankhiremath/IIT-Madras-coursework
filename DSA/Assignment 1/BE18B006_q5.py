from string import whitespace as w
def decoder(encoded, n):
    """
    Input: the encoded text as a string and the shift for Caesar's cipher
    Output: the decoded text as a string
    """
    # Every character in the string is parsed. If a character is a lower/upper case alphabet,
    # its ASCII code number is calculated using the ord() function and the correct index of
    # the required character is calculated. Next, the chr() function is used to obtain the
    # character from the alphabet index and the character is added to the decoded string.
    # If a character is whitespace, it is added to the output as is.
    # Reference 1: https://www.w3schools.com/python/ref_func_ord.asp
    # Reference 2: https://www.programiz.com/python-programming/methods/built-in/chr

    out = ''
    for i in range(len(encoded)):
        if encoded[i].islower():
            lowerasciival = ord(encoded[i]) - 96 + n
            out += chr(96 + (lowerasciival % 26))
        elif encoded[i].isupper():
            upperasciival = ord(encoded[i]) - 64 + n
            out += chr(64 + (upperasciival % 26))
        elif encoded[i] in w:
            out += encoded[i]

    return out


if __name__ == "__main__":
    fin = open("q5_test.txt")
    data = fin.read().splitlines()
    fin.close()

    data[1] = int(data[1])
    text, n = data

    # Add your code here
    decodedstring = decoder(text, n)
    # print statement
    print(decodedstring)