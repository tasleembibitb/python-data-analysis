"""
Shop Sales Data Analysis — demo project by Tasleem Bibi
--------------------------------------------------------
Analyses 100 sample orders (Jan–Jun 2026) from a small Sukkur boutique.
The data in sales_data.csv is SAMPLE / DEMO data, generated for practice —
it is not real business data.

What it does:
  1. Loads the CSV with pandas
  2. Prints total revenue, average order value, total items sold
  3. Finds the best-selling product (by revenue and by quantity)
  4. Breaks sales down by city and by payment method
  5. Shows monthly revenue trend
  6. Saves two charts as PNG files:
       - revenue_by_product.png  (bar chart)
       - monthly_revenue.png     (line chart)

How to run:
    pip install -r requirements.txt
    python analysis.py

Requirements: Python 3.8+, pandas, matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Load the data -------------------------------------------------------
# parse_dates turns the "date" text column into real dates so we can group by month.
df = pd.read_csv("sales_data.csv", parse_dates=["date"])

print("=" * 55)
print("SHOP SALES ANALYSIS  (100 sample orders, Jan–Jun 2026)")
print("=" * 55)
print(f"Orders analysed: {len(df)}")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print()

# --- 2. Overall totals ------------------------------------------------------
total_revenue = df["total_pkr"].sum()
avg_order = df["total_pkr"].mean()
total_items = df["quantity"].sum()

print(f"Total revenue:        Rs. {total_revenue:,}")
print(f"Average order value:  Rs. {avg_order:,.0f}")
print(f"Total items sold:     {total_items}")
print()

# --- 3. Best-selling products ----------------------------------------------
# Group by product: how many items sold and how much revenue each brought in.
by_product = (
    df.groupby("product")
    .agg(items_sold=("quantity", "sum"), revenue_pkr=("total_pkr", "sum"))
    .sort_values("revenue_pkr", ascending=False)
)
print("Sales by product (highest revenue first):")
print(by_product.to_string())
print()
print(f"Top product by revenue: {by_product.index[0]} "
      f"(Rs. {by_product.iloc[0]['revenue_pkr']:,})")
print(f"Top product by items:   {by_product['items_sold'].idxmax()} "
      f"({by_product['items_sold'].max()} items)")
print()

# --- 4. Sales by city and by payment method ---------------------------------
by_city = df.groupby("city")["total_pkr"].sum().sort_values(ascending=False)
print("Revenue by city:")
print(by_city.to_string())
print()

by_payment = df.groupby("payment_method")["total_pkr"].sum().sort_values(ascending=False)
print("Revenue by payment method:")
print(by_payment.to_string())
print()

# --- 5. Monthly trend --------------------------------------------------------
df["month"] = df["date"].dt.to_period("M")  # e.g. 2026-01
monthly = df.groupby("month")["total_pkr"].sum()
print("Monthly revenue:")
print(monthly.to_string())
print()
print(f"Best month: {monthly.idxmax()} (Rs. {monthly.max():,})")
print()

# --- 6. Charts ---------------------------------------------------------------
# Chart 1: revenue by product (bar chart)
plt.figure(figsize=(10, 5))
by_product["revenue_pkr"].plot(kind="bar", color="#6c2bd9")
plt.title("Revenue by Product (PKR)")
plt.ylabel("Revenue (PKR)")
plt.xlabel("Product")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig("revenue_by_product.png")
plt.close()

# Chart 2: monthly revenue trend (line chart)
plt.figure(figsize=(8, 4))
monthly.plot(kind="line", marker="o", color="#b3541e")
plt.title("Monthly Revenue Trend (Jan–Jun 2026)")
plt.ylabel("Revenue (PKR)")
plt.xlabel("Month")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("monthly_revenue.png")
plt.close()

print("Charts saved: revenue_by_product.png, monthly_revenue.png")
print("Done.")
