def sumToN(n):
    if n <= 1:
        return n
    else:
        return n + sumToN(n - 1)
