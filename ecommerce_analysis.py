# PROJECT: E-Commerce Sales Analysis
# Dataset  : Superstore Sales Dataset

# STEP 1: Import Libraries
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

print("Libraries imported successfully!")

# STEP 2: LOAD THE DATA
print("\n Loading the dataset")
data = pd.read_csv("superstore.csv", encoding="latin-1")

# basic info 
print("Number of rows    :", len(data))           # total rows
print("Number of columns :", len(data.columns))   # total columns
print("\nColumn names:")
print(data.columns.tolist())                       # list all column names

# Preview first 5 rows
print("\nFirst 5 rows of data:")
print(data.head())

# STEP 3: CLEAN THE DATA
print("\n Cleaning the data ")
data["Order Date"] = pd.to_datetime(data["Order Date"])
data["Ship Date"]  = pd.to_datetime(data["Ship Date"])

# Create a new column: how many days it took to ship each order
data["Days to Ship"] = (data["Ship Date"] - data["Order Date"]).dt.days

# Create a new column: profit margin percentage
# Profit Margin = (Profit / Sales) × 100
data["Profit Margin %"] = (data["Profit"] / data["Sales"]) * 100

# Check for missing values in each column
print("\nMissing values in each column:")
print(data.isnull().sum())

# STEP 4: BASIC SUMMARY (KPIs - Key Performance Indicators)
print("\n Business KPIs ")

total_sales    = data["Sales"].sum()       # add up all sales values
total_profit   = data["Profit"].sum()      # add up all profit values
total_orders   = data["Order ID"].nunique() # count unique order IDs
total_customers = data["Customer ID"].nunique() # count unique customers
avg_margin     = data["Profit Margin %"].mean() # average of all margins

print(f"Total Revenue    : ${total_sales:,.0f}")   # :, adds comma separator
print(f"Total Profit     : ${total_profit:,.0f}")
print(f"Total Orders     : {total_orders:,}")
print(f"Unique Customers : {total_customers:,}")
print(f"Avg Profit Margin: {avg_margin:.2f}%")    # :.2f means 2 decimal places


# STEP 5: SALES AND PROFIT BY CATEGORY
print("\n Sales & Profit by Category ")

# Group by 'Category' and calculate sum of Sales and Profit
category_summary = data.groupby("Category")[["Sales", "Profit"]].sum()

# Reset index makes Category a regular column again (not an index)
category_summary = category_summary.reset_index()

# Round the numbers for clean display
category_summary["Sales"]  = category_summary["Sales"].round(2)
category_summary["Profit"] = category_summary["Profit"].round(2)

print(category_summary)

# --- Draw a bar chart ---
plt.figure(figsize=(8, 5))  # set chart size (width=8, height=5 inches)

# Create bar chart: x = Category names, y = Sales values
plt.bar(
    category_summary["Category"],   # x-axis: category names
    category_summary["Sales"],      # y-axis: sales values
    color=["#1A56A0", "#F59E0B", "#10B981"]  # custom colors for each bar
)

plt.title("Total Sales by Category")   # chart title
plt.xlabel("Category")                  # label for x-axis
plt.ylabel("Total Sales ($)")           # label for y-axis
plt.tight_layout()                      # auto-adjust spacing
plt.savefig("chart1_sales_by_category.png")  # save chart as image
plt.close()

print("Chart saved: chart1_sales_by_category.png")


# STEP 6: FIND THE TOP 5 MOST PROFITABLE PRODUCTS
print("\n Top 5 Most Profitable Sub-Categories ")

# Group by Sub-Category and sum profit
subcategory_profit = data.groupby("Sub-Category")["Profit"].sum()

# sort_values() sorts the result → ascending=False means highest first
subcategory_profit = subcategory_profit.sort_values(ascending=False)

# Take only first 5 rows using .head(5)
top5 = subcategory_profit.head(5)
print(top5)

# --- Draw horizontal bar chart ---
plt.figure(figsize=(8, 5))
plt.barh(top5.index, top5.values, color="#1A56A0")  # barh = horizontal bar
plt.title("Top 5 Most Profitable Sub-Categories")
plt.xlabel("Total Profit ($)")
plt.tight_layout()
plt.savefig("chart2_top5_subcategories.png")
plt.close()

#print("Chart saved: chart2_top5_subcategories.png")

# STEP 7: FIND LOSS-MAKING SUB-CATEGORIES

print("\n Bottom 5 Loss-Making Sub-Categories ")

# Take the last 5 rows (lowest profit = biggest losses)
bottom5 = subcategory_profit.tail(5)
print(bottom5)

# --- Draw horizontal bar chart with red color to show losses ---
plt.figure(figsize=(8, 5))
plt.barh(bottom5.index, bottom5.values, color="#EF4444")
plt.title("Loss-Making Sub-Categories")
plt.xlabel("Total Profit ($)")
plt.tight_layout()
plt.savefig("chart3_loss_subcategories.png")
plt.close()

#print("Chart saved: chart3_loss_subcategories.png")

# STEP 8: REGIONAL PERFORMANCE
print("\n Sales by Region ")

# Group by Region and sum Sales
region_summary = data.groupby("Region")["Sales"].sum().reset_index()
region_summary = region_summary.sort_values("Sales", ascending=False)
print(region_summary)

