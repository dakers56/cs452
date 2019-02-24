from main import factors_of_n, common_factors, gcd_is_1, euler_totient
from test.conftest import PRIMES, TOTIENTS


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

def test_totient():
    for i in range(len(TOTIENTS)):
        print("Actual euler_totient(%s): %s" % (i+1, euler_totient(i+1)))
        print("Expected euler_totient(%s): %s" % (i, TOTIENTS[i]))
        assert(euler_totient(i+1) == TOTIENTS[i])