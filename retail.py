import pandas as pd

# -------------------------------
# 1. Load Dataset
# -------------------------------

file_path = "C:/Users/Somashekar M/Downloads/Sales_data.csv"
data = pd.read_csv(file_path)

print("Data Loaded Successfully!")
print(data.head())

# -------------------------------
# 2. Clean Column Names
# -------------------------------

data.columns = data.columns.str.strip().str.lower()

# -------------------------------
# 3. Create RFM Table from Your Data
# -------------------------------

rfm = data[['customer_id','signup_days_ago','total_transactions','total_spend']].copy()

# rename as RFM
rfm.columns = ['customer_id','Recency','Frequency','Monetary']

rfm = rfm.set_index('customer_id')

print("\nRFM Table Created!")
print(rfm.head())

# -------------------------------
# 4. RFM Scoring
# -------------------------------

rfm['R_Score'] = pd.qcut(rfm['Recency'], q=5, duplicates='drop').cat.codes + 1
rfm['F_Score'] = pd.qcut(rfm['Frequency'], q=5, duplicates='drop').cat.codes + 1
rfm['M_Score'] = pd.qcut(rfm['Monetary'], q=5, duplicates='drop').cat.codes + 1

# reverse recency (lower days = better customer)
rfm['R_Score'] = 6 - rfm['R_Score']

rfm['RFM_Score'] = (
    rfm['R_Score'].astype(str) +
    rfm['F_Score'].astype(str) +
    rfm['M_Score'].astype(str)
)

# -------------------------------
# 5. Customer Segmentation
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
# 6. Save Output
# -------------------------------

rfm.to_csv("rfm_output.csv")

print("\n✅ RFM Analysis Completed Successfully!")

print("\nCustomer Segment Summary:")
print(rfm['Segment'].value_counts())

print("\nTop 10 Customers:")
print(rfm.sort_values(by='RFM_Score', ascending=False).head(10))

# -------------------------------
# 7. Visualization
# -------------------------------

import matplotlib.pyplot as plt

# Customer segment distribution
plt.figure()
rfm['Segment'].value_counts().plot(kind='bar')
plt.title("Customer Segmentation Distribution")
plt.xlabel("Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45)
plt.show()


# Recency vs Monetary scatter plot
plt.figure()
plt.scatter(rfm['Recency'], rfm['Monetary'])
plt.title("Recency vs Monetary")
plt.xlabel("Recency")
plt.ylabel("Monetary")
plt.show()


# Frequency distribution
plt.figure()
rfm['Frequency'].plot(kind='hist')
plt.title("Frequency Distribution")
plt.xlabel("Frequency")
plt.show()

