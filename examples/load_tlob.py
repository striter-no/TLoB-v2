import os
from decimal import Decimal

from src.LMath.pages import Page, CLOSE_ALPHABET
from src.LMath.address import addr_to_B69

def load_page(fork_from: Page, path: str) -> Page:
    with open(path) as f:
        text = f.read()

    return fork_from.fork(
        text = text, # Automaticly removes all restricted characters 
        title = os.path.basename(path).replace('-', ' ').capitalize()
    )

if __name__ == "__main__":
    default: Page  = Page(CLOSE_ALPHABET, context_max_len = 80 * 40)

    # Load the book
    my_page = load_page(default, "./assets/books/the-library-of-babel.txt")

    print(f"Address to the {my_page.title}:\n\n{addr_to_B69(my_page.get_addr())}")