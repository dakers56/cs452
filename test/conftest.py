import pytest
import os
import subprocess

PRIMES = None #Set at bottom of file. Declared here for visibility.

def ld_primes():
    primes = []
    unzip_files(prime_dir())
    for f in os.listdir(prime_dir()):
        with open(full_path(prime_dir(), f), 'r') as file:
            if not is_zip(file):
                primes.extend(file.readlines())
    return [int(str(p).replace("\n", "")) for p in primes]

def data_dir():
    return "data"


def prime_dir():
    return data_dir() + "/primes"


def unzip(src, dest):
    return subprocess.run(["unzip", "-o", "-d", dest, src.name])

def is_zip(file):
    return str(file.name).endswith(".zip")


def unzip_files(dir_):
    for f in os.listdir(dir_):
        with open(full_path(dir_, f), 'r') as file:
            if is_zip(file):
                print("Found zip file: %s. Unzipping now." % file.name)
                unzip(file, prime_dir())
    print("Done unzipping file in %s" % dir)


def full_path(dir_, fn):
    return dir_ + "/" + fn


PRIMES = ld_primes()
