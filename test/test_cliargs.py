import pytest
from main import CliArgs

def test_correct_args():
    vals = [1,2,3,4]
    input_ = ['file_name'] + [v for v in vals] #First cli arg should be the file name
    under_test = CliArgs(input_)
    assert (under_test.__dict__ == {'b':1, 'm':2, 'x':3, 'i':4})
    assert(isinstance(under_test.b, int))
    assert(isinstance(under_test.m, int))
    assert(isinstance(under_test.x, int))
    assert(isinstance(under_test.i, int))


def test_too_few_args():
    with pytest.raises(RuntimeError):
        CliArgs(None)
        CliArgs(["someArray"])
    with pytest.raises(ValueError):
        CliArgs(["file_name", "one", "two", "three", "four"])
