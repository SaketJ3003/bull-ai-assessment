import os
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph

from app.pdf.pages import ReportPages
from app.pdf.styles import SMALL_STYLE, NAVY, BLUE, MUTED, GRID


class ResearchDocTemplate(SimpleDocTemplate):
    """A4 report template with PDF outline/bookmark support."""

    def afterFlowable(self, flowable):
        if not isinstance(flowable, Paragraph):
            return

        style_name = getattr(flowable.style, "name", "")
        if style_name not in {"Title", "Section"}:
            return

        text = re.sub(r"<[^>]+>", "", flowable.getPlainText()).strip()
        if not text:
            return

        key = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        key = f"{key}-{self.page}"

        try:
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(
                text[:80],
                key,
                level=0 if style_name == "Title" else 1,
                closed=False,
            )
        except Exception:
            pass


class FinancialReportPDF:

    def __init__(self, report, output_path):
        self.report = report
        self.output_path = output_path
        self.chart_dir = os.path.join(
            os.path.dirname(output_path),
            "charts",
        )

        self.doc = ResearchDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=8 * mm,
            leftMargin=8 * mm,
            topMargin=10 * mm,
            bottomMargin=10 * mm,
            title=f"{self.report.company.name or 'Financial'} Research Report",
            author="Bull AI",
            subject="AI-generated financial research report",
            creator="Bull AI Financial Research",
        )

    def _header_footer(self, canvas, doc):
        canvas.saveState()
        width, height = A4

        canvas.setStrokeColor(BLUE)
        canvas.setLineWidth(1.15)
        canvas.line(8 * mm, height - 6.5 * mm, width - 8 * mm, height - 6.5 * mm)

        canvas.setFont("Helvetica-Bold", 5.6)
        canvas.setFillColor(NAVY)
        canvas.drawString(8 * mm, height - 5.2 * mm, "BULL AI")

        canvas.setFont("Helvetica", 4.8)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(
            width - 8 * mm,
            height - 5.2 * mm,
            "AI FINANCIAL RESEARCH • CONFIDENTIAL",
        )

        company = self.report.company.name or "Financial Research Report"

        canvas.setStrokeColor(GRID)
        canvas.setLineWidth(0.35)
        canvas.line(8 * mm, 8 * mm, width - 8 * mm, 8 * mm)

        canvas.setFont("Helvetica-Bold", 5.1)
        canvas.setFillColor(NAVY)
        canvas.drawString(8 * mm, 5 * mm, company)

        canvas.setFont("Helvetica", 5.1)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(
            width / 2,
            5 * mm,
            "Bull AI • Research Intelligence",
        )
        canvas.drawRightString(
            width - 8 * mm,
            5 * mm,
            f"Page {doc.page}",
        )

        canvas.restoreState()

    def build(self):
        os.makedirs(os.path.dirname(self.output_path) or ".", exist_ok=True)

        pages = ReportPages(self.report, self.chart_dir)
        story = []

        story.extend(pages.page_one())
        story.append(PageBreak())
        story.extend(pages.page_two())
        story.append(PageBreak())
        story.extend(pages.page_three())
        story.append(PageBreak())
        story.extend(pages.page_four())

        self.doc.build(
            story,
            onFirstPage=self._header_footer,
            onLaterPages=self._header_footer,
        )

        return self.output_path
