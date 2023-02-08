#!/usr/bin/python3
import unittest
from sympy.ntheory import divisors

from sum_squares import decomposeBy4

# Count of permutations for different elements equalities in tuple
# Indexes: [<number of nonzero components> - 2][<equality bit mask>] (see uses of PERMUTATIONS[][])
PERMUTATIONS = [
    [12, 6],  # 2-tuples: (a,b,0,0) = 12 perms, (a,a,0,0) = 6 perms
    [24, 12, 12, 4],  # 3-tuples: (a,b,c,0) = 24, (a,a,b,0) = 12, (a,b,b,0) = 12, (a,a,a,0) = 4
    [24, 12, 12, 4,  # 4-tuples: (a,b,c,d) = 24, (a,a,b,c) = 12, (a,b,b,c) = 12, (a,a,a,b) = 4
     12, 6, 4, 1]]  # 4-tuples: (a,b,c,c) = 12, (a,a,b,b) = 6, (a,b,b,b) = 4, (a,a,a,a) = 1


def calcDecompositionsBy4Count(num: int) -> int:
    """
    Calculates the number of ways that a given positive integer `num` can be represented as the sum of four squares.
    Uses Jacobi's four-square theorem.
    :param num: Positive integer
    :return: Number of possible decompositions
    """
    div = divisors(num)
    if num & 1 == 1:  # if `num` is odd
        return 8 * sum(div)

    div = [d for d in div if d & 1 == 1]
    return 24 * sum(div)


def countRepresentationsOfDeco4(d: tuple) -> int:
    """
    Returns number of representations of particular 4-square decomposition (see Jacobi's four-square theorem)
    For example, decomposition of 2 = 1^2 + 1^2 can be represented in 24 ways, including permutations, zeros and
    negatives:
    (1^2 + 0^2 + 1^2 + 0^2), ((-1)^2 + 1^2 + 0^2 + 0^2), (0^2 + 0^2 + (-1)^2 + (-1)^2) and so on
    Result = 2^(number of nonzero summands) * (number of permutations including zero summands)
    :param d: Tuple of particular decomposition (can have less than 4 components). Must be sorted nonascending.
    :return: Number of representations
    """
    nzc = len(d)  # Number of nonzero summands
    if nzc == 1:  # There is only 4 permutations for one element, so result = 2 * 4 = 8
        return 8
    # If there are more than 1 element, we should compare them for equality. For example:
    # all summands are different - (a, b, c, d) has 4! = 24 permutations
    # (a, a, b, c) has 4!/2! = 12, (a, a, a, b) has 4!/3! = 4 and (a, a, b, b) has 4!/(2!*2!) = 6 perms
    # Tuple components have this relationship: d[0] >= d[1] >= d[2] >= d[3].
    # Let compose a mask number `eq` less significant bit (LSB) of which relates to leftmost inequality
    # (d[0] >= d[1]) and MSB to rightmost.
    # bit == 1 when d[i] == d[i+1] and bit == 0 when d[i] > d[i+1] (not equal)
    # `eq` will contain 3 bits for 4-tuple, 2 bits for 3-tuple and only one bit for 2-tuple.
    # This number (mask) corresponds to equalities and will be used to calculate count of permutations.
    eq = 0
    for i in range(0, nzc - 1):
        eq *= 2
        eq += 1 if d[i] == d[i + 1] else 0

    return 2**nzc * PERMUTATIONS[nzc - 2][eq]  # From `l` to index in list


class TestSumSquares(unittest.TestCase):
    nums: tuple

    @classmethod
    def setUpClass(cls):
        cls.nums = (1, 2, 3, 4, 10, 77, 2023, 2025)

    def testDecompositionBy4(self):
        for i in self.nums:
            with self.subTest(i=i):
                decs = calcDecompositionsBy4Count(i)
                deco = decomposeBy4(i)
                deco_set = set(deco)
                self.assertEqual(len(deco), len(deco_set))

                for d in deco:
                    p = d[0]
                    s = p * p
                    for x in d[1:]:
                        self.assertGreaterEqual(p, x)  # Make sure components are sorted
                        p = x
                        s += x * x
                    self.assertEqual(s, i)  # Calc sum of squares and compare with original number
                    decs -= countRepresentationsOfDeco4(d)  # Subtracting number of representations of particular tuple
                self.assertEqual(decs, 0)


if __name__ == '__main__':
    unittest.main()
