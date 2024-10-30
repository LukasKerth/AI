import re

class Polynomial:
    def __init__(self, poly_str: str):
        self.coefficients = {}
        # TODO

        # Regular expression pattern to match polynomial terms
        pattern = r"([+-]?)(\d*\.?\d*)?(x?)(\^\d+)?"
        poly_str = ''.join(poly_str.split())
        for match in re.finditer(pattern, poly_str):
            sign, coeff, x, exp = match.groups()
            if not sign and not coeff and not x and not exp:
                continue
            if not coeff:
                coeff = 1 if sign == '+' or sign == '' else -1
            else:
                if "." in coeff:
                    coeff = float(coeff) if sign == '+' or sign == '' else -float(coeff)
                else:
                    coeff = int(coeff) if sign == '+' or sign == '' else -int(coeff)
            if not x:
                exp = 0
            else:
                if not exp:
                    exp = 1
                else:
                    exp = int(exp[1:])

            # updates the self.coeffs
            self.coefficients[exp] = self.coefficients.get(exp, 0) + coeff

# Example usage:
    def __repr__(self):
        # TODO
        terms = []
        for exponent, coefficient in sorted(self.coefficients.items(), reverse=True):
            # :+d makes sure that the sign will be included
            if exponent > 1:
                term = f"{coefficient:+}x^{exponent}"
            if exponent == 1:
                term = f"{coefficient:+}x"
            if exponent == 0:
                term = f"{coefficient:+}"
            terms.append(term)
        return "".join(terms)

    @staticmethod
    def long_division(dividend, divisor):
        quotient = Polynomial(' ')
        remainder = dividend.copy()
        while remainder.degree() >= divisor.degree():
            remainder_degree = remainder.degree()
            divisor_degree = divisor.degree()
            leadingterm_coeff = (
                remainder.coefficients[remainder_degree]
                / divisor.coefficients[divisor_degree]
            )
            leadingterm_exp = remainder_degree - divisor_degree
            result = Polynomial(' ')
            result.coefficients[leadingterm_exp] = result.coefficients.get(leadingterm_exp, 0) + leadingterm_coeff
            quotient = quotient + result
            remainder = remainder.update_remainder(result)
        return quotient, remainder

    def copy(self):
        new = Polynomial(' ')
        new.coefficients = self.coefficients.copy()
        return new

    def degree(self):
        temp = self.coefficients.keys()
        return max(temp)

    def __add__(self, other):
        result = Polynomial(' ')
        for (exp, coeff) in self.coefficients.items():
            result.coefficients[exp] = coeff
        for (exp, coeff) in other.coefficients.items():
            result.coefficients[exp] = result.coefficients.get(exp, 0) + coeff
        return result

    def __sub__(self, other):
        result = Polynomial(' ')
        for (exp, coeff), (e, c) in zip(self.coefficients.items(), other.coefficients.items()):
            degree_self = self.degree()
            result.coefficients[exp] = coeff
        for (exp, coeff) in other.coefficients.items():
            result.coefficients[exp] = result.coefficients.get(exp, 0) - coeff
        return result

    def update_remainder(self, result):
        self.coefficients.pop(self.degree())
        for exp, coeff in result.coefficients.items():
            self.coefficients[exp] = coeff
        return self


    def __mul__(self, other):
        result = Polynomial(' ')
        for (exp, coeff) in self.coefficients.items():
            for (e, c) in other.coefficients.items():
                result.coefficients[exp + e] = result.coefficients.get(exp + e, 0) + coeff * c
        return result


def polynomial_gcd(p: Polynomial, q: Polynomial):
    """Compute the greatest common divisor of two polynomials using Euclid's
    algorithm."""
    # TODO
    if not p:
        return q
    if not q:
        return p
    while q.coefficients:
        _,r = Polynomial.long_division(p, q)
        print(r)
        p,q = q,r
    return p



if __name__ == "__main__":
    print(Polynomial("x^2 +    6x -3"))
    print(Polynomial("x^3 + 5 x^2- 2x +5"))
    p, q = Polynomial("x^5-1"), Polynomial("x-1")
    print(
        f"The polynomial division of {p} over {q} is: {Polynomial.long_division(p, q)}"
    )
    p1 = Polynomial("x^4 - 1")
    p2 = Polynomial("x^3 - x")

    gcd = polynomial_gcd(p1, p2)
    print(f"The GCD of {p1} and {p2} is: {gcd}")
    print(
        polynomial_gcd(
            Polynomial("x^3 +    5x^2 -9x +3"), Polynomial("x^3 - 7 x^2 +9x    -3")
        )
    )


