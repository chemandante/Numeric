#!/usr/bin/python3
import os
import sys
from math import isqrt

from sympy.ntheory import factorint

# Set for numbers that can't be represented as sum of two squares
noSum2sq = set()


def decomposeBy2(num: int, a_max: int = 0) -> list:
    # `num` can not be expressed as sum of two squares when num == 3 mod 4
    if num & 3 == 3:
        return []
    # Check if we've already decomposed num
    if num in noSum2sq:
        return []
    # Check for obvious values
    match num:
        case 0:
            return [()]  # Empty tuple, because there are no non-zero summands
        case 1:
            return [(1,)]
    # Due to sum of two squares theorem:
    # An integer greater than one can be written as a sum of two squares if and only if its
    # prime decomposition contains no factor p**k, where prime p == 3 mod 4 and `k` is odd
    p_fact = factorint(num)
    for p, k in p_fact.items():
        if p & 3 == 3 and k & 1 == 1:
            noSum2sq.add(num)
            return []
    # If we got here, `num` can be expressed as sum of two squares. Let's find all these sums.
    # We check all numbers starting from a = floor(sqrt(n)) but not greater than `a_max`
    # down to b = ceil(sqrt(n/2)) (included)
    a, b = isqrt(num), isqrt((num >> 1) - 1) + 1
    if a_max != 0 and a > a_max:
        a = a_max
    res = []

    for i in range(a, b - 1, -1):
        n = num - i * i
        # if num is a full square, don't add 0 as a summand
        if n == 0:
            res.append((i,))
        else:
            s = isqrt(n)
            if s * s == n:
                res.append((i, s))
    return res


def decomposeBy3(num: int, a_max: int = 0) -> list:
    # Check for obvious case
    if num == 0:
        return [()]  # Empty tuple, because there are no non-zero summands

    # Due to Legendre's three-square theorem:
    # Natural number `N` can be represented as the sum of three squares of integers
    # if and only if it is NOT of the form N = 4**a * (8 * b + 7) for nonnegative integers a and b.
    m = num
    while m & 3 == 0:  # Divide by 4 as long as it is possible
        m >>= 2
    if m & 7 == 7:  # Check value modulo 8
        return []

    # If we got here, `num` can be expressed as sum of three squares. Let's find all these sums.
    # We check all first summand starting from a = floor(sqrt(n)) but not greater than `a_max`
    # down to b = ceil(sqrt(n/3)) (included)
    a, b = isqrt(num), isqrt(num // 3 - 1) + 1 if num >= 3 else 1
    if a_max != 0 and a > a_max:
        a = a_max
    res = []

    for i in range(a, b - 1, -1):
        n = num - i * i
        # Let's check that remaining part (n = num - i * i) can be represented as sum of two squares
        s2 = decomposeBy2(n, a_max=i)
        if s2:
            for s in s2:
                res.append((i, *s))
    return res


def decomposeBy4(num: int, a_max: int = 0) -> list:
    # It should be noted that due to Lagrange's four-square theorem ALL natural numbers
    # CAN be represented as sum of four squares

    # We check all first summand starting from a = floor(sqrt(n)) but not greater than `a_max`
    # down to b = ceil(sqrt(n/4)) (included)
    a, b = isqrt(num), isqrt((num >> 2) - 1) + 1 if num >= 4 else 1
    if a_max != 0 and a > a_max:
        a = a_max
    res = []

    for i in range(a, b - 1, -1):
        n = num - i * i
        # Let's check that remaining part (n = num - i * i) can be represented as sum of three squares
        s3 = decomposeBy3(n, a_max=i)
        if s3:
            for s in s3:
                res.append((i, *s))
    return res


def stopAndPrintUsage():
    print("Calculating all possible decompositions of integer N by sum of 2, 3 or 4 squares.\n")
    print("Usage:")
    print("python sum_squares.py < -2| -3| -4> <integer N>")
    exit_ex(1)


def exit_ex(exit_code: int):
    if "PYCHARM_HOSTED" not in os.environ:
        input("Press Enter to continue...")
    sys.exit(exit_code)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        stopAndPrintUsage()

    number = int(sys.argv[2])
    if number < 1:
        print("Number must be natural, i.e. N >= 1")
        exit_ex(0)

    match sys.argv[1]:
        case "-2":
            deco = decomposeBy2(number)
            if not deco:
                print(f"{number} can not be expressed as sum of two squares due to corresponding theorem.")
                exit_ex(0)
        case "-3":
            deco = decomposeBy3(number)
            if not deco:
                print(f"{number} can not be expressed as sum of three squares due to Legendre's three-square theorem.")
                exit_ex(0)
        case "-4":
            deco = decomposeBy4(number)
        case _:
            deco = []
            stopAndPrintUsage()

    print(f"Total {len(deco)} decompositions found:")

    for d in deco:
        sm = 0
        for di in d:
            sm += di * di
        if sm == number:
            print(f"{d[0]}²", end="")
            for sm in d[1:]:
                print(f"+{sm}²", end="")
            print()
        else:
            print(f"Error in decomposition of {number} as {d}")

    exit_ex(0)
