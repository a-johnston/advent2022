digits = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}
inv = dict((v, k) for k, v in digits.items())


def snafu_to_dec(x):
    v = 0
    for c in x:
        v *= 5
        v += digits[c]
    return v


def dec_to_snafu(x):
    funny_numbers = ''
    while x > 0:
        d = x % 5
        if d > 2:
            d -= 5
        x = (x - d) / 5
        funny_numbers = inv[d] + funny_numbers
    return funny_numbers


def solve(lines):
    total = sum(map(snafu_to_dec, lines))
    return dec_to_snafu(total)
