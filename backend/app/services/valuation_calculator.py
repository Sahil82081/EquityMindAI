import logging
from typing import Optional
from app.schemas.financial import FinancialData
from app.schemas.valuation import (
    ValuationMetric,
    HistoricalValuationComparison,
    ValuationAnalysis,
)
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)

# Established 5-year historical average P/E baselines for prominent tickers, with 24.0x market baseline default
_HISTORICAL_PE_BASELINES: dict[str, float] = {
    "AAPL": 29.5,
    "MSFT": 31.0,
    "NVDA": 42.0,
    "TSLA": 68.0,
    "AMZN": 45.0,
    "GOOGL": 24.5,
    "META": 23.0,
    "NFLX": 35.0,
    "AMD": 38.0,
    "TSM": 22.0,
}


class ValuationCalculator:
    """Performs rigorous financial valuation calculations in pure Python code."""

    def analyze(self, ticker: str, company_name: str, fin: FinancialData) -> ValuationAnalysis:
        clean_ticker = ticker.strip().upper()
        calculations_summary: list[str] = []

        # -----------------------------------------------------------------
        # 1. P/E Multiple Calculation
        # -----------------------------------------------------------------
        pe_val: Optional[float] = None
        eps = fin.fundamentals.eps
        price = fin.quote.current_price

        if price is not None and eps is not None and eps > 0:
            pe_val = round(price / eps, 2)
            pe_formula = f"Share Price (${price:.2f}) / Diluted EPS (${eps:.2f}) = {pe_val:.2f}x"
        elif fin.fundamentals.pe_ratio is not None and fin.fundamentals.pe_ratio > 0:
            pe_val = round(fin.fundamentals.pe_ratio, 2)
            pe_formula = f"Reported P/E from market fundamentals: {pe_val:.2f}x"
        else:
            pe_formula = "P/E unavailable (negative or zero reported earnings)"

        if pe_val is not None:
            if pe_val < 18.0:
                pe_assessment = "Attractive / Discounted"
                pe_exp = f"At {pe_val:.1f}x earnings, the stock trades at a notable discount to broader equity market multiples."
            elif pe_val <= 30.0:
                pe_assessment = "Moderate / Fair Valuation"
                pe_exp = f"Trading at {pe_val:.1f}x earnings reflects a balanced valuation typical of high-quality market leaders."
            elif pe_val <= 45.0:
                pe_assessment = "Growth Premium Multiple"
                pe_exp = f"A {pe_val:.1f}x P/E multiple prices in above-market earnings expansion and leaves little room for revenue deceleration."
            else:
                pe_assessment = "Significantly Stretched Multiple"
                pe_exp = f"At {pe_val:.1f}x earnings, valuation is historically elevated and demands near-perfect quarterly execution."
            pe_formatted = f"{pe_val:.1f}x"
        else:
            pe_assessment = "Unprofitable / Multiple Not Meaningful"
            pe_exp = "Company has trailing net losses or negligible EPS, making standard P/E multiple analysis non-informative."
            pe_formatted = "N/A"

        calculations_summary.append(pe_formula)

        pe_metric = ValuationMetric(
            metric_name="Trailing P/E Ratio",
            value=pe_val,
            formatted_value=pe_formatted,
            benchmark="S&P 500 median: ~22.5x; Sector peer median: ~28.0x",
            assessment=pe_assessment,
            calculation_formula=pe_formula,
            explanation=pe_exp,
        )

        # -----------------------------------------------------------------
        # 2. Revenue Growth Calculation (YoY)
        # -----------------------------------------------------------------
        rev_growth_val: Optional[float] = None
        if len(fin.revenue_history) >= 2:
            latest_rev = fin.revenue_history[-1].amount
            prior_rev = fin.revenue_history[-2].amount
            if prior_rev > 0:
                rev_growth_val = round(((latest_rev - prior_rev) / prior_rev) * 100, 2)
                growth_formula = (
                    f"({fin.revenue_history[-1].year} Rev ${latest_rev:.1f}B - "
                    f"{fin.revenue_history[-2].year} Rev ${prior_rev:.1f}B) / "
                    f"${prior_rev:.1f}B = {rev_growth_val:+.1f}%"
                )
            else:
                growth_formula = "Prior year revenue is zero or unavailable"
        elif fin.fundamentals.revenue_growth is not None:
            rev_growth_val = round(fin.fundamentals.revenue_growth * 100, 2)
            growth_formula = f"Direct filing YoY Revenue Growth: {rev_growth_val:+.1f}%"
        else:
            growth_formula = "Multi-year revenue history unavailable"

        if rev_growth_val is not None:
            if rev_growth_val >= 20.0:
                growth_assessment = "High-Growth Expansion"
                growth_exp = f"YoY top-line growth of {rev_growth_val:+.1f}% demonstrates rapid commercial scale and market share gains."
            elif rev_growth_val >= 10.0:
                growth_assessment = "Solid Steady Growth"
                growth_exp = f"Revenue growth of {rev_growth_val:+.1f}% comfortably outpaces broad GDP growth, sustaining corporate reinvestment."
            elif rev_growth_val >= 0.0:
                growth_assessment = "Moderate / Mature Growth"
                growth_exp = f"Moderate revenue growth of {rev_growth_val:+.1f}% indicates business maturation, prioritizing margin efficiency."
            else:
                growth_assessment = "Contraction"
                growth_exp = f"Top-line contraction of {rev_growth_val:+.1f}% highlights cyclical headwinds or demand slowdown."
            growth_formatted = f"{rev_growth_val:+.1f}%"
        else:
            growth_assessment = "Data Unavailable"
            growth_exp = "Revenue growth history is incomplete."
            growth_formatted = "N/A"

        calculations_summary.append(growth_formula)

        growth_metric = ValuationMetric(
            metric_name="YoY Revenue Growth",
            value=rev_growth_val,
            formatted_value=growth_formatted,
            benchmark="Large-cap median: +7.5% - +10.0%",
            assessment=growth_assessment,
            calculation_formula=growth_formula,
            explanation=growth_exp,
        )

        # -----------------------------------------------------------------
        # 3. Operating Margin Calculation
        # -----------------------------------------------------------------
        op_margin_val: Optional[float] = None
        if fin.fundamentals.operating_margin is not None:
            op_margin_val = round(fin.fundamentals.operating_margin * 100, 2)
            op_formula = f"Operating Income / Total Revenue = {op_margin_val:.1f}%"
        else:
            op_formula = "Operating margin figures not disclosed"

        if op_margin_val is not None:
            if op_margin_val >= 30.0:
                op_assessment = "Exceptional Operating Leverage"
                op_exp = f"Operating margin of {op_margin_val:.1f}% shows industry-leading cost control and pricing power."
            elif op_margin_val >= 15.0:
                op_assessment = "Healthy Operating Efficiency"
                op_exp = f"Operating margin of {op_margin_val:.1f}% represents healthy core business profitability."
            elif op_margin_val >= 5.0:
                op_assessment = "Average Operating Margin"
                op_exp = f"Operating margin of {op_margin_val:.1f}% aligns with capital-intensive or competitive industry baselines."
            else:
                op_assessment = "Compressed Margin"
                op_exp = f"Operating margin of {op_margin_val:.1f}% leaves limited buffer against rising operating costs."
            op_formatted = f"{op_margin_val:.1f}%"
        else:
            op_assessment = "Data Unavailable"
            op_exp = "Operating margin data is unavailable."
            op_formatted = "N/A"

        calculations_summary.append(op_formula)

        op_metric = ValuationMetric(
            metric_name="Operating Margin",
            value=op_margin_val,
            formatted_value=op_formatted,
            benchmark="S&P 500 average: ~12.5%; Tech leaders: ~25.0%+",
            assessment=op_assessment,
            calculation_formula=op_formula,
            explanation=op_exp,
        )

        # -----------------------------------------------------------------
        # 4. Net Margin Calculation
        # -----------------------------------------------------------------
        net_margin_val: Optional[float] = None
        if fin.fundamentals.net_margin is not None:
            net_margin_val = round(fin.fundamentals.net_margin * 100, 2)
            net_formula = f"Net Income / Total Revenue = {net_margin_val:.1f}%"
        elif fin.fundamentals.revenue and fin.fundamentals.net_income and fin.fundamentals.revenue > 0:
            net_margin_val = round((fin.fundamentals.net_income / fin.fundamentals.revenue) * 100, 2)
            net_formula = f"Net Income (${fin.fundamentals.net_income/1e9:.1f}B) / Revenue (${fin.fundamentals.revenue/1e9:.1f}B) = {net_margin_val:.1f}%"
        else:
            net_formula = "Net income or revenue data incomplete"

        if net_margin_val is not None:
            if net_margin_val >= 25.0:
                net_assessment = "Elite Profit Conversion"
                net_exp = f"Net margin of {net_margin_val:.1f}% reflects exceptional translation of top-line revenue into bottom-line profit."
            elif net_margin_val >= 12.0:
                net_assessment = "Strong Profitability"
                net_exp = f"Net margin of {net_margin_val:.1f}% delivers solid returns to equity holders."
            elif net_margin_val >= 4.0:
                net_assessment = "Moderate Profitability"
                net_exp = f"Net margin of {net_margin_val:.1f}% provides stable but modest net earnings conversion."
            else:
                net_assessment = "Thin Margin"
                net_exp = f"Net margin of {net_margin_val:.1f}% provides minimal cushion against interest or tax shifts."
            net_formatted = f"{net_margin_val:.1f}%"
        else:
            net_assessment = "Data Unavailable"
            net_exp = "Net margin figures unavailable."
            net_formatted = "N/A"

        calculations_summary.append(net_formula)

        net_metric = ValuationMetric(
            metric_name="Net Profit Margin",
            value=net_margin_val,
            formatted_value=net_formatted,
            benchmark="Broad market median: ~9.5%; Premium franchises: ~20.0%+",
            assessment=net_assessment,
            calculation_formula=net_formula,
            explanation=net_exp,
        )

        # -----------------------------------------------------------------
        # 5. Historical Valuation Comparison
        # -----------------------------------------------------------------
        hist_baseline = _HISTORICAL_PE_BASELINES.get(clean_ticker, 24.0)
        variance_pct: Optional[float] = None
        if pe_val is not None and hist_baseline > 0:
            variance_pct = round(((pe_val - hist_baseline) / hist_baseline) * 100, 1)
            hist_context = f"Trading at a {abs(variance_pct):.1f}% {'premium' if variance_pct >= 0 else 'discount'} to its 5-year baseline ({hist_baseline:.1f}x)"
            hist_formula = f"(Current P/E {pe_val:.1f}x - 5Y Avg {hist_baseline:.1f}x) / {hist_baseline:.1f}x = {variance_pct:+.1f}%"
            if variance_pct > 20.0:
                comp_summary = (
                    f"{clean_ticker} is commanding a significant +{variance_pct:.1f}% valuation premium relative to its historical 5-year average of {hist_baseline:.1f}x. "
                    "This multiple expansion reflects high market confidence but heightens sensitivity to any quarterly earnings misses."
                )
            elif variance_pct >= -10.0:
                comp_summary = (
                    f"{clean_ticker} is trading in-line with its historical 5-year valuation norm of {hist_baseline:.1f}x (variance {variance_pct:+.1f}%). "
                    "The current pricing reflects balanced multi-year expectations without extreme multiple distortion."
                )
            else:
                comp_summary = (
                    f"{clean_ticker} is trading at a {abs(variance_pct):.1f}% discount to its 5-year historical average of {hist_baseline:.1f}x. "
                    "This multiple compression presents potential upside if earnings momentum stabilizes."
                )
        else:
            hist_context = "Historical multiple comparison unavailable"
            hist_formula = "Historical P/E baseline not established"
            comp_summary = "Historical valuation multiple comparison cannot be calculated due to unavailable baseline or earnings data."

        calculations_summary.append(hist_formula)

        historical_comp = HistoricalValuationComparison(
            metric="P/E Multiple vs 5-Year Historical Average",
            current_value=pe_formatted,
            historical_benchmark=f"5-Year Average: ~{hist_baseline:.1f}x",
            variance_percent=variance_pct,
            historical_context=hist_context,
            comparison_summary=comp_summary,
        )

        # -----------------------------------------------------------------
        # 6. Composite Valuation Score & Classification
        # -----------------------------------------------------------------
        score = 65  # Baseline neutral score
        if pe_val is not None:
            # Lower P/E yields higher value score; high P/E reduces score
            if pe_val < 20.0:
                score += 15
            elif pe_val > 40.0:
                score -= 15
            elif pe_val > 30.0:
                score -= 8

        if rev_growth_val is not None:
            if rev_growth_val >= 15.0:
                score += 12
            elif rev_growth_val >= 8.0:
                score += 6
            elif rev_growth_val < 0.0:
                score -= 10

        if op_margin_val is not None:
            if op_margin_val >= 30.0:
                score += 10
            elif op_margin_val >= 20.0:
                score += 5
            elif op_margin_val < 10.0:
                score -= 8

        score = max(10, min(95, score))

        if score >= 75:
            classification = "Attractive Valuation (High Quality at Fair/Discounted Price)"
        elif score >= 55:
            classification = "Fairly Valued (Balanced Risk/Reward Multiple)"
        elif score >= 40:
            classification = "Premium / Elevated Valuation"
        else:
            classification = "Significantly Stretched Multiple (High Valuation Risk)"

        # -----------------------------------------------------------------
        # 7. Narrative Explanation & Reasoning (Gemini with Pydantic validation)
        # -----------------------------------------------------------------
        metrics_dict = {
            "pe_ratio": pe_formatted,
            "revenue_growth": growth_formatted,
            "operating_margin": op_formatted,
            "net_margin": net_formatted,
            "historical_benchmark": f"{hist_baseline:.1f}x (Variance: {variance_pct:+.1f}%)" if variance_pct is not None else "N/A",
            "classification": classification,
            "valuation_score": score,
        }

        # Reason about code-computed metrics with Gemini (validated with Pydantic)
        valuation_reasoning = llm_service.reason_valuation(clean_ticker, company_name, metrics_dict)

        return ValuationAnalysis(
            ticker=clean_ticker,
            company_name=company_name,
            pe_ratio=pe_metric,
            revenue_growth=growth_metric,
            operating_margin=op_metric,
            net_margin=net_metric,
            historical_comparison=historical_comp,
            valuation_score=score,
            valuation_classification=classification,
            executive_explanation=valuation_reasoning.executive_summary,
            calculations_summary=calculations_summary,
            reasoning=valuation_reasoning,
        )


valuation_calculator = ValuationCalculator()
