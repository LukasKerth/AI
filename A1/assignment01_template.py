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
        while remainder.degree() >= divisor.degree() and remainder.coefficients:
            remainder_degree = remainder.degree()
            divisor_degree = divisor.degree()
            leadingterm_coeff = (
                remainder.coefficients[remainder_degree]
                / divisor.coefficients[divisor_degree]
            )
            leadingterm_exp = remainder_degree - divisor_degree
            result = Polynomial(' ')
            result.coefficients[leadingterm_exp] = leadingterm_coeff
            quotient += result
            temp = divisor * result
            remainder -= temp
            remainder.clean_up()
        return quotient, remainder

    def clean_up(self):
        self.coefficients = {exp: coeff for exp, coeff in self.coefficients.items() if coeff != 0}

    def copy(self):
        new = Polynomial(' ')
        new.coefficients = self.coefficients.copy()
        return new

    def degree(self):
        if not self.coefficients:
            return -1
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
        for exp, coeff in self.coefficients.items():
            result.coefficients[exp] = coeff
        for exp, coeff in other.coefficients.items():
            result.coefficients[exp] = result.coefficients.get(exp, 0) - coeff
        result.clean_up()
        return result

    def update_remainder(self, result):
        self.coefficients.pop(self.degree())
        for exp, coeff in result.coefficients.items():
            self.coefficients[exp] = coeff
        result.clean_up()
        return self


    def __mul__(self, other):
        result = Polynomial(' ')
        for (exp, coeff) in self.coefficients.items():
            for (e, c) in other.coefficients.items():
                result.coefficients[exp + e] = result.coefficients.get(exp + e, 0) + (coeff * c)
        result.clean_up()
        return result


def polynomial_gcd(p: Polynomial, q: Polynomial):
    """Compute the greatest common divisor of two polynomials using Euclid's
    algorithm."""
    # TODO
    while q.coefficients:
        _,remainder = Polynomial.long_division(p, q)
        p,q = q,remainder
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
    p3 = Polynomial("x^3 +    5x^2 -9x +3")
    p4 = Polynomial("x^3 - 7 x^2 +9x    -3")
    print(
        polynomial_gcd(
            p3, p4
        )
    )