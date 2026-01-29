import pandas as pd
from datetime import datetime

# -------------------------------
# 1. Load Dataset
# -------------------------------

file_path = "C:/Users/Somashekar M/Downloads/sales_data.csv"   # Your uploaded file
data = pd.read_csv(file_path)

print("Data Loaded Successfully!")
print(data.head())


# -------------------------------
# 2. Convert Date Column
# -------------------------------

data['sale_date'] = pd.to_datetime(
    data['sale_date'],
    dayfirst=True,
    errors='coerce'
)


# -------------------------------
# 3. Set Reference Date (Today)
# -------------------------------

today = datetime(2026, 1, 29)


# -------------------------------
# 4. Calculate RFM Values
# -------------------------------

rfm = data.groupby('customer_id').agg({

    'sale_date': lambda x: (today - x.max()).days,  # Recency
    'sale_id': 'count',                             # Frequency
    'amount': 'sum'                                 # Monetary

})


# Rename Columns
rfm.columns = ['Recency', 'Frequency', 'Monetary']


print("\nRFM Table Created!")
print(rfm.head())


# -------------------------------
# 5. Assign RFM Scores (1 to 5)
# -------------------------------

# -------------------------------
# Safe RFM Scoring (No Errors)
# -------------------------------

rfm['R_Score'] = pd.qcut(
    rfm['Recency'],
    q=5,
    duplicates='drop'
).cat.codes + 1


rfm['F_Score'] = pd.qcut(
    rfm['Frequency'],
    q=5,
    duplicates='drop'
).cat.codes + 1


rfm['M_Score'] = pd.qcut(
    rfm['Monetary'],
    q=5,
    duplicates='drop'
).cat.codes + 1


# Reverse Recency Score (Lower recency = better customer)
rfm['R_Score'] = 6 - rfm['R_Score']


# -------------------------------
# 6. Combine Scores
# -------------------------------

rfm['RFM_Score'] = (
    rfm['R_Score'].astype(str) +
    rfm['F_Score'].astype(str) +
    rfm['M_Score'].astype(str)
)


print("\nRFM Scores Assigned!")
print(rfm[['R_Score','F_Score','M_Score','RFM_Score']].head())


# -------------------------------
# 7. Customer Segmentation
# -------------------------------

def segment_customer(row):

    score = row['RFM_Score']

    if score >= '455':
        return 'Champions'

    elif score >= '344':
        return 'Loyal Customers'

    elif score >= '233':
        return 'Potential Loyalist'

    elif score >= '122':
        return 'Needs Attention'

    else:
        return 'Lost Customers'


rfm['Segment'] = rfm.apply(segment_customer, axis=1)


print("\nCustomer Segments Created!")
print(rfm[['RFM_Score','Segment']].head())


# -------------------------------
# 8. Sort by Best Customers
# -------------------------------

rfm_sorted = rfm.sort_values(by='RFM_Score', ascending=False)


# -------------------------------
# 9. Save Output File
# -------------------------------

# Save Output File
output_file = "rfm_output.csv"

rfm_sorted.to_csv(output_file, index=True)

print("File saved successfully as:", output_file)


rfm_sorted.to_csv(output_file)


print("\nRFM Analysis Completed Successfully!")
print("Output saved as:", output_file)


# -------------------------------
# 10. Segment Summary
# -------------------------------

segment_summary = rfm['Segment'].value_counts()

print("\nCustomer Segment Summary:")
print(segment_summary)


# -------------------------------
# 11. Top 10 Customers
# -------------------------------

print("\nTop 10 High Value Customers:")
print(rfm_sorted.head(10))
