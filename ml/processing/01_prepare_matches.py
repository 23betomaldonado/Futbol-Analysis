import pandas as pd
from pathlib import Path

#file path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

MATCHES_FILE = RAW_DATA / "matches_1930_2022.CSV"

#--------------------------------------------------------

#Load data
matches = pd.read_csv(MATCHES_FILE)

#---------------------------------------------------------

#Initial inspection
print("Dataset shape: ", matches.shape) 

print("\nColumns: ")     
print(matches.columns.tolist()) 

print("\nFirst 5 rows: ") 
print(matches.head()) 

print("\nData types: ") 
print(matches.dtypes) 

print("\nMissing values: ") 
print(matches.isnull().sum()) 

print("\nDuplicare rows: ", matches.duplicated().sum()) 