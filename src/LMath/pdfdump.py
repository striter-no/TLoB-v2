import os
from src.LMath.pages import Page
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont

WIDTH, HEIGHT = A4

def reg_fonts(header: str, content: str):
    pdfmetrics.registerFont(TTFont("CUSTOM_FONT", header))
    pdfmetrics.registerFont(TTFont("MONO_FONT", content))

def dump_page(
        page: Page,
        save_dir: str
) -> None:
    title = page.title.replace('-', ' ').capitalize()

    c = canvas.Canvas(f"{os.path.join(save_dir, page.title)}.pdf", pagesize=A4)
    c.setFont("CUSTOM_FONT", 24)
    c.drawCentredString(WIDTH / 2, HEIGHT - 50, title)

    def draw_multiline(start_x: float, start_y: float, text: str) -> None:
        for i, l in enumerate(text.split('\n')):
            if len(l) == 0: continue
            
            c.drawString(start_x, start_y - 16 * i, l)

    c.setFont("MONO_FONT", 12)
    draw_multiline(WIDTH * 0.11, HEIGHT - 100, page.get_formatted())

    c.save()