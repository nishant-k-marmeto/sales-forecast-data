import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file from your local directory
sales_data = pd.read_csv('./consolidated-sales.csv')

# Calculate total revenue for each row
sales_data['Revenue'] = sales_data['Qty'] * sales_data['Amount']

# Find top 10 sold items by 'SKU'
top_selling_items = sales_data.groupby('SKU')['Qty'].sum().sort_values(ascending=False).head(10)

# Calculate revenue for each of the top 10 items
top_items_data = sales_data[sales_data['SKU'].isin(top_selling_items.index)]
revenue_per_item = top_items_data.groupby('SKU')['Revenue'].sum().sort_values(ascending=False)

# Inventory Setup
initial_inventory_per_item = 365  # Each SKU starts with 365 units
initial_inventory = {sku: initial_inventory_per_item for sku in top_selling_items.index}

# Calculate total revenue without discount
revenue_without_discount = revenue_per_item.sum()

# Apply tiered discounts using .loc to avoid SettingWithCopyWarning
top_items_data.loc[:, 'Discounted Price'] = top_items_data.apply(
    lambda row: row['Amount'] * (0.90 if row['Qty'] >= 2 else (0.85 if row['Qty'] >= 3 else 1)), 
    axis=1
)

# Calculate total revenue with discount
revenue_with_discount = top_items_data.groupby('SKU')['Discounted Price'].sum().sort_values(ascending=False)

# Inventory consumption calculations
def inventory_consumption(days, discount=False):
    # Reset inventory for each simulation
    inventory = {sku: initial_inventory_per_item for sku in initial_inventory}
    inventory_consumed = {sku: 0 for sku in initial_inventory}
    consumption_data = {sku: [] for sku in initial_inventory}
    consumption_days = {sku: None for sku in initial_inventory}  # To track consumption days

    for day in range(1, days + 1):
        for sku in initial_inventory:
            if inventory[sku] > 0:  # If there is inventory left to sell
                if discount:
                    # Assume selling a fixed number of items for discounted case
                    sold_qty = min(2, inventory[sku])  # Selling 2 items when discount is applied
                else:
                    # Assume selling a fixed number of items for non-discounted case
                    sold_qty = min(1, inventory[sku])  # Selling 1 item without discount

                # Update the sold quantity and inventory
                inventory_consumed[sku] += sold_qty
                inventory[sku] -= sold_qty  # Update remaining inventory
                consumption_data[sku].append(inventory_consumed[sku])
                
                # Debugging: Print sold quantity and remaining inventory
                print(f"Day {day}: Selling {sold_qty} of {sku}. Inventory left: {inventory[sku]}.")

                # Track consumption days
                if consumption_days[sku] is None and inventory_consumed[sku] >= initial_inventory_per_item:
                    consumption_days[sku] = day
            else:
                consumption_data[sku].append(inventory_consumed[sku])  # Keep appending the last value when sold out

    return consumption_data, consumption_days

# Simulate inventory consumption over 365 days
days = 365
consumption_without_discount, consumption_days_without_discount = inventory_consumption(days, discount=False)
consumption_with_discount, consumption_days_with_discount = inventory_consumption(days, discount=True)

# Visualizing Revenue
plt.figure(figsize=(12, 6))

# Bar plot for Revenue without Discount
plt.subplot(1, 2, 1)
revenue_per_item.plot(kind='bar', color='blue', alpha=0.7, label='Without Discount')
plt.title('Revenue Generated by Top Selling Items\nWithout Discount')
plt.xlabel('SKU')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.legend()

# Add values on top of bars for without discount
for index, value in enumerate(revenue_per_item):
    plt.text(index, value, f'{value/1000:.0f}k', ha='center', va='bottom')

# Bar plot for Revenue with Discount
plt.subplot(1, 2, 2)
revenue_with_discount.plot(kind='bar', color='orange', alpha=0.7, label='With Discount')
plt.title('Revenue Generated by Top Selling Items\nWith Discount')
plt.xlabel('SKU')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.legend()

# Add values on top of bars for with discount
for index, value in enumerate(revenue_with_discount):
    plt.text(index, value, f'{value/1000:.0f}k', ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Visualizing Inventory Consumption
plt.figure(figsize=(12, 6))

# Line plot for Inventory Consumption without Discount (solid red)
for sku, consumption in consumption_without_discount.items():
    plt.plot(range(1, days + 1), consumption, label=f'Without Discount - {sku}', color='red', linestyle='solid')

# Line plot for Inventory Consumption with Discount (dashed green)
for sku, consumption in consumption_with_discount.items():
    plt.plot(range(1, days + 1), consumption, label=f'With Discount - {sku}', color='green', linestyle='dashed')

plt.title('Inventory Consumption Over 365 Days')
plt.xlabel('Days')
plt.ylabel('Cumulative Inventory Consumed')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Print consumption days for each SKU
print("Consumption Days Without Discount:")
for sku, days in consumption_days_without_discount.items():
    print(f"{sku}: Consumed by day {days}" if days is not None else f"{sku}: Not consumed")

print("\nConsumption Days With Discount:")
for sku, days in consumption_days_with_discount.items():
    print(f"{sku}: Consumed by day {days}" if days is not None else f"{sku}: Not consumed")