# Pie chart to show each region's share of total sales
plt.figure(figsize=(7, 7))
plt.pie(
    region_summary["Sales"],          # values (slice sizes)
    labels=region_summary["Region"],  # labels for each slice
    autopct="%1.1f%%",                # show percentage on each slice
    startangle=90,                    # rotate start position
    colors=["#1A56A0", "#F59E0B", "#10B981", "#EF4444"]
)
plt.title("Sales Share by Region")
plt.tight_layout()
plt.savefig("chart4_region_sales.png")
plt.close()

#print("Chart saved: chart4_region_sales.png")

# STEP 9: MONTHLY SALES TREND
print("\n Monthly Sales Trend")

# Extract year and month from Order Date
# dt.to_period("M") converts date to "2020-01" format
data["Month"] = data["Order Date"].dt.to_period("M").astype(str)

# Group by Month and sum sales
monthly_sales = data.groupby("Month")["Sales"].sum().reset_index()

print(f"Total months in data: {len(monthly_sales)}")
print(monthly_sales.tail(12))  # show last 12 months

# --- Line chart to show trend over time ---
plt.figure(figsize=(14, 5))
plt.plot(
    monthly_sales["Month"],    # x-axis: month names
    monthly_sales["Sales"],    # y-axis: sales amount
    color="#1A56A0",
    linewidth=2,
    marker="o",                # add dot at each data point
    markersize=4
)
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales ($)")
plt.xticks(rotation=45, ha="right", fontsize=7)  # rotate x labels
plt.tight_layout()
plt.savefig("chart5_monthly_trend.png")
plt.close()

print("Chart saved: chart5_monthly_trend.png")

# STEP 10: DISCOUNT IMPACT ON PROFIT
# Business question: Do heavy discounts reduce profit?

print("\n Does Discount Reduce Profit? ")

data["Discount Group"] = pd.cut(
    data["Discount"],
    bins=[-0.01, 0, 0.2, 0.5, 1.0],                    # bin boundaries
    labels=["No Discount", "1-20%", "21-50%", ">50%"]  # labels for each bin
)

# Calculate average profit for each discount group
discount_impact = data.groupby("Discount Group")["Profit"].mean().reset_index()
print(discount_impact)

# --- Bar chart with green (profit) and red (loss) colors ---
colors = []
for value in discount_impact["Profit"]:
    if value > 0:
        colors.append("#10B981")  # green for profit
    else:
        colors.append("#EF4444")  # red for loss

plt.figure(figsize=(8, 5))
plt.bar(discount_impact["Discount Group"].astype(str), discount_impact["Profit"], color=colors)
plt.axhline(0, color="black", linewidth=1, linestyle="--")  # horizontal line at 0
plt.title("Average Profit by Discount Level")
plt.xlabel("Discount Range")
plt.ylabel("Average Profit ($)")
plt.tight_layout()
plt.savefig("chart6_discount_impact.png")
plt.close()

print("Chart saved: chart6_discount_impact.png")

# STEP 11: SQL ANALYSIS USING SQLITE
# We can load our data into a mini database and run SQL queries!
# sqlite3 creates an in-memory database (temporary, lives in RAM)

print("\n SQL Queries ")

# Create a connection to an in-memory SQLite database
connection = sqlite3.connect(":memory:")

# Write our DataFrame into the database as a table called "orders"
data.to_sql("orders", connection, index=False, if_exists="replace")

print("Data loaded into SQLite database!")

# SQL Query 1: Top 5 States by Total Sales
query1 = """
    SELECT State,
           ROUND(SUM(Sales), 2)  AS Total_Sales,
           ROUND(SUM(Profit), 2) AS Total_Profit
    FROM orders
    GROUP BY State
    ORDER BY Total_Sales DESC
    LIMIT 5
"""
# pd.read_sql() runs the query and returns result as a DataFrame
result1 = pd.read_sql(query1, connection)
print("\nTop 5 States by Sales:")
print(result1)

# SQL Query 2: Which Customer Segment is Most Profitable? 
query2 = """
    SELECT Segment,
           COUNT(DISTINCT [Customer ID]) AS Customers,
           ROUND(SUM(Sales), 2) AS Total_Sales,
           ROUND(SUM(Profit), 2) AS Total_Profit
    FROM orders
    GROUP BY Segment
    ORDER BY Total_Profit DESC
"""
result2 = pd.read_sql(query2, connection)
print("\nProfit by Customer Segment:")
print(result2)

# SQL Query 3: Shipping Mode Analysis
query3 = """
    SELECT [Ship Mode],
           COUNT(*) AS Total_Orders,
           ROUND(AVG([Days to Ship]), 1) AS Avg_Ship_Days,
           ROUND(SUM(Sales), 2)  AS Revenue
    FROM orders
    GROUP BY [Ship Mode]
    ORDER BY Revenue DESC
"""
result3 = pd.read_sql(query3, connection)
print("\nShipping Mode Performance:")
print(result3)

# Close the database connection when done
connection.close()
print("\nSQL analysis complete!")

# STEP 12: FINAL BUSINESS INSIGHTS

print("\n" + "=" * 60)
print("KEY BUSINESS INSIGHTS")
print("=" * 60)
print("1. Technology has the highest sales but Office Supplies has best profit margin.")
print("2. Tables and Bookcases are LOSING money despite high sales volume.")
print("3. West region generates the most revenue.")
print("4. Discounts above 20% result in NEGATIVE average profit - avoid heavy discounting.")
print("5. Sales peak in Q4 (Oct-Dec) every year - plan inventory accordingly.")
print("6. Consumer segment has most customers; Corporate has highest profit per order.")
print("\nAll 6 charts saved as PNG files in the same folder.")
print("=" * 60)
