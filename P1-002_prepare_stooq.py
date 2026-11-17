# ============================================================
# P1-002_prepare_stooq.py
# Build a local S&P 500 daily close-price matrix
# from Stooq bulk historical data.
# ============================================================

from pathlib import Path
import pandas as pd

stooq_root = Path(r"D:\Code\Quant\data\d_us_txt\data\daily\us")
output_path = Path(r"D:\Code\Quant\data\stooq_sp500_close_2018_2026.csv")

sp500_url = (
    "https://raw.githubusercontent.com/"
    "datasets/s-and-p-500-companies/"
    "main/data/constituents.csv"
)

sp500 = pd.read_csv(sp500_url)
tickers = (
    sp500["Symbol"]
    .dropna()
    .astype(str)
    .str.strip()
    .tolist()
)

print("Current S&P 500 securities:", len(tickers))

if not stooq_root.exists():
    raise FileNotFoundError(f"Stooq root does not exist: {stooq_root}")

all_files = list(stooq_root.rglob("*.txt"))
print("Stooq txt files found:", len(all_files))

if not all_files:
    raise RuntimeError("No .txt files found under the Stooq US folder.")

file_map = {f.stem.lower(): f for f in all_files}

def ticker_to_candidates(ticker):
    ticker = str(ticker).strip().lower()
    candidates = [f"{ticker}.us"]
    if "." in ticker:
        candidates.append(f"{ticker.replace('.', '-')}.us")
        candidates.append(f"{ticker.replace('.', '_')}.us")
    return candidates

start_date = pd.Timestamp("2018-01-01")
end_date = pd.Timestamp("2026-10-01")

series_list = []
missing_tickers = []
failed_read_tickers = []

for ticker in tickers:
    filepath = None

    for candidate in ticker_to_candidates(ticker):
        if candidate in file_map:
            filepath = file_map[candidate]
            break

    if filepath is None:
        missing_tickers.append(ticker)
        continue

    try:
        df = pd.read_csv(filepath)
    except Exception as exc:
        print("Failed reading:", ticker, exc)
        failed_read_tickers.append(ticker)
        continue

    df.columns = [
        str(c).strip().replace("<", "").replace(">", "").lower()
        for c in df.columns
    ]

    if "date" not in df.columns or "close" not in df.columns:
        missing_tickers.append(ticker)
        continue

    df["date"] = pd.to_datetime(
        df["date"].astype(str).str.strip(),
        format="%Y%m%d",
        errors="coerce",
    )

    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    df = df.loc[
        (df["date"] >= start_date) & (df["date"] < end_date),
        ["date", "close"],
    ].dropna()

    if df.empty:
        missing_tickers.append(ticker)
        continue

    s = (
        df.drop_duplicates(subset="date", keep="last")
        .set_index("date")["close"]
        .sort_index()
    )
    s.name = ticker
    series_list.append(s)

if not series_list:
    raise RuntimeError("No usable Stooq stock data matched the S&P 500 ticker list.")

close = pd.concat(series_list, axis=1).sort_index()
close.index.name = "date"
close.columns.name = "ticker"

print("\n===== Stooq Price Matrix =====")
print("Shape:", close.shape)
print("Date range:", close.index.min(), "to", close.index.max())
print("Successfully matched:", close.shape[1])
print("Missing tickers:", len(missing_tickers))
print(missing_tickers[:30])
print("Read failures:", len(failed_read_tickers))
print("Missing values:", close.isna().sum().sum())

monthly_close = close.resample("ME").last()
valid_stocks = monthly_close.notna().sum(axis=1)

print("\n===== Monthly Coverage Validation =====")
print("Monthly shape:", monthly_close.shape)
print("Minimum valid stocks:", int(valid_stocks.min()))
print("Median valid stocks:", float(valid_stocks.median()))
print("Maximum valid stocks:", int(valid_stocks.max()))

output_path.parent.mkdir(parents=True, exist_ok=True)
close.to_csv(output_path)

print("\nSaved to:", output_path)
