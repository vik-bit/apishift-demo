from pathlib import Path

import pandas as pd

from sales_report import RegionReport, monthly_report
from sales_report.load import load_sales

DATA = Path(__file__).parent / "data"


def test_load_strips_text_columns():
    df = load_sales(DATA / "sales.csv")
    assert sorted(df["region"].unique()) == ["east", "north", "south"]


def test_summary_per_region():
    report = RegionReport(load_sales(DATA / "sales.csv"))
    s = report.build()
    assert s["region"].tolist() == ["east", "north", "south"]
    assert s["orders"].tolist() == [1, 3, 2]
    assert s["revenue"].tolist() == [40.0, 60.0, 30.0]
    assert s["spread"].tolist() == [0.0, 6.67, 5.0]
    assert report.warnings == ["east: only 1 order"]


def test_column_widths():
    report = RegionReport(load_sales(DATA / "sales.csv"))
    report.build()
    assert report.column_widths()["region"] == 5


def test_monthly_report_csv():
    csv = monthly_report(DATA / "sales.csv", DATA / "targets.csv")
    assert csv.splitlines() == [
        "region,orders,revenue,spread,hit_target",
        "east,1,40.0,0.0,True",
        "north,3,60.0,6.67,True",
        "south,2,30.0,5.0,False",
    ]
    assert csv.endswith("\n") and "\r" not in csv


def test_targets_loaded_as_series():
    targets = pd.read_csv(DATA / "targets.csv", index_col="region").squeeze("columns")
    assert isinstance(targets, pd.Series)
