# -*- coding: utf-8 -*-
"""
Created on 2025/8/15 17:21

@author: starry
"""


import os
import pandas as pd
import matplotlib.pyplot as plt


INPUT_PATH  = r"/Users/starry/Documents/GIS/Applied Project(Academic)/Picture1/10CAIRail.csv"
LSOA_COL    = "LSOA21CD"
CAI_COL     = "CAI"
OUT_PREFIX  = "Rail_cai_newham"


CLASS_METHOD = "fixed"


LOW_TH, HIGH_TH = 0.33, 0.66


Q_LOW, Q_HIGH = 1/3, 2/3



def read_table(path: str) -> pd.DataFrame:
    """Read CSV or Excel by file extension, no hard dependency on openpyxl."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(path)
    elif ext in (".xlsx", ".xls"):

        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}. Use .csv, .xlsx or .xls")


def classify_fixed(v: float, low_th: float, high_th: float) -> str:
    if pd.isna(v):
        return "NA"
    if v >= high_th:
        return "High"
    elif v >= low_th:
        return "Medium"
    else:
        return "Low"


def main():

    df = read_table(INPUT_PATH)


    cols = {c.lower(): c for c in df.columns}
    lsoa = LSOA_COL if LSOA_COL in df.columns else cols.get(LSOA_COL.lower())
    cai  = CAI_COL  if CAI_COL  in df.columns else cols.get(CAI_COL.lower())
    if lsoa is None or cai is None:
        raise ValueError(f"Can't find {LSOA_COL} or {CAI_COL}，have：{list(df.columns)}")

    df = df[[lsoa, cai]].rename(columns={lsoa: "LSOA21CD", cai: "CAI"}).copy()


    if CLASS_METHOD == "fixed":
        low, high = LOW_TH, HIGH_TH
    elif CLASS_METHOD == "quantile":
        low, high = df["CAI"].quantile(Q_LOW), df["CAI"].quantile(Q_HIGH)
    else:
        raise ValueError("CLASS_METHOD must be 'fixed' or 'quantile'.")

    df["Class"] = df["CAI"].apply(lambda v: classify_fixed(v, low, high))

    # Count the quantity and proportion
    valid = df[df["Class"] != "NA"].copy()
    counts = valid["Class"].value_counts().reindex(["High", "Medium", "Low"], fill_value=0)
    total = counts.sum()
    perc = (counts / total * 100).round(1) if total > 0 else counts.astype(float)


    vmin, vmax = valid["CAI"].min(), valid["CAI"].max()
    vrange = vmax - vmin


    summary = pd.DataFrame({
        "Class": ["High", "Medium", "Low", "Range (min–max)", "Range width"],
        "Count": [int(counts["High"]), int(counts["Medium"]), int(counts["Low"]), vmin, vrange],
        "Percent": [float(perc["High"]), float(perc["Medium"]), float(perc["Low"]), vmax, None]
    })


    out_csv = f"{OUT_PREFIX}_bus_only_distribution.csv"
    out_tex = f"{OUT_PREFIX}_bus_only_distribution.tex"
    summary.to_csv(out_csv, index=False)


    # Figure 1: Three-tier proportion bar chart
    fig = plt.figure(figsize=(6, 4.5))
    ax = plt.gca()
    ax.bar(["High", "Medium", "Low"], [perc["High"], perc["Medium"], perc["Low"]])
    ax.set_ylabel("Share of LSOAs (%)")
    ax.set_title("10-Minute Rail Stations Accessibility CAI Class Shares (Newham)")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    out_png1 = f"{OUT_PREFIX}_bus_only_class_shares.png"
    fig.savefig(out_png1, dpi=300)
    plt.close(fig)

    # Figure 2: LSOA-level CAI bar chart
    df_sorted = valid.sort_values("CAI").reset_index(drop=True)
    fig = plt.figure(figsize=(10, 5))
    ax = plt.gca()
    ax.bar(df_sorted["LSOA21CD"], df_sorted["CAI"])
    ax.set_xlabel("LSOA21CD")
    ax.set_ylabel("CAI")
    ax.set_title("Rail CAI by LSOA (sorted)")
    ax.tick_params(axis="x", labelrotation=90)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    out_png2 = f"{OUT_PREFIX}_bus_only_LSOA_bars.png"
    fig.savefig(out_png2, dpi=300)
    plt.close(fig)


    print("\n=== Bus CAI Distribution (Single Mode) ===")
    print(f"Thresholds used -> Low: {low:.4f}, High: {high:.4f}  (method: {CLASS_METHOD})")
    print(f"Total valid LSOAs: {total}")
    print(summary.to_string(index=False))
    print("\nSaved:")
    print(out_csv)
    print(out_tex)
    print(out_png1)
    print(out_png2)


if __name__ == "__main__":
    main()