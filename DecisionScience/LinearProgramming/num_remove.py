import pandas as pd
origin_df = pd.read_excel('Input excel files/ORIGINS1.xlsx')
destinations_df = pd.read_excel('Input excel files/DESTINATIONS1.xlsx')

current_sum = destinations_df['Required quantity'].sum()*0.05
threshold = origin_df.M1.sum()

# Calculate excess
excess = current_sum - threshold
df = destinations_df.copy()
if excess > 0:
    # Sort rows in descending order (assuming you want to remove the largest values first)
    df = df.sort_values(by='Required quantity', ascending=False)
    
    # Iteratively remove rows until the sum is below the threshold
    for i, row in df.iterrows():
        if current_sum - row['Required quantity']*0.05 >= threshold:
            current_sum -= row['Required quantity']*0.05
            df = df.drop(i)
        else:
            break

num_remove = destinations_df.shape[0] - df.shape[0]
print(num_remove)