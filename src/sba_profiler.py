import pandas as pd

# 1. Load the raw dataset
file_path = '../data/raw/SBAnational.csv'
print(f"Loading raw federal ledger data from {file_path}...\n")
df = pd.read_csv(file_path, low_memory=False)

# 2. High-Level Structural Overview
print("--- Data Lineage: Structural Overview ---")
print(f"Total Raw Records: {df.shape[0]:,}")
print(f"Total Attributes (Columns): {df.shape[1]}")

# 3. Quantifying Missing Data (Null Concentrations)
print("\n--- Null Value Concentrations (Top 5 columns missing data) ---")
missing_data = df.isnull().sum()
print(missing_data[missing_data > 0].sort_values(ascending=False).head(5))

# 4. Profiling the Revolving Line of Credit column (The Messy Flag)
print("\n--- Data Defect Profiling: Revolving Credit Flag (RevLineCr) ---")
print("Expected enterprise values: 'Y' (Yes) or 'N' (No)")
print("Actual garbage values found in the raw system:")
print(df['RevLineCr'].value_counts(dropna=False).head(10))

# 5. Profiling the Financial Columns for Data Types
print("\n--- Financial Attribute Types ---")
print("Notice how these are 'object' (strings), not floats, meaning we can't do math on them yet:")
print(df[['DisbursementGross', 'SBA_Appv']].dtypes)
