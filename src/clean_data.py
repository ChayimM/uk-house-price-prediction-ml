import pandas as pd
from pathlib import Path


# ============================================================
# 1. FILE PATHS
# ============================================================

RAW_FILE = Path("data/raw/pp-2021.csv")
OUTPUT_FILE = Path("data/processed/house_prices_clean.csv")


# ============================================================
# 2. COLUMN NAMES
# ============================================================

COLUMNS = [
    "TransactionID",
    "Price",
    "Date",
    "Postcode",
    "PropertyType",
    "NewBuild",
    "Tenure",
    "PAON",
    "SAON",
    "Street",
    "Locality",
    "TownCity",
    "District",
    "County",
    "PPDCategory",
    "RecordStatus"
]


# ============================================================
# 3. LOAD RAW DATA
# ============================================================

df = pd.read_csv(
    RAW_FILE,
    header=None,
    names=COLUMNS
)


# ============================================================
# 4. CLEAN DATE
# ============================================================

df["Date"] = pd.to_datetime(df["Date"])

df["Year"] = df["Date"].dt.year


# ============================================================
# 5. CREATE USEFUL VARIABLES
# ============================================================

# Whether a secondary address exists.
df["HasSecondaryAddress"] = df["SAON"].notna().astype(int)


# ============================================================
# 6. SELECT VARIABLES FOR ANALYSIS
# ============================================================

df_clean = df[
    [
        "Price",
        "Year",
        "Postcode",
        "PropertyType",
        "NewBuild",
        "Tenure",
        "TownCity",
        "District",
        "County",
        "HasSecondaryAddress",
    ]
].copy()


# ============================================================
# 7. SAVE PROCESSED DATA
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df_clean.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 8. SUMMARY
# ============================================================

print("Cleaned dataset created.")
print(f"Rows: {len(df_clean):,}")
print(f"Columns: {len(df_clean.columns)}")
print(f"Saved to: {OUTPUT_FILE}")