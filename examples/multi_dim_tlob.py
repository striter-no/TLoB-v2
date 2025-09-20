from decimal import Decimal
from random import randint

from src.LMath.ndim import NDIM_Point
from src.LMath.pages import Page, CLOSE_ALPHABET
from src.LMath.address import addr_to_B69, addr_to_ndim, addr_from_ndim

from load_tlob import load_page

if __name__ == "__main__":
    default: Page  = Page(CLOSE_ALPHABET, context_max_len = 80 * 40)

    # Loading book
    my_page = load_page(default, './assets/books/the-library-of-babel.txt')
    f_addr = my_page.get_addr()
    print(my_page.get_formatted())

    # Cutting to 21D
    addr_in_21D = addr_to_ndim(my_page, 21)
    print(f"in total: {addr_in_21D.dimensions}D")
    for i, coord in enumerate(addr_in_21D.coords):
        print(f"plane {i + 1}: {addr_to_B69(coord)}")
    
    print()
    addr_in_1D = addr_from_ndim(default, addr_in_21D)
    print(f"21D is {'equal' if addr_in_1D == f_addr else 'not equal'} to the start address")

    got_page = default.fork(address = addr_in_1D)
    print(got_page.get_formatted())