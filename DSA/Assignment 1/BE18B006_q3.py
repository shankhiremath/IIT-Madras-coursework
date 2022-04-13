def pascals_triangle(n):
    """
    Input: a positive integer n
    Output: a list containing the first n rows of Pascal's triangle (A list of lists).
    """
    # The main idea used is the following:
    # Row i (starting from 0) has i + 1 elements.
    # Element j (starting from 0) in row i is equal to C(i, j).
    # C(i, 0) is equal to 1 and so is C(i, i) for all i.
    # The remaining C(i, j) = C(i, j-1) * (i-j)/j. This is easily proven by expanding the RHS.
    # I also had the above idea but I used a reference: https://stackoverflow.com/questions/15580291/how-to-efficiently-calculate-a-row-in-pascals-triangle
    
    assert int(n) > 0
    nrows = [[1],]
    for i in range(1, n):
        nextrow = [1]
        for j in range(i - 1):
            nextelem = nextrow[j] * ((i - j) / (j + 1))
            nextrow.append(int(nextelem))
        nextrow.append(1)
        nrows.append(nextrow)
    return nrows

if __name__ == "__main__":
    fin = open("q3_test.txt")
    n = int(fin.read().splitlines()[0])
    fin.close()

    # Add your code here
    a = pascals_triangle(n)
    # The n rows are printed using list comprehension
    [print(*row, sep = ' ') for row in a]
    