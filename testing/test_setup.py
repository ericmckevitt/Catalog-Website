import pytest
import sys

def add_two(x):
    return x+2

def test_add_two():
    assert add_two(2) == 4