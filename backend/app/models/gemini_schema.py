from typing import Optional
from pydantic import BaseModel


class GeminiCompany(BaseModel):
    name: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None


class GeminiRecommendation(BaseModel):
    rating: Optional[str] = None
    target_price: Optional[float] = None
    current_price: Optional[float] = None
    expected_return: Optional[float] = None


class GeminiCompanyData(BaseModel):
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


class GeminiAnnualFinancial(BaseModel):
    year: Optional[str] = None
    sales: Optional[float] = None
    sales_growth: Optional[float] = None
    ebitda: Optional[float] = None
    ebitda_margin: Optional[float] = None
    adjusted_pat: Optional[float] = None
    pat_growth: Optional[float] = None
    adjusted_eps: Optional[float] = None
    eps_growth: Optional[float] = None


class GeminiQuarterlyFinancial(BaseModel):
    period: Optional[str] = None
    sales: Optional[float] = None
    sales_growth_yoy: Optional[float] = None
    sales_growth_qoq: Optional[float] = None
    ebitda: Optional[float] = None
    margin: Optional[float] = None
    ebit: Optional[float] = None
    pbt: Optional[float] = None
    reported_pat: Optional[float] = None
    adjusted_pat: Optional[float] = None
    adjusted_eps: Optional[float] = None


class GeminiShareholding(BaseModel):
    period: Optional[str] = None
    promoters: Optional[float] = None
    fiis: Optional[float] = None
    mutual_funds_institutions: Optional[float] = None
    public: Optional[float] = None
    others: Optional[float] = None
    total: Optional[float] = None


class GeminiChart(BaseModel):
    title: Optional[str] = None
    categories: list[str] = []
    values: list[Optional[float]] = []
    secondary_values: list[Optional[float]] = []


class GeminiFinancialExtraction(BaseModel):
    company: GeminiCompany
    recommendation: GeminiRecommendation
    company_data: GeminiCompanyData

    shareholding: list[GeminiShareholding] = []

    price_performance: Optional[GeminiPricePerformance] = None

    annual_financials: list[GeminiAnnualFinancial] = []

    quarterly_financials: list[GeminiQuarterlyFinancial] = []

    outlook_valuation: Optional[str] = None

    business_summary: Optional[str] = None

    key_highlights: list[str] = []

    risks: list[str] = []

    estimate_changes: list[GeminiEstimateChange] = []

    profit_loss: list[GeminiProfitLoss] = []

    balance_sheet: list[GeminiBalanceSheet] = []

    cash_flow: list[GeminiCashFlow] = []

    ratios: list[GeminiRatio] = []

    charts: list[GeminiChart] = []

    recommendation_history: list[GeminiRecommendationHistory] = []


class GeminiEstimateChange(BaseModel):
    metric: Optional[str] = None
    old_fy26e: Optional[float] = None
    old_fy27e: Optional[float] = None
    new_fy26e: Optional[float] = None
    new_fy27e: Optional[float] = None
    change_fy26e: Optional[float] = None
    change_fy27e: Optional[float] = None


class GeminiProfitLoss(BaseModel):
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
    adjusted_pat: Optional[float] = None
    adjusted_pat_growth: Optional[float] = None

    number_of_shares: Optional[float] = None

    adjusted_eps: Optional[float] = None
    eps_growth: Optional[float] = None

    dps: Optional[float] = None


class GeminiBalanceSheet(BaseModel):
    year: Optional[str] = None
    cash: Optional[float] = None
    accounts_receivable: Optional[float] = None
    inventories: Optional[float] = None
    investments: Optional[float] = None
    gross_fixed_assets: Optional[float] = None
    net_fixed_assets: Optional[float] = None
    cwip: Optional[float] = None
    intangible_assets: Optional[float] = None
    total_assets: Optional[float] = None
    current_liabilities: Optional[float] = None
    debt_funds: Optional[float] = None
    equity_capital: Optional[float] = None
    reserves_surplus: Optional[float] = None
    shareholder_funds: Optional[float] = None
    total_liabilities: Optional[float] = None
    bvps: Optional[float] = None


class GeminiRatio(BaseModel):
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
    debt_equity: Optional[float] = None
    ev_sales: Optional[float] = None
    ev_ebitda: Optional[float] = None
    pe: Optional[float] = None
    pbv: Optional[float] = None


class GeminiPricePerformance(BaseModel):
    absolute_return_3m: Optional[float] = None
    absolute_return_6m: Optional[float] = None
    absolute_return_1y: Optional[float] = None
    sensex_return_3m: Optional[float] = None
    sensex_return_6m: Optional[float] = None
    sensex_return_1y: Optional[float] = None
    relative_return_3m: Optional[float] = None
    relative_return_6m: Optional[float] = None
    relative_return_1y: Optional[float] = None


class GeminiCashFlow(BaseModel):
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


class GeminiRecommendationHistory(BaseModel):
    date: Optional[str] = None
    rating: Optional[str] = None
    target: Optional[float] = None