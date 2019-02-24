PRIMES = None


def is_prime(n):
    n = int(n)
    if n == 0 or n == 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def ld_primes(n=1000):
    primes = []
    i = 1
    j = 2
    while i < n:
        if is_prime(j):
            primes += [j]
            i += 1
        j += 1
    return primes


PRIMES = ld_primes()


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
    n_totatives = 1  # Accounting for 1
    for i in range(2, n):
        if gcd_is_1(n, i):
            n_totatives += 1
    return n_totatives


def prime_factorization(n):
    pf = []
    if is_prime(n):
        return pf + [n]
    for p in PRIMES:
        if p > n:
            return pf
        if n % p == 0:
            pf += [p]
            return pf + prime_factorization(int(n / p))


class PrimeFactorization:
    def __init__(self, n):
        self.n = n
        self.raw = prime_factorization(n)
        self.fact_dict = {i: self.raw.count(i) for i in self.raw}

    def fac_str(self, n):
        return str(n) + (("^" + str(self.fact_dict[n])) if self.fact_dict[n] > 1 else "")

    def __str__(self):
        str_ = ""
        for f in self.fact_dict.keys():
            if str_ == "":
                str_ = self.fac_str(f)
            else:
                str_ += " * " + self.fac_str(f)
        return str_

    def carmichael_comps(self):
        comps = []
        for pr, pow in self.fact_dict.items():
            if pr >= 3 or pow <= 2:
                comps += [euler_totient(pr ** pow)]
            elif pr == 2 and pow >= 3:
                comps += [(1 / 2) * euler_totient(pr ** pow)]
        return comps


def lcm(nums):
    if nums is None or len(nums) == 0:
        raise RuntimeError("nums cannot be empty/None")
    pf = []
    for n in nums:
        pf += [PrimeFactorization(n)]
    lcm_dict = pf[0].fact_dict
    for pf_ in pf:
        for k, v in pf_.fact_dict.items():
            if k not in lcm_dict:
                lcm_dict[k] = v
            else:
                lcm_dict[k] = max(lcm_dict[k], v)

    res = 1
    for k, v in lcm_dict.items():
        res *= int((k ** v))
    return res


def carmichael(n):
    return lcm(PrimeFactorization(n).carmichael_comps())


class Period:
    def __init__(self, seq):
        self.seq = seq
        self.length, self.val, self.occ_1 = self.__period(self.seq)
        self.i_seg = seq[:self.occ_1]
        self.r_seg = seq[self.occ_1:self.occ_1 + self.length]

    def __period(self, seq):
        found = {}
        for i, j in enumerate(seq):
            if j in found:
                return i - found[j], j, found[j]
            found[j] = i
        raise RuntimeError("No repeating sequence found.")

    def __str__(self, *args, **kwargs):
        return "Seq: %s; Initial segment: %s; Repeating segment: %s; Value: %s; Length: %s" % (self.seq, self.i_seg, self.r_seg, self.val, self.length)


def test_seq(mod, base=10):
    seq = []
    for pow in range(10):
        seq += [(base ** pow) % mod]
    return seq


if __name__ == "__main__":
    print(Period(test_seq(22)))