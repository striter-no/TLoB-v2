from decimal import Decimal
from random import randint

from src.LMath.pages import Page, CLOSE_ALPHABET
from src.LMath.gfactor import g2_factor, decode_g2
from src.LMath.address import addr_to_B69

from textual.widgets import Header, Footer, Label, Rule
from textual.containers import VerticalGroup
from textual.app import App, ComposeResult

default: Page  = Page(CLOSE_ALPHABET, context_max_len = 80 * 40)
max_addr: Decimal = default.max_address()

class SideBar(VerticalGroup):

    curr_page: Page | None = None

    def compose(self) -> ComposeResult:
        if self.curr_page is None:
            return None
        
        b69 = addr_to_B69(self.curr_page.get_addr())
        yield Rule(classes = "info-rule")
        yield Label(f"address:", classes = "info")
        yield Label(f"{b69[:15]}...{b69[-15:]}", classes = "info-value")
        yield Label(f"distance:", classes = "info")
        yield Label(f"~10^{self.curr_page.get_addr().log10():.5f}", classes = "info-value")
        
        g2f = g2_factor(self.curr_page.get_text())
        yield Label(f"g2 factor:", classes="info")
        yield Label(f"{g2f} ({decode_g2(g2f)})", classes = "info-value")
        yield Rule(classes = "info-rule")

class MainApp(App):
    
    CSS_PATH = "./.tcss/main.tcss"

    my_page = default.fork(
        address = Decimal(randint(0, int(max_addr))),
        title = "Title of the page"
    )

    def compose(self) -> ComposeResult:
        self.theme = "gruvbox"
        yield Label(
            content = self.my_page.title,
            id = "main-title"
        )
        yield Label(
            content = self.my_page.get_formatted(),
            id = "main-text"
        )
        sb = SideBar(
            id = "side-bar"
        )
        sb.curr_page = self.my_page
        yield sb

        yield Footer()

if __name__ == "__main__":
    app = MainApp()
    app.run()