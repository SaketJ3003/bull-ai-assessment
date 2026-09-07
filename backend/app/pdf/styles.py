from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

NAVY = colors.HexColor("#0B1324")
NAVY_2 = colors.HexColor("#101B31")
BLUE = colors.HexColor("#4F7FE8")
BLUE_LIGHT = colors.HexColor("#EAF1FF")
PURPLE = colors.HexColor("#7667E8")
PURPLE_LIGHT = colors.HexColor("#F0EDFF")
GREEN = colors.HexColor("#1FA774")
GREEN_LIGHT = colors.HexColor("#EAF8F2")
RED = colors.HexColor("#D85C64")
RED_LIGHT = colors.HexColor("#FDEEEF")
GOLD = colors.HexColor("#D99A2B")
GOLD_LIGHT = colors.HexColor("#FFF7E7")
INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#647086")
GRID = colors.HexColor("#DDE4EF")
PALE = colors.HexColor("#F6F8FC")
WHITE = colors.white

TITLE_STYLE = ParagraphStyle("Title", fontName="Helvetica-Bold", fontSize=14, leading=15,
    textColor=INK, alignment=TA_LEFT, spaceAfter=3)
SUBTITLE_STYLE = ParagraphStyle("Subtitle", fontName="Helvetica", fontSize=7, leading=8,
    textColor=MUTED, alignment=TA_LEFT, spaceAfter=2)
SECTION_STYLE = ParagraphStyle("Section", fontName="Helvetica-Bold", fontSize=8, leading=9,
    textColor=NAVY, alignment=TA_LEFT, spaceBefore=3, spaceAfter=2)
BODY_STYLE = ParagraphStyle("Body", fontName="Helvetica", fontSize=6.5, leading=7.2,
    textColor=INK, alignment=TA_LEFT, spaceAfter=2)
SMALL_STYLE = ParagraphStyle("Small", fontName="Helvetica", fontSize=5.2, leading=5.8,
    textColor=MUTED, alignment=TA_LEFT)
TABLE_HEADER_STYLE = ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=5.2,
    leading=5.8, textColor=WHITE, alignment=TA_CENTER)
TABLE_CELL_STYLE = ParagraphStyle("TableCell", fontName="Helvetica", fontSize=4.9,
    leading=5.4, textColor=INK, alignment=TA_LEFT)
CENTER_STYLE = ParagraphStyle("Center", fontName="Helvetica", fontSize=6.5, leading=7,
    textColor=INK, alignment=TA_CENTER)
KPI_LABEL_STYLE = ParagraphStyle("KpiLabel", fontName="Helvetica-Bold", fontSize=5.2,
    leading=6, textColor=MUTED, alignment=TA_LEFT)
KPI_VALUE_STYLE = ParagraphStyle("KpiValue", fontName="Helvetica-Bold", fontSize=11,
    leading=12, textColor=NAVY, alignment=TA_LEFT)
CALLOUT_STYLE = ParagraphStyle("Callout", fontName="Helvetica", fontSize=6.2,
    leading=7.2, textColor=INK, alignment=TA_LEFT)
