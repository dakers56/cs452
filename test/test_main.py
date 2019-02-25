from main import factors_of_n, common_factors, gcd_is_1, euler_totient, is_prime, ld_primes as ld_primes_main, \
    prime_factorization, lcm, carmichael, Period, DFAState, DFA
from test.conftest import PRIMES, TOTIENTS, CARMS


# def test_even_factors_of():
#     evens = range(4, 10000, 2)
#     for e in evens:
#         assert(2 in factors_of(e))
#
# def test_odd_factors_of():
#     odds = range(3, 10000, 2)
#     for e in odds:
#         assert(not 2 in factors_of(e))
#
# def test_prime_factors_of():
#     for p in PRIMES:
#         assert(factors_of(p) == [])

# fac_of_20 = [2, 4, 5, 10]
# fac_of_90 = [2, 3, 5, 6, 9, 10, 15, 18, 30, 45]
# fac_of_40 = [2, 4, 5, 8, 10, 20]
#
#
# def test_misc_factors_of():
#     assert (factors_of_n(20) == fac_of_20)
#     assert (factors_of_n(90) == fac_of_90)
#     assert (factors_of_n(40) == fac_of_40)
#
#
# def test_even_common_factors():
#     evens = range(4, 10000, 2)
#     for e in evens:
#         assert (2 in common_factors(e, 4))
#
#
# def test_odd_factors_of():
#     odds = range(5, 10000, 2)
#     for e in odds:
#         assert (not 2 in common_factors(e, 4))
#
# def test_misc_common_factors():
#     assert (common_factors(20, 40) == {2,4,5,10})
#     assert (common_factors(20, 90) == {2,5,10})
#     assert (common_factors(40, 90) == {2,5,10})

# def test_gcd_is_1():
#     expected = {1: True, 2: False, 3: True, 4: False, 5: False, 6: False, 7: True, 8: False, 9: True}
#     for k, v in expected.items():
#         assert (gcd_is_1(10, k) == v)
#
#     # for p in PRIMES[3:]: #exclude 2,5
#     #     assert (gcd_is_1(p, 10))
#
#
#     expected = {i:True for i in range(25)}
#     expected[5] = expected[10] = expected[15] = expected[20] = False
#     for k, v in expected.items():
#         assert (gcd_is_1(25, k) == v)
#
#     expected = {i:True for i in range(34)}
#     expected[2] = expected[17] = False
#     for i in range(4,34,2):
#         expected[i] = False
#     for k, v in expected.items():
#         assert (gcd_is_1(34, k) == v)

# def test_totient():
#     for i in range(len(TOTIENTS)):
#         print("Actual euler_totient(%s): %s" % (i+1, euler_totient(i+1)))
#         print("Expected euler_totient(%s): %s" % (i, TOTIENTS[i]))
#         assert(euler_totient(i+1) == TOTIENTS[i])
#
# def test_ld_primes():
#     primes = ld_primes_main()
#     for i in range(len(PRIMES)):
#             assert(primes[i] == PRIMES[i])


# def __prime_fac_test(n):
#     for m in n:
#         assert(is_prime(m))
#
# def test_prime_fac():
#     for i in range(5000):
#         pf = prime_factorization(i)
#         print(pf)
#         __prime_fac_test(pf)

# def test_lcm():
#     lcm_dict = {12:[4,6], 130:[65,10,5], 6914628732:[54321, 789, 484]}
#     for k,v in lcm_dict.items():
#         assert (lcm(v) == k)


def test_carms():
    for i in range(2, len(TOTIENTS)):
        print("Actual carmichael(%s): %s" % (i + 1, carmichael(i + 1)))
        print("Expected euler_totient(%s): %s" % (i, CARMS[i]))
        assert (carmichael(i + 1) == CARMS[i])


def __make_seq(mod, base=10):
    seq = []
    for pow in range(10):
        seq += [(base ** pow) % mod]
    return seq


def test_period():
    mod = 22
    seq = __make_seq(mod)
    period = Period(seq)
    assert (period.i_seg == [1])
    assert (period.r_seg == [10, 12])
    assert (period.length == 2)
    assert (period.val == 10)

    mod = 25
    seq = __make_seq(mod)
    period = Period(seq)
    assert (period.i_seg == [1, 10])
    assert (period.r_seg == [0])
    assert (period.length == 1)
    assert (period.val == 0)

    mod = 37
    seq = __make_seq(mod)
    period = Period(seq)
    assert (period.i_seg == [])
    assert (period.r_seg == [1, 10, 26])
    assert (period.length == 3)
    assert (period.val == 1)


def __assert_for_dfa_states(n_states, states, state_index):
    assert (n_states == len(states))
    assert (n_states == len(state_index))
    for s in states:
        assert ((s.i, s.j) in state_index)
        for _, s_t in s.tran_func.items():
            assert s_t in state_index


def __assert_for_dfa(n_states, state_index, dfa):
    dfa_n_states = 0
    for i in range(len(dfa.states)):
        for j in range(len(dfa.states[i])):
            dfa_n_states += 1
    assert (n_states == dfa_n_states)
    assert (n_states == len(state_index))
    for i in range(len(dfa.states)):
        for j in range(len(dfa.states[i])):
            assert ((dfa.states[i][j].i, dfa.states[i][j].j) in state_index)
            for _, s_t in dfa.states[i][j].tran_func.items():
                assert s_t in state_index


def test_dfa_states():
    mod = 4
    seq = [(10 ** p) % mod for p in range(2 * (mod + 1))]
    b = 10

    period = Period(seq)
    print("Period for division modulo %s: %s" % (mod, period))
    n_states = 0
    states = set()
    state_index = set()
    w = len(period.i_plus_r_seg)
    for i in range(w):
        for j in range(mod):
            this_state = DFAState(i=i, j=j, m=mod, b=10, period=period)
            states.add(this_state)
            state_index.add((i, j))
            n_states += 1
            print("DFA state with i = %s, j = %s, b = %s, mod = %s: %s" % (i, j, b, mod, this_state))

            print("Number of states: %s" % n_states)

    __assert_for_dfa_states(n_states, states, state_index)


def test_dfa():
    mod = 4
    seq = [(10 ** p) % mod for p in range(2 * (mod + 1))]
    base = 10
    dfa = DFA(mod=mod, base=base, seq=seq)

    period = Period(seq)
    w = 3
    states = set()
    state_index = set()
    for i in range(w):
        for j in range(mod):
            this_state = DFAState(i=i, j=j, m=mod, b=10, period=period)
            states.add(this_state)
            state_index.add((i, j))

    __assert_for_dfa(12, state_index, dfa)
