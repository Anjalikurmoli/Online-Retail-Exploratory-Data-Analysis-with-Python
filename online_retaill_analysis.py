
# Import the necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Data
file = "Online Retail.xlsx"
df = pd.read_excel(file)
print(df.head())
print(df.info())
print(df.describe())

# Exploring the dataset
print(df['InvoiceDate'].min(), df['InvoiceDate'].max())
print(df['Country'].value_counts())

# Visualizing the sales trends
# Monthly sales
df['Month'] = df['InvoiceDate'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Quantity'].sum()
monthly_sales.plot(kind='line', title="Monthly Sales")
plt.show()

# Top Products
top_products = df.groupby('Description')['Quantity'].sum().nlargest(10)
top_products.plot(kind='bar', title="Top products")
plt.show()

# Country-wise Sales
country_sales = df.groupby('Country')['Quantity'].sum().sort_values(ascending=False)
country_sales.head(10).plot(kind='bar', title='Top 10 Countries by Sales')
plt.show()

# Clean and Validate the Data
# Checking for missing values
print(df.isnull().sum())

# Handling missing values
df = df.dropna(subset=['CustomerID'])

# Removing duplicates
df = df.drop_duplicates()

# Checking for any outliers in Quantity and UnitPrice
sns.boxplot(x=df['Quantity'])
plt.show()
sns.boxplot(x=df['UnitPrice'])
plt.show()

# Removing any invalid entries
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Analyzing the data
# Customer Behaviour
frequent_customers = df.groupby('CustomerID')['InvoiceNo'].count().nlargest(10)
print(frequent_customers)

# Average spending per customer
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
avg_spending = df.groupby('CustomerID')['TotalPrice'].mean()
print(avg_spending.describe())

# Seasonal Trends
# Monthly Sales Trends
df['Month'] = df['InvoiceDate'].dt.month
monthly_sales = df.groupby('Month')['TotalPrice'].sum()
monthly_sales.plot(kind='line', title='Monthly Sales Trend', figsize=(10,6))
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.show()

# Weekly Sales Trends
df['Weekday'] = df['InvoiceDate'].dt.day_name()
weekday_sales = df.groupby('Weekday')['TotalPrice'].sum()
weekday_sales = weekday_sales.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
weekday_sales.plot(kind='bar', title='Sales by Weekday', figsize=(10,6))
plt.xlabel('Day of the Week')
plt.ylabel('Total Sales')
plt.show()

# Yearly seasonal trends
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month
yearly_sales = df.groupby(['Year', 'Month'])['TotalPrice'].sum().unstack()
yearly_sales.plot(kind='line', figsize=(12,6))
plt.title('Year-over-Year Monthly Sales')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.legend(title='Year')
plt.show()
