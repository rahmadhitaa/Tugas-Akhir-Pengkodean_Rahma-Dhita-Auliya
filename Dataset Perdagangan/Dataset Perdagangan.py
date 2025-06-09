# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import files
from datetime import datetime
import io

# Create dataframes from the provided CSV data
inventory_data = """
inventory_id,product_id,warehouse_id,stock_quantity,last_updated
1,P001,W001,450,2025-03-10
2,P002,W001,280,2025-03-10
3,P003,W002,180,2025-03-10
4,P004,W001,240,2025-03-10
5,P001,W002,100,2025-03-10
"""
production_data = """
production_id,product_id,product_name,production_date,quantity_produced,production_cost
1,P001,Kemeja Katun,2025-01-10,500,75000.00
2,P002,Celana Jeans,2025-01-15,300,120000.00
3,P003,Jaket Kulit,2025-02-01,200,250000.00
4,P001,Kemeja Katun,2025-02-10,400,76000.00
5,P004,Sepatu Sneaker,2025-03-01,250,150000.00
"""
sales_data = """
sale_id,product_id,sale_date,quantity_sold,sale_price,total_revenue
1,P001,2025-02-15,50,100000.00,5000000.00
2,P002,2025-02-20,20,150000.00,3000000.00
3,P003,2025-03-01,15,300000.00,4500000.00
4,P001,2025-03-05,30,105000.00,3150000.00
5,P004,2025-03-10,10,200000.00,2000000.00
"""

# Read CSV strings into dataframes
inventory_df = pd.read_csv(io.StringIO(inventory_data))
production_df = pd.read_csv(io.StringIO(production_data))
sales_df = pd.read_csv(io.StringIO(sales_data))

# Data Cleaning and Preparation
# Convert date columns to datetime
inventory_df['last_updated'] = pd.to_datetime(inventory_df['last_updated'])
production_df['production_date'] = pd.to_datetime(production_df['production_date'])
sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])

# Analysis 1: Inventory Status by Product
inventory_summary = inventory_df.groupby('product_id').agg({
    'stock_quantity': 'sum',
    'warehouse_id': 'nunique'
}).reset_index()
inventory_summary = inventory_summary.merge(
    production_df[['product_id', 'product_name']].drop_duplicates(),
    on='product_id',
    how='left'
)
inventory_summary.columns = ['Product ID', 'Total Stock', 'Warehouse Count', 'Product Name']

# Analysis 2: Production and Sales Performance
# Calculate total production cost
production_summary = production_df.groupby('product_id').agg({
    'quantity_produced': 'sum',
    'production_cost': 'mean',
    'product_name': 'first'
}).reset_index()

# Calculate total sales metrics
sales_summary = sales_df.groupby('product_id').agg({
    'quantity_sold': 'sum',
    'sale_price': 'mean',
    'total_revenue': 'sum'
}).reset_index()

# Merge production and sales data
performance_summary = production_summary.merge(
    sales_summary,
    on='product_id',
    how='outer'
).fillna(0)
performance_summary['profit_per_unit'] = performance_summary['sale_price'] - performance_summary['production_cost']
performance_summary['total_profit'] = performance_summary['quantity_sold'] * performance_summary['profit_per_unit']

# Save analysis results to CSV files
inventory_summary.to_csv('inventory_summary.csv', index=False)
performance_summary.to_csv('performance_summary.csv', index=False)

# Download the CSV files
files.download('inventory_summary.csv')
files.download('performance_summary.csv')

# Visualization 1: Stock Levels by Product
plt.figure(figsize=(10, 6))
sns.barplot(data=inventory_summary, x='Product Name', y='Total Stock')
plt.title('Current Stock Levels by Product')
plt.xlabel('Product')
plt.ylabel('Stock Quantity')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Visualization 2: Profit Analysis
plt.figure(figsize=(10, 6))
sns.barplot(data=performance_summary, x='product_name', y='total_profit')
plt.title('Total Profit by Product')
plt.xlabel('Product')
plt.ylabel('Total Profit (IDR)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Visualization 3: Production vs Sales Quantity
plt.figure(figsize=(10, 6))
performance_summary_melted = performance_summary.melt(
    id_vars=['product_name'],
    value_vars=['quantity_produced', 'quantity_sold'],
    var_name='Type',
    value_name='Quantity'
)
sns.barplot(data=performance_summary_melted, x='product_name', y='Quantity', hue='Type')
plt.title('Production vs Sales Quantity by Product')
plt.xlabel('Product')
plt.ylabel('Quantity')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Display summary tables
print("\nInventory Summary:")
print(inventory_summary)
print("\nPerformance Summary:")
print(performance_summary[['product_name', 'quantity_produced', 'quantity_sold', 'total_revenue', 'total_profit']])