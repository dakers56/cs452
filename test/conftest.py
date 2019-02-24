import pytest
import os
import subprocess

PRIMES = None #Set at bottom of file. Declared here for visibility.
TOTIENTS = None
CARMS = None

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

def totient_dir():
    return data_dir() + "/" + "totient"

def ld_totients():
    totients = []
    with open(full_path(totient_dir(), "totient-1-69.txt"), 'r') as f:
        totients = f.readlines()
    return [int(str(t).replace("\n", "")) for t in totients]

def carm_dir():
    return data_dir() + "/" + "carmichael"

def ld_carms():
    carms = []
    with open(full_path(carm_dir(), "carmichael-1-81.txt"), 'r') as f:
        carms = f.readlines()
    return [int(str(t).replace("\n", "")) for t in carms]

PRIMES = ld_primes()
TOTIENTS = ld_totients()
CARMS = ld_carms()


