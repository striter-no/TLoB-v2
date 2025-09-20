from decimal import Decimal
from random import randint

from src.LMath.pages import Page, CLOSE_ALPHABET
from src.LMath.pdfdump import reg_fonts, dump_page

reg_fonts(
    header = "./assets/fonts/Bentham-Regular.ttf",
    content = "./assets/fonts/XanhMono-Regular.ttf"
)

if __name__ == "__main__":
    default: Page  = Page(CLOSE_ALPHABET, context_max_len = 80 * 40)
    max_addr: Decimal = default.max_address()

    # Just random address
    my_page = default.fork(
        address = Decimal(randint(0, int(max_addr))),
        title = "My page"
    )

    dump_page(my_page, "./assets/pdf")