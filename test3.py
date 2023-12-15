import pandas as pd

df = pd.read_csv('data.csv')

print(df.head())

df['price_per_foot'] = df['price'] / df['sq__ft']
average_price_per_foot = df['price_per_foot'].mean()

filtered_df = df[df['price'] < average_price_per_foot]

filtered_df.to_csv('output.csv', index=False)