from typing import Optional

from pydantic import BaseModel, Field


class CompanyInfo(BaseModel):
    name: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None

    stock_type: Optional[str] = None
    bloomberg_code: Optional[str] = None
    sensex_code: Optional[str] = None
    nse_code: Optional[str] = None
    bse_code: Optional[str] = None

    time_frame: Optional[str] = None


class Recommendation(BaseModel):
    rating: Optional[str] = None
    target_price: Optional[float] = None
    current_price: Optional[float] = None
    expected_return: Optional[float] = None

    key_change_target: Optional[str] = None
    key_change_rating: Optional[str] = None
    key_change_earnings: Optional[str] = None


class CompanyData(BaseModel):
    market_cap: Optional[float] = None
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None

    enterprise_value: Optional[float] = None
    outstanding_shares: Optional[float] = None
    free_float_percent: Optional[float] = None

    dividend_yield_percent: Optional[float] = None
    average_volume_6m: Optional[float] = None

    beta: Optional[float] = None
    face_value: Optional[float] = None


class ShareholdingPeriod(BaseModel):
    period: Optional[str] = None

    promoters: Optional[float] = None
    fiis: Optional[float] = None
    mutual_funds_institutions: Optional[float] = None
    public: Optional[float] = None
    others: Optional[float] = None

    total: Optional[float] = None
    promoter_pledge: Optional[str] = None


class PricePerformance(BaseModel):
    absolute_return_3m: Optional[float] = None
    absolute_return_6m: Optional[float] = None
    absolute_return_1y: Optional[float] = None

    sensex_return_3m: Optional[float] = None
    sensex_return_6m: Optional[float] = None
    sensex_return_1y: Optional[float] = None

    relative_return_3m: Optional[float] = None
    relative_return_6m: Optional[float] = None
    relative_return_1y: Optional[float] = None


class AnnualFinancialSummary(BaseModel):
    year: Optional[str] = None

    sales: Optional[float] = None
    sales_growth: Optional[float] = None

    ebitda: Optional[float] = None
    ebitda_margin: Optional[float] = None

    adjusted_pat: Optional[float] = None
    pat_growth: Optional[float] = None

    adjusted_eps: Optional[float] = None
    eps_growth: Optional[float] = None

    pe: Optional[float] = None
    pb: Optional[float] = None
    ev_ebitda: Optional[float] = None

    roe: Optional[float] = None
    debt_equity: Optional[float] = None



class QuarterlyFinancial(BaseModel):
    period: Optional[str] = None

    sales: Optional[float] = None
    sales_growth_yoy: Optional[float] = None
    sales_growth_qoq: Optional[float] = None

    ebitda: Optional[float] = None
    ebitda_growth_yoy: Optional[float] = None
    ebitda_growth_qoq: Optional[float] = None

    margin: Optional[float] = None
    margin_change_yoy_bps: Optional[float] = None
    margin_change_qoq_bps: Optional[float] = None

    ebit: Optional[float] = None
    ebit_growth_yoy: Optional[float] = None
    ebit_growth_qoq: Optional[float] = None

    pbt: Optional[float] = None
    pbt_growth_yoy: Optional[float] = None
    pbt_growth_qoq: Optional[float] = None

    reported_pat: Optional[float] = None
    reported_pat_growth_yoy: Optional[float] = None
    reported_pat_growth_qoq: Optional[float] = None

    adjusted_pat: Optional[float] = None
    adjusted_pat_growth_yoy: Optional[float] = None
    adjusted_pat_growth_qoq: Optional[float] = None

    adjusted_eps: Optional[float] = None
    adjusted_eps_growth_yoy: Optional[float] = None
    adjusted_eps_growth_qoq: Optional[float] = None


class ProfitLoss(BaseModel):
    year: Optional[str] = None

    sales: Optional[float] = None
    sales_growth: Optional[float] = None

    ebitda: Optional[float] = None
    ebitda_growth: Optional[float] = None

    depreciation: Optional[float] = None

    ebit: Optional[float] = None

    interest: Optional[float] = None

    other_income: Optional[float] = None

    pbt: Optional[float] = None
    pbt_growth: Optional[float] = None

    tax: Optional[float] = None
    tax_rate: Optional[float] = None

    reported_pat: Optional[float] = None
    pat_attributable_to_common_shareholders: Optional[float] = None

    adjusted_pat: Optional[float] = None
    adjusted_pat_growth: Optional[float] = None

    number_of_shares: Optional[float] = None

    adjusted_eps: Optional[float] = None
    eps_growth: Optional[float] = None

    dps: Optional[float] = None



