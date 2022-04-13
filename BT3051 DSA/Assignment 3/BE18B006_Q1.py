def min_mutations(dna1, dna2):
    '''
    Input: 2 strings dna1 and dna2 containing nucleotide sequences
    Output: a positive integer that denotes the minimum number of edit operations that
    will transform dna1 to dna2. This is the edit distance between dna1 and dna2.
    '''
    # define the insertion and deletion costs
    ins, dele = 2, 1
    
    # define the base cases for the recursive algorithm
    # When the length of the string is 0, it is either a complete insertion or deletion
    if len(dna1) == 0:
        return len(dna2) # entire dna2 is an insertion
    
    elif len(dna2) == 0:
        return len(dna1) # entire dna1 has been deleted
    
    # Recursive call for the calculation of the edit distance
    # The edit distance for s and t can be expressed as the following recurrence relation
    # based on the edit distance between the strings such that the last element is removed for one of them
    # or the last element is removed for both of them and that last element's substitution cost is found.
    return min(min_mutations(dna1[:-1], dna2[:-1]) + delta(dna1[-1], dna2[-1]), min_mutations(dna1 ,dna2[:-1]) + ins, 
               min_mutations(dna1[:-1], dna2) + dele)

# Function for substitution
# If the nucleotides are identical, no substitution cost in incurred.
# If both the nucleotides are unidentical purines or unidentical pyrimidines, the cost is +1
# If one of the nucleotides is purine and the other is pyrimidine, the cost is +3
def delta(si, tj):
    pur, pyr = 'AG', 'CT'

    if si == tj:
        return 0
    elif ((si in pur) and (tj in pur)) or ((si in pyr) and (tj in pyr)):
        return 1
    else:
        return 3

# Test
print(min_mutations('ATGC', 'ATGGG'))
print(min_mutations('TAGTA', 'TGGTA'))