class CliArgs:
    def __init__(self, args):
        if (args == None):
            raise RuntimeError("'args' was None. Make sure you provide arguments")
        arg_len = len(args)
        if (arg_len < 5):
            raise RuntimeError("Did not provide enough arguments. Only %s were provided." % arg_len)
        try:
            self.b = int(args[1])
            self.m = int(args[2])
            self.x = int(args[3])
            self.i = int(args[4])
        except ValueError as v:
            raise ValueError("Provided invalid arguments. Ensure that they are integers: %s" % args)

    def cli_args(self):
        """ Return arguments given to command line in expected order.
        """
        return self.b, self.m, self.x, self.i

    def __str__(self):
        return "b: %s; m: %s; x: %s; i: %s" % self.cli_args()


def is_prime(n):
    if n == 0 or n == 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            print("%s was not prime (divisible by %s)" % (n, i))
            return False
    print("%s is prime" % (n))
    return True


class RepSeq:
    def __init__(self, mod, base=10):
        self.base = base
        self.mod = mod

    def gen_seq(self):
        ord_b = self.order_of()
        rem = []
        pow = []
        for i in range(2 * ord_b):
            rem.append((self.base ** i) % self.mod)
            pow.append(self.base ** i)
        return rem, pow

    def seg_and_seq(self):
        """ Returns the initial segment and repeating sequence for mod using base @base.
        """
        # For now, only worry about prime moduli

    def order_of(self):
        if is_prime(self.mod):
            return self.mod - 1
        raise RuntimeError("Only works for testing modulo a prime number")


def factors_of_n(n, incl_n=False):
    factors = []
    if not n == 1 and incl_n:
        factors.append(n)
    for i in range(2, n):
        if n % i == 0:
            factors.append(i)
    return factors


def gcd_is_1(n, m):
    return common_factors(n, m) == set()


def common_factors(n, m, incl_n=True):
    return set(factors_of_n(n, incl_n=incl_n)).intersection(set(factors_of_n(m, incl_n=incl_n)))

def euler_totient(n):
    if n == 0:
        return 0
    n_totatives = 1 #Accounting for 1
    for i in range(2,n):
        if gcd_is_1(n,i):
            n_totatives += 1
    return n_totatives


if __name__ == "__main__":
    print("Testing Euler totient function")
    for i in range(10):
        print("euler_totient(%s) = %s" % (i, euler_totient(i)))
