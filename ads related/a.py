# .venv/bin/activate
import json
import pandas as pd
import numpy as np

with open("data.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

print(df.head())
print(df.shape)
print(df.dtypes)
print(df["click"].value_counts())
print(df["click"].value_counts(normalize=True))