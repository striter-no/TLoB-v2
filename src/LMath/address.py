from src.LMath.ndim import NDIM_Point
from src.LMath.pages import Page

from decimal import Decimal

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#-_!@*~"

def addr_to_B69(addr: Decimal) -> str:
    if addr == 0: return ALPHABET[0]
    
    neg = addr < 0
    if neg: addr = -addr

    base = len(ALPHABET)  # 64
    chars = []
    n = int(addr)
    while n:
        n, r = divmod(n, base)
        chars.append(ALPHABET[int(r)])
    
    return ('n' if neg else 'p') + ''.join(reversed(chars))

def addr_from_B69(addr: str) -> Decimal:
    neg = addr[0] == 'n'

    base = len(ALPHABET)
    number = 0
    for char in addr[1:]:
        number = number * base + ALPHABET.index(char)
    
    return (-1 if neg else 1) * Decimal(number)


def addr_to_ndim(page: Page, dims: int) -> NDIM_Point:
    text = page.get_text()
    total = page.context_max_len
    # print(len(text), total, dims)

    part_sizes = [total // dims] * dims
    remainder = total % dims
    for i in range(remainder):
        part_sizes[i] += 1

    coords = []
    start = 0
    for i in range(dims):

        part = text[start:start + part_sizes[i]]
        addr = Page(page.alphabet, context_max_len = len(part)).search(part).get_addr()
        coords.append(addr)
        start += part_sizes[i]
    return NDIM_Point(coords)

def addr_from_ndim(_default: Page, coords: NDIM_Point) -> Decimal:
    total = _default.context_max_len
    dims = coords.dimensions
    # print(total, dims)

    part_sizes = [total // dims] * dims
    remainder = total % dims
    for i in range(remainder):
        part_sizes[i] += 1

    out_text = ""
    for i, coord in enumerate(coords.coords):
        
        text = Page(_default.alphabet, context_max_len=part_sizes[i]).acquire(coord).get_text()
        out_text += text
    
    return _default.fork(text=out_text).get_addr()