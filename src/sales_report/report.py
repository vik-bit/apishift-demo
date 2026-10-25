"""Monthly sales report: per-region totals, spread and a CSV export.

Written against pandas 1.x.
"""

import io

import pandas as pd

from .load import load_sales


class RegionReport:
    def __init__(self, sales: pd.DataFrame):
        self.sales = sales
        self.summary = pd.DataFrame(columns=["region", "orders", "revenue", "spread"])
        self.warnings = []

    def build(self) -> pd.DataFrame:
        for region, group in self.sales.groupby("region"):
            amounts = group["amount"]
            if len(group) < 2:
                self.warnings.append(f"{region}: only {len(group)} order")
            self.summary = self.summary.append(
                {
                    "region": region,
                    "orders": len(group),
                    "revenue": float(amounts.sum()),
                    "spread": round(float(amounts.mad()), 2),
                },
                ignore_index=True,
            )
        return self.summary

    def column_widths(self) -> dict:
        return {name: int(col.astype(str).str.len().max()) for name, col in self.summary.iteritems()}

    def to_csv(self) -> str:
        out = io.StringIO()
        self.summary.to_csv(out, index=False, line_terminator="\n")
        return out.getvalue()


def monthly_report(sales_path, targets_path) -> str:
    report = RegionReport(load_sales(sales_path))
    summary = report.build()
    targets = pd.read_csv(targets_path, index_col="region", squeeze=True)
    summary["hit_target"] = summary["revenue"].values >= targets.reindex(summary["region"]).values
    return report.to_csv()