class BalanceSheet(BaseModel):
    year: Optional[str] = None

    cash: Optional[float] = None
    accounts_receivable: Optional[float] = None
    inventories: Optional[float] = None
    other_current_assets: Optional[float] = None
    investments: Optional[float] = None

    gross_fixed_assets: Optional[float] = None
    net_fixed_assets: Optional[float] = None

    cwip: Optional[float] = None
    intangible_assets: Optional[float] = None

    deferred_tax_net: Optional[float] = None
    other_assets: Optional[float] = None

    total_assets: Optional[float] = None

    current_liabilities: Optional[float] = None
    provisions: Optional[float] = None
    debt_funds: Optional[float] = None
    other_liabilities: Optional[float] = None

    equity_capital: Optional[float] = None
    reserves_surplus: Optional[float] = None

    shareholder_funds: Optional[float] = None
    minority_interest: Optional[float] = None

    total_liabilities: Optional[float] = None

    bvps: Optional[float] = None


class CashFlow(BaseModel):
    year: Optional[str] = None

    net_income_depreciation: Optional[float] = None
    non_cash_adjustments: Optional[float] = None
    other_adjustments: Optional[float] = None
    changes_in_working_capital: Optional[float] = None

    cash_flow_operations: Optional[float] = None

    capital_expenditure: Optional[float] = None
    change_in_investments: Optional[float] = None
    other_investing_cash_flow: Optional[float] = None

    cash_flow_investment: Optional[float] = None

    issue_of_equity: Optional[float] = None
    issue_repayment_debt: Optional[float] = None
    dividends_paid: Optional[float] = None
    other_financing_cash_flow: Optional[float] = None

    cash_flow_finance: Optional[float] = None

    change_in_cash: Optional[float] = None
    closing_cash: Optional[float] = None


class FinancialRatios(BaseModel):
    year: Optional[str] = None

    ebitda_margin: Optional[float] = None
    ebit_margin: Optional[float] = None
    net_profit_margin: Optional[float] = None

    roe: Optional[float] = None
    roce: Optional[float] = None

    receivables_days: Optional[float] = None
    inventory_days: Optional[float] = None
    payables_days: Optional[float] = None

    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None

    gross_asset_turnover: Optional[float] = None
    total_asset_turnover: Optional[float] = None

    interest_coverage_ratio: Optional[float] = None
    debt_equity: Optional[float] = None

    ev_sales: Optional[float] = None
    ev_ebitda: Optional[float] = None
    pe: Optional[float] = None
    pbv: Optional[float] = None


class EstimateChange(BaseModel):
    metric: Optional[str] = None

    old_fy26e: Optional[float] = None
    old_fy27e: Optional[float] = None

    new_fy26e: Optional[float] = None
    new_fy27e: Optional[float] = None

    change_fy26e: Optional[float] = None
    change_fy27e: Optional[float] = None


class ChartData(BaseModel):
    title: Optional[str] = None

    categories: list[str] = Field(
        default_factory=list
    )

    values: list[Optional[float]] = Field(
        default_factory=list
    )

    secondary_values: list[Optional[float]] = Field(
        default_factory=list
    )

    primary_label: Optional[str] = None
    secondary_label: Optional[str] = None


class Charts(BaseModel):
    revenue: Optional[ChartData] = None
    gross_order_value: Optional[ChartData] = None
    ebitda: Optional[ChartData] = None
    pat: Optional[ChartData] = None


class RecommendationHistory(BaseModel):
    date: Optional[str] = None
    rating: Optional[str] = None
    target: Optional[float] = None


class FinancialReport(BaseModel):

    company: CompanyInfo = Field(
        default_factory=CompanyInfo
    )

    recommendation: Recommendation = Field(
        default_factory=Recommendation
    )

    company_data: CompanyData = Field(
        default_factory=CompanyData
    )

    shareholding: list[ShareholdingPeriod] = Field(
        default_factory=list
    )

    price_performance: PricePerformance = Field(
        default_factory=PricePerformance
    )

    annual_financials: list[AnnualFinancialSummary] = Field(
        default_factory=list
    )

    quarterly_financials: list[QuarterlyFinancial] = Field(
        default_factory=list
    )

    outlook_valuation: Optional[str] = None

    business_summary: Optional[str] = None

    key_highlights: list[str] = Field(
        default_factory=list
    )

    risks: list[str] = Field(
        default_factory=list
    )

    estimate_changes: list[EstimateChange] = Field(
        default_factory=list
    )

    charts: Charts = Field(
        default_factory=Charts
    )

    profit_loss: list[ProfitLoss] = Field(
        default_factory=list
    )

    balance_sheet: list[BalanceSheet] = Field(
        default_factory=list
    )

    cash_flow: list[CashFlow] = Field(
        default_factory=list
    )

    ratios: list[FinancialRatios] = Field(
        default_factory=list
    )

    recommendation_history: list[RecommendationHistory] = Field(
        default_factory=list
    )