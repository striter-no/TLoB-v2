import pyperclip
from decimal import Decimal
from random import randint

from src.LMath.pages import Page, CLOSE_ALPHABET
from src.LMath.gfactor import g2_factor, decode_g2
from src.LMath.address import addr_to_B69, addr_from_B69, ALPHABET as ADDR_ALPHABET

from textual import events
from textual.screen import Screen, ModalScreen
from textual.widgets import TextArea, Footer, Label, Rule, Button, Input
from textual.containers import VerticalGroup, Horizontal, Vertical, HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from textual.app import App, ComposeResult

default: Page  = Page(CLOSE_ALPHABET, context_max_len = 80 * 40)
max_addr: Decimal = default.max_address()

class SideBar(VerticalGroup):

    curr_page = reactive(Page(CLOSE_ALPHABET))  # ← реактивное свойство

    async def watch_curr_page(self, old, new):
        print("curr_page changed, refreshing sidebar...")
        await self.recompose()

    def compose(self) -> ComposeResult:
        if self.curr_page is None:
            yield Rule(classes = "info-rule")
            yield Label(f"No page loaded", classes = "info")
            yield Rule(classes = "info-rule")
            return
        
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

class ShareScreen(ModalScreen):
    def __init__(self, page: Page, name: str | None = None, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.page = page

    def compose(self) -> ComposeResult:
        with VerticalScroll(id = "share-cont"):
            yield Label("Share your findings (esc for exit)", id = "share-label")

            g2 = g2_factor(self.page.get_text())
            yield Label(f"Title: {self.page.title}", classes="info")
            yield Label(f"G2 Factor: {g2_factor(self.page.get_text())} ({decode_g2(g2)})", classes = "value")
            
            yield Rule()
            yield Label(f"Address: {addr_to_B69(self.page.get_addr())}", classes = "value")
            pyperclip.copy(addr_to_B69(self.page.get_addr()))
            self.notify("Address was copyied to the clipboard")

    def on_key(self, event: events.Key) -> None:
        if event.key == 'escape':
            self.dismiss()

class ViewScreen(Screen):
    def __init__(self, page: Page, name: str | None = None) -> None:
        super().__init__(name)
        self.page = page

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="page-cont"):
            yield Label(self.page.title, id="main-title")
            yield Label(self.page.get_formatted(), id="main-text")

        sb = SideBar(id="side-bar")
        sb.curr_page = self.page
        yield sb

        with Horizontal(id="nav-cont"):
            yield Button("Search content", id="search-page", variant="primary")
            yield Button("Random page", id="rnd-page", variant="default")
            yield Button("Share", id="share-page", variant="default")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search-page":
            self.app.pop_screen()  # ← возвращаемся назад
        elif event.button.id == "rnd-page":
            new_page = default.fork(
                address=Decimal(randint(0, int(max_addr)))
            )
            self.page = new_page
            
            self.query_one("#main-title", Label).update(new_page.title)
            self.query_one("#main-text", Label).update(new_page.get_formatted())
            sb = self.query_one("#side-bar", SideBar)
            sb.curr_page = new_page
        elif event.button.id == "share-page":
            self.app.push_screen(ShareScreen(self.page, id="share-screen"))

class SearchScreen(Screen):
    def compose(self) -> ComposeResult:
        with open("./assets/logo.txt") as f:
            logo = f.read()
        with open("./assets/logo-label.txt") as f:
            logo_label = f.read()
        
        with Vertical(id="inp-group"):
            with Horizontal(id="logo-cont"):
                yield Label(logo, id="logo-img")
                yield Label(logo_label, id="logo-label")
            with Vertical(id="search-inp"):
                yield TextArea(placeholder="Enter text to search", id="search-ta")
                yield Input(placeholder = "Or enter the address", id ="search-addr", restrict=f"[{ADDR_ALPHABET}]*")
            with Horizontal(id="s-nav-cont"):
                yield Button(label="Search", id="search-btn", variant="primary", flat=True)
                yield Button(label="Random page", id="rand-btn", variant="primary", flat=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        ta: TextArea = self.query_one("#search-ta")
        ai: Input    = self.query_one("#search-addr")

        text = ta.document.text.lower().replace('\n', ' ')
        addr = ai.value
        if event.button.id == "search-btn":
            if addr == '':
                page = Page(CLOSE_ALPHABET, text=text)
                
                self.app.push_screen(ViewScreen(page))
                ta.clear()
            else:
                page = Page(CLOSE_ALPHABET, address=addr_from_B69(addr))
                self.app.push_screen(ViewScreen(page))
                ai.clear()
                
        if event.button.id == "rand-btn":
            page = Page(CLOSE_ALPHABET, address=Decimal(randint(0, int(max_addr))))
            
            self.app.push_screen(ViewScreen(page))
            ta.clear()

class MainApp(App):
    CSS_PATH = [
        "./.tcss/view.tcss", 
        "./.tcss/search.tcss", 
        "./.tcss/modal.tcss"
    ]

    def on_mount(self) -> None:
        self.theme = "nord"
        self.push_screen(SearchScreen())  # ← Запускаем с экрана поиска

    def compose(self) -> ComposeResult:
        yield Footer()

if __name__ == "__main__":
    app = MainApp()
    app.run()