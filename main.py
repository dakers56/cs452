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
        self.length, self.val, self.r_seg_start = self.__period(self.seq)
        self.i_seg = seq[:self.r_seg_start]
        self.r_seg = seq[self.r_seg_start:self.r_seg_start + self.length]
        self.i_plus_r_seg = self.i_seg + self.r_seg

    def __period(self, seq):
        found = {}
        for i, j in enumerate(seq):
            if j in found:
                return i - found[j], j, found[j]
            found[j] = i
        raise RuntimeError("No repeating sequence found.")

    def __str__(self, *args, **kwargs):
        return "Seq: %s; Initial segment: %s; Repeating segment: %s; Value: %s; Length: %s" % (
            self.seq, self.i_seg, self.r_seg, self.val, self.length)


def test_seq(mod, base=10):
    seq = []
    for pow in range(10):
        seq += [(base ** pow) % mod]
    return seq


def from_base_10(n_b10, b):
    """Takes a number n_b10 in base 10 and returns it in the given base b."""
    radix = b - 1  # Radix is one less than b b/c b is the number of unique digits
    pow = 0
    b_digits = []  # Digits in base b representation of the number
    rem = lambda m_b10, b, pow: n_b10 - (b ** pow)
    r_i = rem(n_b10, b, pow)
    while r_i >= 0:
        b_digits += [r_i]
        pow += 1
        n_b10 /= 10
        r_i = rem(n_b10, b, pow)
    return b_digits


def __test_from_base_10(n_b10, b):
    print("%s (base 10) converted to base %s: %s" % (n_b10, b, from_base_10(n_b10, b)))


class DFA:
    def __init__(self, mod, base, seq):
        self.m = mod
        self.base = base
        self.w = base - 1
        self.period = Period(seq)


class DFAState:
    def __init__(self, i, j, b, m, period):
        self.i = i
        self.j = j
        self.b = b
        self.m = m
        self.period = period
        self.tran_func = {d: self.__calc_delta_of(d) for d in range(b)}

    def delta_of(self, d):
        return self.tran_func[d]

    def __str__(self):
        str_ = "["
        for d in range(self.b - 1):
            str_ += "(%s, %s), " % (self.delta_of(d))
        str_ += "(%s, %s)]" % (self.delta_of(self.b - 1))
        return str_

    def __in_init_seg(self):
        return self.i < len(self.period.i_seg)

    def next_in_i_seg(self):
        return self.i + 1

    def next_in_r_seg(self):
        return self.period.r_seg_start + ((self.j + 1 - self.period.r_seg_start) % len(self.period.r_seg))

    def current_period_val(self, in_i_seg=False):
        return self.period.i_plus_r_seg[self.i]

    def next_classifier_val(self, digit):
        return (self.j + (digit * self.current_period_val())) % self.m

    def __calc_delta_of(self, d):
        """ Returns the state transitioned to when b is read in the current state (i,j)."""
        if ((self.j % len(self.period.r_seg)) > self.b):
            raise RuntimeError("Repeating sequence was too long to calculate transition function: %s" % (
                self.j % len(self.period.r_seg) > self.b))
        if self.__in_init_seg():
            return self.i + 1, self.next_classifier_val(digit=d)
        return self.next_in_r_seg(), self.next_classifier_val(digit=d)


if __name__ == "__main__":
    mod = 4
    seq = [(10 ** p) % mod for p in range(2 * (mod + 1))]

    period = Period(seq)
    print("Period for division modulo %s: %s" % (mod, period))
    n_states = 0
    for  i in range(3):
        for j in range(10):
            n_states += 1
            print("DFA state with i = %s, j = %s, b = %s, mod = %s: %s" % (
            i, j, 10, mod, DFAState(i=i, j=j, m=mod, b=10, period=period)))
    print("Number of states: %s" % n_states)

