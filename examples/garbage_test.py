from random import randint
from decimal import Decimal

from src.LMath.gfactor import g2_factor
from src.LMath.pages import Page, CLOSE_ALPHABET
from load_tlob import load_page

if __name__ == "__main__":
    default: Page  = Page(CLOSE_ALPHABET, context_max_len = 80 * 40)
    max_addr: Decimal = default.max_address()

    
    books = [
        # Real one
        load_page(default, "./assets/books/the-library-of-babel.txt"),
        
        # Random
        default.fork(address = Decimal(randint(0, int(max_addr)))),
        
        # Random
        default.fork(address = Decimal(randint(0, int(max_addr))))
    ]

    for i, b in enumerate(books):

        factor = g2_factor(b.get_text())

        if factor < 0:
            print(f"Text {i + 1} is likely a random, because: ", end = "")
            
            match factor:
                case -1: print("very high or low entropy")
                case -3: print("too litle words")
                case -4: print("too big or little words")
                case -5: print("lack of real words")
        else:
            print(f"Text {i + 1} is likely a real one")