import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

def add_kpis(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["CTR"] = df["clicks"] / df["impressions"]
    df["CVR"] = df["conversions"] / df["clicks"].replace(0, np.nan)
    df["CPC"] = df["spend_usd"] / df["clicks"].replace(0, np.nan)
    df["CPA"] = df["spend_usd"] / df["conversions"].replace(0, np.nan)
    return df

def summarize_by_group(df: pd.DataFrame) -> pd.DataFrame:
    agg = df.groupby("group").agg(
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        conversions=("conversions", "sum"),
        spend_usd=("spend_usd", "sum"),
    )
    agg["CTR"] = agg["clicks"] / agg["impressions"]
    agg["CVR"] = agg["conversions"] / agg["clicks"].replace(0, np.nan)
    agg["CPC"] = agg["spend_usd"] / agg["clicks"].replace(0, np.nan)
    agg["CPA"] = agg["spend_usd"] / agg["conversions"].replace(0, np.nan)
    return agg

def run_ab_test(df: pd.DataFrame):
    df = add_kpis(df)
    group_a = df[df["group"] == "A"]["CVR"].dropna()
    group_b = df[df["group"] == "B"]["CVR"].dropna()
    t_stat, p_val = ttest_ind(group_a, group_b, equal_var=False)
    return t_stat, p_val, group_a.mean(), group_b.mean()

if __name__ == "__main__":
    df = pd.read_csv("marketing_data.csv", parse_dates=["date"])
    df = add_kpis(df)

    print("===== Overall KPI summary by group =====")
    summary = summarize_by_group(df)
    print(summary)

    t_stat, p_val, mean_a, mean_b = run_ab_test(df)
    print("\n===== A/B Test on Conversion Rate (CVR) =====")
    print(f"Mean CVR A: {mean_a:.4f}")
    print(f"Mean CVR B: {mean_b:.4f}")
    print(f"T-statistic: {t_stat:.3f}")
    print(f"P-value: {p_val:.6f}")
    if p_val < 0.05:
        better = "B" if mean_b > mean_a else "A"
        print(f"Result: Statistically significant. Variant {better} wins at alpha=0.05.")
    else:
        print("Result: Not statistically significant at alpha=0.05.")
