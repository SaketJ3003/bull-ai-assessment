import os
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    Spacer,
    PageBreak,
    Image,
    Table,
    TableStyle,
    KeepTogether,
)

from app.pdf.styles import (
    TITLE_STYLE,
    SUBTITLE_STYLE,
    SECTION_STYLE,
    BODY_STYLE,
    SMALL_STYLE,
    KPI_LABEL_STYLE,
    KPI_VALUE_STYLE,
    CALLOUT_STYLE,
    NAVY,
    NAVY_2,
    BLUE,
    BLUE_LIGHT,
    PURPLE,
    PURPLE_LIGHT,
    GREEN,
    GREEN_LIGHT,
    RED,
    RED_LIGHT,
    GOLD,
    GOLD_LIGHT,
    INK,
    MUTED,
    GRID,
    PALE,
    WHITE,
)

from app.pdf.tables import (
    financial_table,
    key_value_table,
)

from app.pdf.charts import create_financial_chart


class ReportPages:

    def __init__(self, report, chart_dir):

        self.report = report
        self.chart_dir = chart_dir
        self._section_counter = 0

    def _anchor(self, title):
        self._section_counter += 1
        key = re.sub(r"[^a-z0-9]+", "-", str(title).lower()).strip("-")
        return f"{key}-{self._section_counter}"

    def _section(self, title, accent=BLUE):
        anchor = self._anchor(title)
        marker = Paragraph(f'<a name="{anchor}"/>{title}', SECTION_STYLE)
        bar = Table([[""]], colWidths=[1.3 * mm], rowHeights=[5.2 * mm])
        bar.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), accent),
            ("BOX", (0, 0), (-1, -1), 0, accent),
        ]))
        heading = Table([[bar, marker]], colWidths=[2.5 * mm, 185 * mm])
        heading.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ]))
        return heading

    def _styled_table(self, table, accent=BLUE):
        if not hasattr(table, "setStyle"):
            return table
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), accent),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.28, GRID),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 2.2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
        ]))
        return table

    def _kpi_cards(self, cards):
        cells = []
        for label, value, accent, bg in cards:
            inner = Table([
                [Paragraph(str(label).upper(), KPI_LABEL_STYLE)],
                [Paragraph(str(value), KPI_VALUE_STYLE)],
            ], colWidths=[43.5 * mm], rowHeights=[5.5 * mm, 8.5 * mm])
            inner.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.55, accent),
                ("LINEBEFORE", (0, 0), (0, -1), 2.1, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            cells.append(inner)
        outer = Table([cells], colWidths=[45.5 * mm] * len(cells))
        outer.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 1.5),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        return outer

    def _callout(self, title, text, accent=BLUE, background=BLUE_LIGHT):
        box = Table([[
            Paragraph(f"<b>{title}</b><br/>{text}", CALLOUT_STYLE)
        ]], colWidths=[188 * mm])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), background),
            ("LINEBEFORE", (0, 0), (0, -1), 2.2, accent),
            ("BOX", (0, 0), (-1, -1), 0.45, accent),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        return box

    # =========================================================
    # PAGE 1
    # =========================================================

    def page_one(self):

        story = []

        company = self.report.company.name or "Company"

        story.append(
            Paragraph(
                "Retail Equity Research",
                SUBTITLE_STYLE,
            )
        )

        story.append(
            Paragraph(
                company,
                TITLE_STYLE,
            )
        )

        story.append(
            Paragraph(
                f"Sector: {self.report.company.sector or '-'}",
                SUBTITLE_STYLE,
            )
        )

        story.append(Spacer(1, 2.5 * mm))

        story.append(
            self._callout(
                "AI RESEARCH SNAPSHOT",
                self.report.business_summary or
                "Financial context extracted from the supplied source document.",
                accent=BLUE,
                background=BLUE_LIGHT,
            )
        )
        story.append(Spacer(1, 2 * mm))

        # -----------------------------------------------------
        # Recommendation
        # -----------------------------------------------------

        story.append(self._section("Recommendation", PURPLE))

        rec = self.report.recommendation

        story.append(
            self._kpi_cards([
                ("Rating", rec.rating or "-", PURPLE, PURPLE_LIGHT),
                ("Target", self._rs(rec.target_price), BLUE, BLUE_LIGHT),
                ("CMP", self._rs(rec.current_price), NAVY, PALE),
                ("Expected Return", self._pct(rec.expected_return), GREEN, GREEN_LIGHT),
            ])
        )

        # -----------------------------------------------------
        # Company Data
        # -----------------------------------------------------

        story.append(self._section("Company Data"))

        cd = self.report.company_data

        story.append(
            key_value_table(
                [
                    ("Market Cap", cd.market_cap),
                    ("52W High", cd.week_52_high),
                    ("52W Low", cd.week_52_low),
                    ("EV", cd.enterprise_value),
                    ("Shares", cd.outstanding_shares),
                    ("Free Float", self._pct(cd.free_float_percent)),
                    ("Dividend Yield", self._pct(cd.dividend_yield_percent)),
                    ("6M Avg Volume", cd.average_volume_6m),
                    ("Beta", cd.beta),
                    ("Face Value", cd.face_value),
                ],
                columns=2,
            )
        )

        # -----------------------------------------------------
        # Shareholding
        # -----------------------------------------------------

        if self.report.shareholding:

            story.append(self._section("Shareholding Pattern"))

            headers = [
                "Period",
                "Promoters",
                "FIIs",
                "MFs / Inst.",
                "Public",
                "Others",
                "Total",
            ]

            rows = []

            for item in self.report.shareholding:

                rows.append(
                    [
                        item.period,
                        item.promoters,
                        item.fiis,
                        item.mutual_funds_institutions,
                        item.public,
                        item.others,
                        item.total,
                    ]
                )

            story.append(
                self._styled_table(
                    financial_table(
                        headers,
                        rows,
                    )
                )
            )

        # -----------------------------------------------------
        # Price Performance
        # -----------------------------------------------------

        pp = self.report.price_performance

        story.append(self._section("Price Performance", GREEN))

        story.append(
            self._styled_table(
                financial_table(
                    [
                        "Period", "3M", "6M", "1Y",
                    ],
                    [
                        [
                            "Absolute",
                            self._pct(pp.absolute_return_3m),
                            self._pct(pp.absolute_return_6m),
                            self._pct(pp.absolute_return_1y),
                        ],
                        [
                            "Sensex",
                            self._pct(pp.sensex_return_3m),
                            self._pct(pp.sensex_return_6m),
                            self._pct(pp.sensex_return_1y),
                        ],
                        [
                            "Relative",
                            self._pct(pp.relative_return_3m),
                            self._pct(pp.relative_return_6m),
                            self._pct(pp.relative_return_1y),
                        ],
                    ],
                )
            )
        )

        # -----------------------------------------------------
        # Outlook
        # -----------------------------------------------------

        if self.report.outlook_valuation:

            story.append(self._section("Outlook & Valuation", PURPLE))

            story.append(
                Paragraph(
                    self.report.outlook_valuation,
                    BODY_STYLE,
                )
            )

        # -----------------------------------------------------
        # Quarterly Financials
        # -----------------------------------------------------

        if self.report.quarterly_financials:

            story.append(self._section("Quarterly Financials"))

            headers = ["Metric"]

            for item in self.report.quarterly_financials:
                headers.append(item.period)

            rows = []

            metrics = [
                ("Sales", "sales"),
                ("YoY Growth", "sales_growth_yoy"),
                ("QoQ Growth", "sales_growth_qoq"),
                ("EBITDA", "ebitda"),
                ("Margin", "margin"),
                ("EBIT", "ebit"),
                ("PBT", "pbt"),
                ("Reported PAT", "reported_pat"),
                ("Adj PAT", "adjusted_pat"),
                ("Adj EPS", "adjusted_eps"),
            ]

            for label, attr in metrics:

                row = [label]

                for item in self.report.quarterly_financials:
                    row.append(
                        getattr(item, attr, None)
                    )

                rows.append(row)

            story.append(
                self._styled_table(
                    financial_table(
                        headers,
                        rows,
                    )
                )
            )

        # -----------------------------------------------------
        # Annual Financial Summary
        # -----------------------------------------------------

        story.append(self._section("Annual Financial Summary"))

        headers = ["Metric"]

        for item in self.report.annual_financials:
            headers.append(item.year)

        rows = []

        metrics = [
            ("Sales", "sales"),
            ("Growth %", "sales_growth"),
            ("EBITDA", "ebitda"),
            ("Margin %", "ebitda_margin"),
            ("Adj PAT", "adjusted_pat"),
            ("PAT Growth %", "pat_growth"),
            ("Adj EPS", "adjusted_eps"),
            ("EPS Growth %", "eps_growth"),
        ]

        for label, attr in metrics:

            row = [label]

            for item in self.report.annual_financials:
                row.append(
                    getattr(item, attr, None)
                )

            rows.append(row)

        story.append(
            financial_table(
                headers,
                rows,
            )
        )

        return story

    # =========================================================
    # PAGE 2
    # =========================================================

    def page_two(self):

        story = []

        story.append(
            Paragraph(
                "Estimates & Key Highlights",
                TITLE_STYLE,
            )
        )

        if self.report.business_summary:
            story.append(
                self._callout(
                    "BUSINESS SUMMARY",
                    self.report.business_summary,
                    accent=PURPLE,
                    background=PURPLE_LIGHT,
                )
            )
            story.append(Spacer(1, 2 * mm))

        # -----------------------------------------------------
        # Estimate Changes
        # -----------------------------------------------------

        if self.report.estimate_changes:

            story.append(self._section("Old Estimates vs New Estimates"))

            headers = [
                "Metric",
                "Old FY26E",
                "Old FY27E",
                "New FY26E",
                "New FY27E",
                "Change FY26E",
                "Change FY27E",
            ]

            rows = []

            for item in self.report.estimate_changes:

                rows.append(
                    [
                        item.metric,
                        item.old_fy26e,
                        item.old_fy27e,
                        item.new_fy26e,
                        item.new_fy27e,
                        item.change_fy26e,
                        item.change_fy27e,
                    ]
                )

            story.append(
                self._styled_table(
                    financial_table(
                        headers,
                        rows,
                    )
                )
            )

        # -----------------------------------------------------
        # Highlights
        # -----------------------------------------------------

        story.append(self._section("Key Highlights", GOLD))

        for highlight in self.report.key_highlights:
            story.append(
                self._callout(
                    "KEY HIGHLIGHT",
                    highlight,
                    accent=GOLD,
                    background=GOLD_LIGHT,
                )
            )
            story.append(Spacer(1, 1.2 * mm))

        # -----------------------------------------------------
        # Charts
        # -----------------------------------------------------

        chart_paths = self._generate_charts()

        if chart_paths:

            story.append(self._section("Financial Charts"))

            for path in chart_paths:

                story.append(
                    Image(
                        path,
                        width=85 * mm,
                        height=40 * mm,
                    )
                )

                story.append(
                    Spacer(1, 2 * mm)
                )

        return story

    # =========================================================
    # PAGE 3
    # =========================================================

    def page_three(self):

        story = []

        story.append(
            Paragraph(
                "Consolidated Financials",
                TITLE_STYLE,
            )
        )

        # P&L
        if self.report.profit_loss:

            story.append(self._section("Profit & Loss"))

            headers = [
                "Metric"
            ]

            for item in self.report.profit_loss:
                headers.append(item.year)

            metrics = [
                ("Sales", "sales"),
                ("Growth %", "sales_growth"),
                ("EBITDA", "ebitda"),
                ("EBITDA Growth %", "ebitda_growth"),
                ("Depreciation", "depreciation"),
                ("EBIT", "ebit"),
                ("Interest", "interest"),
                ("Other Income", "other_income"),
                ("PBT", "pbt"),
                ("PBT Growth %", "pbt_growth"),
                ("Tax", "tax"),
                ("Tax Rate %", "tax_rate"),
                ("Reported PAT", "reported_pat"),
                ("Adj PAT", "adjusted_pat"),
                ("Adj EPS", "adjusted_eps"),
                ("EPS Growth %", "eps_growth"),
                ("DPS", "dps"),
            ]

            rows = []

            for label, attr in metrics:

                row = [label]

                for item in self.report.profit_loss:
                    row.append(
                        getattr(item, attr, None)
                    )

                rows.append(row)

            story.append(
                self._styled_table(
                    financial_table(
                        headers,
                        rows,
                    )
                )
            )

        # Balance Sheet
        if self.report.balance_sheet:

            story.append(self._section("Balance Sheet"))

            headers = ["Metric"]

            for item in self.report.balance_sheet:
                headers.append(item.year)

            metrics = [
                ("Cash", "cash"),
                ("Accounts Receivable", "accounts_receivable"),
                ("Inventories", "inventories"),
                ("Investments", "investments"),
                ("Gross Fixed Assets", "gross_fixed_assets"),
                ("Net Fixed Assets", "net_fixed_assets"),
                ("CWIP", "cwip"),
                ("Intangible Assets", "intangible_assets"),
                ("Total Assets", "total_assets"),
                ("Current Liabilities", "current_liabilities"),
                ("Debt Funds", "debt_funds"),
                ("Equity Capital", "equity_capital"),
                ("Reserves & Surplus", "reserves_surplus"),
                ("Shareholder Funds", "shareholder_funds"),
                ("Total Liabilities", "total_liabilities"),
                ("BVPS", "bvps"),
            ]

            rows = []

            for label, attr in metrics:

                row = [label]

                for item in self.report.balance_sheet:
                    row.append(
                        getattr(item, attr, None)
                    )

                rows.append(row)

            story.append(
                self._styled_table(
                    financial_table(
                        headers,
                        rows,
                    )
                )
            )

        # Cash Flow
        if self.report.cash_flow:

            story.append(self._section("Cash Flow"))

            headers = ["Metric"]

            for item in self.report.cash_flow:
                headers.append(item.year)

            metrics = [
                ("CFO", "cash_flow_operations"),
                ("Capex", "capital_expenditure"),
                ("CF Investment", "cash_flow_investment"),
                ("CF Finance", "cash_flow_finance"),
                ("Change in Cash", "change_in_cash"),
                ("Closing Cash", "closing_cash"),
            ]

            rows = []

            for label, attr in metrics:

                row = [label]

                for item in self.report.cash_flow:
                    row.append(
                        getattr(item, attr, None)
                    )

                rows.append(row)

            story.append(
                self._styled_table(
                    financial_table(
                        headers,
                        rows,
                    )
                )
            )

        # Ratios
        if self.report.ratios:

            story.append(self._section("Ratios"))

            headers = ["Metric"]

            for item in self.report.ratios:
                headers.append(item.year)

            metrics = [
                ("EBITDA Margin", "ebitda_margin"),
                ("EBIT Margin", "ebit_margin"),
                ("Net Profit Margin", "net_profit_margin"),
                ("ROE", "roe"),
                ("ROCE", "roce"),
                ("Receivables Days", "receivables_days"),
                ("Inventory Days", "inventory_days"),
                ("Payables Days", "payables_days"),
                ("Current Ratio", "current_ratio"),
                ("Quick Ratio", "quick_ratio"),
                ("Debt / Equity", "debt_equity"),
                ("EV / Sales", "ev_sales"),
                ("EV / EBITDA", "ev_ebitda"),
                ("P / E", "pe"),
                ("P / BV", "pbv"),
            ]

            rows = []

            for label, attr in metrics:

                row = [label]

                for item in self.report.ratios:
                    row.append(
                        getattr(item, attr, None)
                    )

                rows.append(row)

            story.append(
                self._styled_table(
                    financial_table(
                        headers,
                        rows,
                    )
                )
            )

        return story

    # =========================================================
    # PAGE 4
    # =========================================================

    def page_four(self):

        story = []

        story.append(
            Paragraph(
                "Recommendation Summary",
                TITLE_STYLE,
            )
        )

        if self.report.recommendation_history:

            headers = [
                "Date",
                "Rating",
                "Target",
            ]

            rows = []

            for item in self.report.recommendation_history:

                rows.append(
                    [
                        item.date,
                        item.rating,
                        item.target,
                    ]
                )

            story.append(
                self._styled_table(
                    financial_table(
                        headers,
                        rows,
                    )
                )
            )

        story.append(self._section("Investment Rating Criteria"))

        rating_text = """
        <b>Buy:</b> Expected upside generally above the prescribed
        investment threshold.<br/>
        <b>Accumulate:</b> Moderate expected upside with positive
        risk-reward characteristics.<br/>
        <b>Hold:</b> Limited expected upside or balanced risk-reward.<br/>
        <b>Reduce / Sell:</b> Expected downside or unfavourable
        risk-reward.<br/>
        <b>Not Rated:</b> Insufficient basis for a formal rating.
        """

        story.append(
            Paragraph(
                rating_text,
                BODY_STYLE,
            )
        )

        if self.report.risks:

            story.append(self._section("Risks", RED))

            for risk in self.report.risks:
                story.append(
                    self._callout(
                        "RISK",
                        risk,
                        accent=RED,
                        background=RED_LIGHT,
                    )
                )
                story.append(Spacer(1, 1.2 * mm))

        story.append(self._section("Disclaimer & Disclosures", NAVY))

        story.append(
            self._callout(
                "AI-GENERATED RESEARCH",
                "This report is generated from information available in the supplied source document. "
                "Missing information is not independently estimated. Review the report before external distribution.",
                accent=BLUE,
                background=BLUE_LIGHT,
            )
        )

        return story

    # =========================================================
    # CHARTS
    # =========================================================

    def _generate_charts(self):

        os.makedirs(
            self.chart_dir,
            exist_ok=True,
        )

        charts = []

        annual = self.report.annual_financials

        if not annual:
            return charts

        categories = [
            item.year
            for item in annual
        ]

        # Revenue
        revenue_path = os.path.join(
            self.chart_dir,
            "revenue.png",
        )

        create_financial_chart(
            title="Revenue",
            categories=categories,
            values=[
                item.sales
                for item in annual
            ],
            secondary_values=[
                item.sales_growth
                for item in annual
            ],
            primary_label="Sales",
            secondary_label="Growth %",
            output_path=revenue_path,
        )

        charts.append(revenue_path)

        # EBITDA
        ebitda_path = os.path.join(
            self.chart_dir,
            "ebitda.png",
        )

        create_financial_chart(
            title="EBITDA",
            categories=categories,
            values=[
                item.ebitda
                for item in annual
            ],
            secondary_values=[
                item.ebitda_margin
                for item in annual
            ],
            primary_label="EBITDA",
            secondary_label="Margin %",
            output_path=ebitda_path,
        )

        charts.append(ebitda_path)

        # PAT
        pat_path = os.path.join(
            self.chart_dir,
            "pat.png",
        )

        create_financial_chart(
            title="Adjusted PAT",
            categories=categories,
            values=[
                item.adjusted_pat
                for item in annual
            ],
            secondary_values=[
                item.pat_growth
                for item in annual
            ],
            primary_label="PAT",
            secondary_label="Growth %",
            output_path=pat_path,
        )

        charts.append(pat_path)

        return charts

    # =========================================================
    # FORMATTING
    # =========================================================

    @staticmethod
    def _rs(value):

        if value is None:
            return "-"

        return f"Rs.{value:g}"

    @staticmethod
    def _pct(value):

        if value is None:
            return "-"

        return f"{value:g}%"