import pandas as pd

# Data source:
# HM Land Registry Price Paid Data
# Contains HM Land Registry data © Crown copyright and database right 2021.
# Licensed under the Open Government Licence v3.0.

# ============================================================
# 0. PRINTING CONVENTION 
# ============================================================

def print_header(m_str):
    print("\n" + "=" * 60)
    print(m_str)
    print("" + "=" * 60)

# ============================================================
# 1. LOAD DATA
# ============================================================

data = pd.read_csv("data/raw/pp-monthly-update-new-version.csv")

# ============================================================
# 2. BASIC INFORMATION
# ============================================================

print_header("DATASET SHAPE")
print(data.shape)
print_header("DATASET HEAD")
print(data.head)
print_header("COLUMN NAMES")
print(data.columns.tolist())
print_header("DATA TYPES")
print(data.dtypes)
print_header("INFORMATION")
print(data.info)
print_header("MISSING VALUES")
print(data.isnull().sum())
print_header("SUMMARY STATISTIC")
print(data.describe(include="all"))