"""Combinatorics operations: Factorial, Permutations, Combinations, Fibonacci, etc."""

import math
from functools import lru_cache
from typing import TYPE_CHECKING

from mathlang.operations.base import Operation, OperationProvider, ArgInfo
from mathlang.types.scalar import Scalar
from mathlang.types.collection import List
from mathlang.engine.errors import TypeError, ArgumentError

if TYPE_CHECKING:
    from mathlang.types.base import MathObject
    from mathlang.engine.session import Session


class CombinatoricsProvider(OperationProvider):
    """Provider for combinatorics operations."""

    @property
    def name(self) -> str:
        return "Combinatorics"

    def _register_operations(self) -> None:
        self.register(Operation(
            identifier="Factorial",
            friendly_name="Factorial",
            description="Calculates n! (n factorial)",
            category="Combinatorics/Basic",
            required_args=[ArgInfo("n", "Non-negative integer")],
            execute=self._factorial,
        ))

        self.register(Operation(
            identifier="Permutations",
            friendly_name="Permutations (nPr)",
            description="Calculates the number of permutations of r items from n items",
            category="Combinatorics/Basic",
            required_args=[
                ArgInfo("n", "Total number of items"),
                ArgInfo("r", "Number of items to select"),
            ],
            execute=self._permutations,
        ))

        self.register(Operation(
            identifier="Combinations",
            friendly_name="Combinations (nCr)",
            description="Calculates the number of combinations of r items from n items",
            category="Combinatorics/Basic",
            required_args=[
                ArgInfo("n", "Total number of items"),
                ArgInfo("r", "Number of items to select"),
            ],
            execute=self._combinations,
        ))

        self.register(Operation(
            identifier="Fibonacci",
            friendly_name="Fibonacci",
            description="Returns the nth Fibonacci number (0-indexed: F(0)=0, F(1)=1)",
            category="Combinatorics/Sequences",
            required_args=[ArgInfo("n", "Index in the sequence (0-based)")],
            execute=self._fibonacci,
        ))

        self.register(Operation(
            identifier="FibonacciList",
            friendly_name="Fibonacci List",
            description="Returns the first n Fibonacci numbers",
            category="Combinatorics/Sequences",
            required_args=[ArgInfo("n", "Number of Fibonacci numbers to generate")],
            execute=self._fibonacci_list,
        ))

        self.register(Operation(
            identifier="GCD",
            friendly_name="Greatest Common Divisor",
            description="Calculates the greatest common divisor of two integers",
            category="Combinatorics/Number Theory",
            required_args=[
                ArgInfo("a", "First integer"),
                ArgInfo("b", "Second integer"),
            ],
            execute=self._gcd,
        ))

        self.register(Operation(
            identifier="LCM",
            friendly_name="Least Common Multiple",
            description="Calculates the least common multiple of two integers",
            category="Combinatorics/Number Theory",
            required_args=[
                ArgInfo("a", "First integer"),
                ArgInfo("b", "Second integer"),
            ],
            execute=self._lcm,
        ))

        self.register(Operation(
            identifier="IsPrime",
            friendly_name="Is Prime",
            description="Tests whether a number is prime",
            category="Combinatorics/Number Theory",
            required_args=[ArgInfo("n", "Integer to test")],
            execute=self._is_prime,
        ))

        self.register(Operation(
            identifier="PrimeFactors",
            friendly_name="Prime Factors",
            description="Returns the prime factorization of a number",
            category="Combinatorics/Number Theory",
            required_args=[ArgInfo("n", "Positive integer to factor")],
            execute=self._prime_factors,
        ))

        self.register(Operation(
            identifier="Primes",
            friendly_name="Primes Up To",
            description="Returns all prime numbers up to n",
            category="Combinatorics/Number Theory",
            required_args=[ArgInfo("n", "Upper limit")],
            execute=self._primes,
        ))

        self.register(Operation(
            identifier="BinomialCoeff",
            friendly_name="Binomial Coefficient",
            description="Calculates the binomial coefficient (n choose k)",
            category="Combinatorics/Basic",
            required_args=[
                ArgInfo("n", "Total number"),
                ArgInfo("k", "Selection number"),
            ],
            execute=self._binomial_coeff,
        ))

    def _get_non_negative_int(self, value: "MathObject", name: str) -> int:
        """Extract a non-negative integer from a MathObject."""
        if not isinstance(value, Scalar):
            raise TypeError(f"{name} must be an integer, got {value.type_name}")
        if not isinstance(value.value, int):
            raise TypeError(f"{name} must be an integer, got float")
        if value.value < 0:
            raise ArgumentError(f"{name} must be non-negative, got {value.value}")
        return value.value

    def _get_positive_int(self, value: "MathObject", name: str) -> int:
        """Extract a positive integer from a MathObject."""
        n = self._get_non_negative_int(value, name)
        if n == 0:
            raise ArgumentError(f"{name} must be positive, got 0")
        return n

    def _get_int(self, value: "MathObject", name: str) -> int:
        """Extract any integer from a MathObject."""
        if not isinstance(value, Scalar):
            raise TypeError(f"{name} must be an integer, got {value.type_name}")
        if not isinstance(value.value, int):
            raise TypeError(f"{name} must be an integer, got float")
        return value.value

    def _factorial(self, args: list["MathObject"], session: "Session") -> "MathObject":
        n = self._get_non_negative_int(args[0], "n")
        if n > 170:
            raise ArgumentError(f"Factorial too large: {n}! exceeds floating point range")
        return Scalar(math.factorial(n))

    def _permutations(self, args: list["MathObject"], session: "Session") -> "MathObject":
        n = self._get_non_negative_int(args[0], "n")
        r = self._get_non_negative_int(args[1], "r")
        if r > n:
            raise ArgumentError(f"r ({r}) cannot be greater than n ({n})")
        return Scalar(math.perm(n, r))

    def _combinations(self, args: list["MathObject"], session: "Session") -> "MathObject":
        n = self._get_non_negative_int(args[0], "n")
        r = self._get_non_negative_int(args[1], "r")
        if r > n:
            raise ArgumentError(f"r ({r}) cannot be greater than n ({n})")
        return Scalar(math.comb(n, r))

    def _fibonacci(self, args: list["MathObject"], session: "Session") -> "MathObject":
        n = self._get_non_negative_int(args[0], "n")
        if n > 1000:
            raise ArgumentError(f"Fibonacci index too large: {n}")
        return Scalar(self._fib(n))

    @staticmethod
    @lru_cache(maxsize=1024)
    def _fib(n: int) -> int:
        """Calculate nth Fibonacci number using matrix exponentiation."""
        if n <= 1:
            return n

        # Use iterative approach for large n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    def _fibonacci_list(self, args: list["MathObject"], session: "Session") -> "MathObject":
        n = self._get_positive_int(args[0], "n")
        if n > 1000:
            raise ArgumentError(f"Too many Fibonacci numbers requested: {n}")

        fibs = []
        a, b = 0, 1
        for _ in range(n):
            fibs.append(Scalar(a))
            a, b = b, a + b

        return List(fibs)

    def _gcd(self, args: list["MathObject"], session: "Session") -> "MathObject":
        a = self._get_int(args[0], "a")
        b = self._get_int(args[1], "b")
        return Scalar(math.gcd(a, b))

    def _lcm(self, args: list["MathObject"], session: "Session") -> "MathObject":
        a = self._get_int(args[0], "a")
        b = self._get_int(args[1], "b")
        return Scalar(math.lcm(a, b))

    def _is_prime(self, args: list["MathObject"], session: "Session") -> "MathObject":
        n = self._get_int(args[0], "n")
        if n < 2:
            return Scalar(0)

        if n == 2:
            return Scalar(1)
        if n % 2 == 0:
            return Scalar(0)

        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return Scalar(0)

        return Scalar(1)

    def _prime_factors(self, args: list["MathObject"], session: "Session") -> "MathObject":
        n = self._get_positive_int(args[0], "n")

        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(Scalar(d))
                n //= d
            d += 1
        if n > 1:
            factors.append(Scalar(n))

        return List(factors)

    def _primes(self, args: list["MathObject"], session: "Session") -> "MathObject":
        n = self._get_non_negative_int(args[0], "n")
        if n < 2:
            return List([])
        if n > 1000000:
            raise ArgumentError(f"Upper limit too large: {n}")

        # Sieve of Eratosthenes
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False

        for i in range(2, int(math.sqrt(n)) + 1):
            if sieve[i]:
                for j in range(i * i, n + 1, i):
                    sieve[j] = False

        primes = [Scalar(i) for i, is_prime in enumerate(sieve) if is_prime]
        return List(primes)

    def _binomial_coeff(self, args: list["MathObject"], session: "Session") -> "MathObject":
        n = self._get_non_negative_int(args[0], "n")
        k = self._get_non_negative_int(args[1], "k")
        if k > n:
            return Scalar(0)
        return Scalar(math.comb(n, k))
