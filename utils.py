import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def compute_kin(year: int, month: int, day: int) -> int:
    kin_start = pd.read_csv(
        os.path.join(DATA_DIR, "kin_start_year.csv"), index_col="年份", dtype=int
    )["起始KIN"].to_dict()
    month_accum = pd.read_csv(
        os.path.join(DATA_DIR, "month_day_accum.csv"), index_col="月份", dtype=int
    )["累積天數"].to_dict()
    start = kin_start[year]
    days = month_accum[month]
    raw = start + days + day
    mod = raw % 260
    return 260 if mod == 0 else mod

def fetch_self_info(kin: int) -> dict:
    basic = pd.read_csv(
        os.path.join(DATA_DIR, "kin_basic_info.csv"), dtype={"KIN": int, "圖騰": str}
    )
    row = basic[basic["KIN"] == kin]
    totem = row.iloc[0]["圖騰"]
    self_df = pd.read_csv(
        os.path.join(DATA_DIR, "totem_interpretation_new.csv"), dtype=str
    )
    matched = self_df[self_df["圖騰"] == totem]
    info = matched.iloc[0].to_dict()
    info["KIN"] = kin
    info["圖騰"] = totem
    return info
