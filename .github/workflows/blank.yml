delim, delit = input().split()
if int(delit) > int(delim):
    print("The integer part of the division: 0")
    print(f"The remainder of the division: {delim}")
else:
    n, m = len(delim), len(delit)
    quotient = []
    remainder = int(delim)
    divisor = int(delit)

    for i in range(n - m + 1): # n - m + 1 раз
        prefix = remainder // (10 ** (n - m - i)) # 4 операции
        digit = prefix // divisor #1 операция
        quotient.append(str(digit))
        remainder -= digit * divisor * (10 ** (n - m - i)) #6 операций
# Всего около (n-m+1)*11 операций, множитель 11 не меняет порядок роста, поэтому О(11(n-m+1)) = O(n-m+1) = O(n-m)<O(n*m)
    print(f"The integer part of the division: {''.join(quotient)}")
    print(f"The remainder of the division: {remainder}")
