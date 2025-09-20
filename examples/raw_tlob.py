from decimal import Decimal
from random import randint

from src.LMath.pages import Page, CLOSE_ALPHABET
from src.LMath.address import addr_to_B69

if __name__ == "__main__":
    default: Page  = Page(CLOSE_ALPHABET, context_max_len = 80 * 40)
    max_addr: Decimal = default.max_address()

    # Just random address
    my_page = default.fork(
        address = Decimal(randint(0, int(max_addr)))
    )

    print(f"Random address: {addr_to_B69(my_page.get_addr())}")

    print(f"\nText:\n{my_page.get_formatted(line_len=80)}")