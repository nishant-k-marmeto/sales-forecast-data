import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file from your local directory
# Replace 'path/to/your/csv/file.csv' with the actual path to your CSV file
sales_data = pd.read_csv('./consolidated-sales.csv')

# Display the column names to verify
print("Column Names:")
print(sales_data.columns)

# Calculate total revenue for each row
sales_data['Revenue'] = sales_data['Qty'] * sales_data['Amount']

# Find top 10 sold items by 'Style' and 'SKU'
top_selling_items = sales_data.groupby(['Style', 'SKU'])['Qty'].sum().sort_values(ascending=False).head(10)
print("\nTop 10 Sold Items:")
print(top_selling_items)

# Calculate revenue for each of the top 10 items
top_items_data = sales_data[sales_data['SKU'].isin(top_selling_items.index.get_level_values('SKU'))]
revenue_per_item = top_items_data.groupby(['Style', 'SKU'])['Revenue'].sum().sort_values(ascending=False)
print("\nRevenue per Top 10 Item:")
print(revenue_per_item)

# Calculate total revenue from all top 10 items combined
total_revenue_top_10 = revenue_per_item.sum()
print("\nTotal Revenue from Top 10 Items:", total_revenue_top_10)

# Visualization
# Create a DataFrame for plotting, including both Qty and Revenue
top_items_data = sales_data[sales_data['SKU'].isin(top_selling_items.index.get_level_values('SKU'))]
top_items_summary = top_items_data.groupby(['Style', 'SKU']).agg({'Qty': 'sum', 'Revenue': 'sum'}).reset_index()

# Sort for visualization
top_items_summary = top_items_summary.sort_values(by='Qty', ascending=False).head(10)

print("\nTop Items Summary DataFrame:")
print(top_items_summary)

# Visualization
plt.figure(figsize=(12, 6))

# Bar plot for Quantity Sold
plt.subplot(1, 2, 1)
sns.barplot(data=top_items_summary, x='Qty', y='SKU', palette='viridis')
plt.title('Top 10 Sold Items - Quantity')
plt.xlabel('Quantity Sold')
plt.ylabel('SKU')

# Bar plot for Revenue
plt.subplot(1, 2, 2)
sns.barplot(data=top_items_summary, x='Revenue', y='SKU', palette='viridis')
plt.title('Top 10 Sold Items - Revenue')
plt.xlabel('Total Revenue')
plt.ylabel('SKU')

plt.tight_layout()
plt.show()
