import os
import subprocess
from main import is_prime
from test.conftest import PRIMES


# def test_is_prime():
#     primes = PRIMES
#     primes_dict = {n:is_prime(n) for n in primes}
#     composites = [i for i in range(primes[len(primes) - 1]) if not i in primes_dict]
#     for n in primes_dict:
#         assert(primes_dict[n] == True)
#     for i in composites:
#         assert(not i in primes_dict)
#         assert (is_prime(i) == False)
