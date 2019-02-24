def print_tbl(a, b, mod, base=10):
    l_delim = "    \t\t\t\t"
    print("%s^n%s| mod %s" % (base, l_delim, mod))
    for c, d in zip(a, b):
        print("%s%s| %s" % (c, l_delim, d))


def pwrs_of(a, b):
    return [a ** c for c in range(b)]


def mod(n, arr, base=10):
    for a in arr:
        print("%s mod %s is %s" % (a, n, (a % n)))
    return [m % n for m in arr]