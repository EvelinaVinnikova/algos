def long_division(delimoe: int, delitel: int): # delimoe - n, delit - m
    assert delitel > 0, "Error: Division by zero"
    if delimoe < delitel:
        return 0, delimoe

    whole_part = 0
    remainder = 0

    power = 1
    while (delitel << power) <= delimoe: # n-m operations
        power += 1

    for i in reversed(range(power + 1)): #n-m operations
        shifted = delitel << i
        if shifted <= delimoe:
            delimoe -= shifted
            whole_part += (1 << i)
        # total operations: 1 to 4

    return whole_part, delimoe

# In total k*(n-m) operations, if k is comparable to n or m then we have: kn- km = c1*n*m - c2*n*m = (c1-c2)*n*m
# Worst case: 5 * (n-1) operations
# Best case: (delitel and delimoe are equal) 3 operations

q, r = long_division(200, 66)
assert q == 3 and r == 2; "Error: wrong answer"

q, r = long_division(123459532930350, 24591)
assert q == 5020516974 and r == 22716; "Error: wrong answer"

q, r = long_division(123459532930350, 123459302113484343)
assert q == 0 and r == 123459532930350; "Error: wrong answer"

q, r = long_division(20, 12)
assert q == 1 and r == 8; "Error: wrong answer"
