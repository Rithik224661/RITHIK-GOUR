from typing import Dict, Any
import re


class LanguageResolutionAgent:
    """Resolve user's natural language into an internal query plan.

    Very lightweight rule-based parser for demo. In production this would use an LLM
    or a small semantic parser.
    """

    def resolve(self, text: str) -> Dict[str, Any]:
        t = text.lower().strip()
        if any(x in t for x in ["summarize", "summary", "overview", "insights"]):
            return {"mode": "summarize"}
        # detect time filters
        time_match = re.search(r"q([1-4])(?:[\s,-]*\s?(\d{4}))?", t)
        if "which" in t or "which product" in t or "underperform" in t or "who" in t:
            return {"mode": "query", "intent": "which_product_underperform", "raw": text, "time_match": time_match.groups() if time_match else None}
        return {"mode": "query", "intent": "general", "raw": text}


class DataExtractionAgent:
    """Execute structured queries against the DataLayer based on the resolved plan."""

    def __init__(self, data_layer):
        self.data_layer = data_layer

    def extract(self, plan: Dict[str, Any]):
        mode = plan.get("mode")
        if mode == "summarize":
            # run a few summary queries
            top_cats = self.data_layer.sample_top_categories(3)
            by_region = self.data_layer.total_sales_by_region()
            return {"top_categories": top_cats, "by_region": by_region}

        intent = plan.get("intent")
        if intent == "which_product_underperform":
            # naive underperform logic: compare average quarter sales per product
            # Ensure the `date` column (likely a string) is parsed to DATE before extracting
            # DuckDB prefers date_part('unit', DATE) where date needs to be DATE/TIMESTAMP
            q = (
                "SELECT product_line, date_part('year', CAST(date AS DATE)) AS year, "
                "date_part('quarter', CAST(date AS DATE)) AS qtr, SUM(sales) as total_sales "
                "FROM sales GROUP BY 1,2,3 ORDER BY total_sales ASC LIMIT 10;"
            )
            df = self.data_layer.query(q)
            return {"underperform_candidates": df}

        # default: return top categories
        return {"top_categories": self.data_layer.sample_top_categories(5)}


class ValidationAgent:
    """Validate the extracted dataset(s) for quality and completeness before presenting to user.

    Example checks: Are results empty, does dataset contain major columns, are numerics sane, etc.
    """

    def validate(self, extraction_result: Dict[str, Any]) -> Dict[str, Any]:
        errors = []
        for k, v in extraction_result.items():
            if v is None:
                errors.append(f"{k} is empty")
            # DataFrame detection
            try:
                import pandas as pd

                if isinstance(v, pd.DataFrame) and v.empty:
                    errors.append(f"{k} dataframe is empty")
            except Exception:
                pass

        return {"errors": errors, "ok": len(errors) == 0}
