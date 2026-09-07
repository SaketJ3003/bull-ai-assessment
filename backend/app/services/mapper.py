from app.models.gemini_schema import GeminiFinancialExtraction

from app.models.financial import (
    FinancialReport,
    CompanyInfo,
    Recommendation,
    CompanyData,
    ShareholdingPeriod,
    PricePerformance,
    AnnualFinancialSummary,
    QuarterlyFinancial,
    EstimateChange,
    ProfitLoss,
    BalanceSheet,
    CashFlow,
    FinancialRatios,
    RecommendationHistory,
    Charts
)


def map_gemini_to_financial_report(
    data: GeminiFinancialExtraction,
) -> FinancialReport:

    # =========================================================
    # COMPANY
    # =========================================================

    company = CompanyInfo(
        name=data.company.name,
        sector=data.company.sector,
        industry=data.company.industry,
    )

    # =========================================================
    # RECOMMENDATION
    # =========================================================

    recommendation = Recommendation(
        rating=data.recommendation.rating,
        target_price=data.recommendation.target_price,
        current_price=data.recommendation.current_price,
        expected_return=data.recommendation.expected_return,
    )

    # =========================================================
    # COMPANY DATA
    # =========================================================

    company_data = CompanyData(
        market_cap=data.company_data.market_cap,
        week_52_high=data.company_data.week_52_high,
        week_52_low=data.company_data.week_52_low,
        enterprise_value=data.company_data.enterprise_value,
        outstanding_shares=data.company_data.outstanding_shares,
        free_float_percent=data.company_data.free_float_percent,
        dividend_yield_percent=data.company_data.dividend_yield_percent,
        average_volume_6m=data.company_data.average_volume_6m,
        beta=data.company_data.beta,
        face_value=data.company_data.face_value,
    )

    # =========================================================
    # SHAREHOLDING
    # =========================================================

    shareholding = []

    for item in data.shareholding:

        shareholding.append(
            ShareholdingPeriod(
                period=item.period,
                promoters=item.promoters,
                fiis=item.fiis,
                mutual_funds_institutions=item.mutual_funds_institutions,
                public=item.public,
                others=item.others,
                total=item.total,
                promoter_pledge=None,
            )
        )

    # =========================================================
    # PRICE PERFORMANCE
    # =========================================================

    price_performance = PricePerformance()

    if data.price_performance:

        price_performance = PricePerformance(
            absolute_return_3m=data.price_performance.absolute_return_3m,
            absolute_return_6m=data.price_performance.absolute_return_6m,
            absolute_return_1y=data.price_performance.absolute_return_1y,
            sensex_return_3m=data.price_performance.sensex_return_3m,
            sensex_return_6m=data.price_performance.sensex_return_6m,
            sensex_return_1y=data.price_performance.sensex_return_1y,
            relative_return_3m=data.price_performance.relative_return_3m,
            relative_return_6m=data.price_performance.relative_return_6m,
            relative_return_1y=data.price_performance.relative_return_1y,
        )

    # =========================================================
    # ANNUAL FINANCIALS
    # =========================================================

    annual_financials = []

    for item in data.annual_financials:

        annual_financials.append(
            AnnualFinancialSummary(
                year=item.year,
                sales=item.sales,
                sales_growth=item.sales_growth,
                ebitda=item.ebitda,
                ebitda_margin=item.ebitda_margin,
                adjusted_pat=item.adjusted_pat,
                pat_growth=item.pat_growth,
                adjusted_eps=item.adjusted_eps,
                eps_growth=item.eps_growth,
            )
        )

    # =========================================================
    # QUARTERLY FINANCIALS
    # =========================================================

    quarterly_financials = []

    for item in data.quarterly_financials:

        quarterly_financials.append(
            QuarterlyFinancial(
                period=item.period,

                sales=item.sales,
                sales_growth_yoy=item.sales_growth_yoy,
                sales_growth_qoq=item.sales_growth_qoq,

                ebitda=item.ebitda,

                # These fields are not currently present in
                # GeminiQuarterlyFinancial, so don't invent them.
                ebitda_growth_yoy=None,
                ebitda_growth_qoq=None,

                margin=item.margin,
                margin_change_yoy_bps=None,
                margin_change_qoq_bps=None,

                ebit=item.ebit,

                ebit_growth_yoy=None,
                ebit_growth_qoq=None,

                pbt=item.pbt,

                pbt_growth_yoy=None,
                pbt_growth_qoq=None,

                reported_pat=item.reported_pat,

                reported_pat_growth_yoy=None,
                reported_pat_growth_qoq=None,

                adjusted_pat=item.adjusted_pat,

                adjusted_pat_growth_yoy=None,
                adjusted_pat_growth_qoq=None,

                adjusted_eps=item.adjusted_eps,

                adjusted_eps_growth_yoy=None,
                adjusted_eps_growth_qoq=None,
            )
        )

    # =========================================================
    # ESTIMATE CHANGES
    # =========================================================

    estimate_changes = []

    for item in data.estimate_changes:

        estimate_changes.append(
            EstimateChange(
                metric=item.metric,
                old_fy26e=item.old_fy26e,
                old_fy27e=item.old_fy27e,
                new_fy26e=item.new_fy26e,
                new_fy27e=item.new_fy27e,
                change_fy26e=item.change_fy26e,
                change_fy27e=item.change_fy27e,
            )
        )

    # =========================================================
    # PROFIT & LOSS
    # =========================================================

    profit_loss = []

    for item in data.profit_loss:

        profit_loss.append(
            ProfitLoss(
                year=item.year,

                sales=item.sales,
                sales_growth=item.sales_growth,

                ebitda=item.ebitda,
                ebitda_growth=item.ebitda_growth,

                depreciation=item.depreciation,
                ebit=item.ebit,

                interest=item.interest,
                other_income=item.other_income,

                pbt=item.pbt,
                pbt_growth=item.pbt_growth,

                tax=item.tax,
                tax_rate=item.tax_rate,

                reported_pat=item.reported_pat,

                pat_attributable_to_common_shareholders=None,

                adjusted_pat=item.adjusted_pat,
                adjusted_pat_growth=item.adjusted_pat_growth,

                number_of_shares=item.number_of_shares,

                adjusted_eps=item.adjusted_eps,
                eps_growth=item.eps_growth,

                dps=item.dps,
            )
        )

    # =========================================================
    # BALANCE SHEET
    # =========================================================

    balance_sheet = []

    for item in data.balance_sheet:

        balance_sheet.append(
            BalanceSheet(
                year=item.year,
                cash=item.cash,
                accounts_receivable=item.accounts_receivable,
                inventories=item.inventories,
                other_current_assets=None,
                investments=item.investments,
                gross_fixed_assets=item.gross_fixed_assets,
                net_fixed_assets=item.net_fixed_assets,
                cwip=item.cwip,
                intangible_assets=item.intangible_assets,
                deferred_tax_net=None,
                other_assets=None,
                total_assets=item.total_assets,
                current_liabilities=item.current_liabilities,
                provisions=None,
                debt_funds=item.debt_funds,
                other_liabilities=None,
                equity_capital=item.equity_capital,
                reserves_surplus=item.reserves_surplus,
                shareholder_funds=item.shareholder_funds,
                minority_interest=None,
                total_liabilities=item.total_liabilities,
                bvps=item.bvps,
            )
        )

    # =========================================================
    # CASH FLOW
    # =========================================================

    cash_flow = []

    for item in data.cash_flow:

        cash_flow.append(
            CashFlow(
                year=item.year,
                net_income_depreciation=item.net_income_depreciation,
                non_cash_adjustments=item.non_cash_adjustments,
                other_adjustments=item.other_adjustments,
                changes_in_working_capital=item.changes_in_working_capital,
                cash_flow_operations=item.cash_flow_operations,
                capital_expenditure=item.capital_expenditure,
                change_in_investments=item.change_in_investments,
                other_investing_cash_flow=item.other_investing_cash_flow,
                cash_flow_investment=item.cash_flow_investment,
                issue_of_equity=item.issue_of_equity,
                issue_repayment_debt=item.issue_repayment_debt,
                dividends_paid=item.dividends_paid,
                other_financing_cash_flow=item.other_financing_cash_flow,
                cash_flow_finance=item.cash_flow_finance,
                change_in_cash=item.change_in_cash,
                closing_cash=item.closing_cash,
            )
        )

    # =========================================================
    # RATIOS
    # =========================================================

    ratios = []

    for item in data.ratios:

        ratios.append(
            FinancialRatios(
                year=item.year,
                ebitda_margin=item.ebitda_margin,
                ebit_margin=item.ebit_margin,
                net_profit_margin=item.net_profit_margin,
                roe=item.roe,
                roce=item.roce,
                receivables_days=item.receivables_days,
                inventory_days=item.inventory_days,
                payables_days=item.payables_days,
                current_ratio=item.current_ratio,
                quick_ratio=item.quick_ratio,
                gross_asset_turnover=None,
                total_asset_turnover=None,
                interest_coverage_ratio=None,
                debt_equity=item.debt_equity,
                ev_sales=item.ev_sales,
                ev_ebitda=item.ev_ebitda,
                pe=item.pe,
                pbv=item.pbv,
            )
        )

    # =========================================================
    # RECOMMENDATION HISTORY
    # =========================================================

    recommendation_history = []

    for item in data.recommendation_history:

        recommendation_history.append(
            RecommendationHistory(
                date=item.date,
                rating=item.rating,
                target=item.target,
            )
        )

    # =========================================================
    # FINAL REPORT
    # =========================================================

    return FinancialReport(
        company=company,
        recommendation=recommendation,
        company_data=company_data,

        shareholding=shareholding,

        price_performance=price_performance,

        annual_financials=annual_financials,

        quarterly_financials=quarterly_financials,

        outlook_valuation=data.outlook_valuation,

        business_summary=data.business_summary,

        key_highlights=data.key_highlights,

        risks=data.risks,

        estimate_changes=estimate_changes,

        charts=Charts(),

        profit_loss=profit_loss,

        balance_sheet=balance_sheet,

        cash_flow=cash_flow,

        ratios=ratios,

        recommendation_history=recommendation_history,
    )

    return report