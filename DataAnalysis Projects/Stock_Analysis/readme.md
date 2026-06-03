# S&P 500 Stock Market Analysis

## Overview

This project explores historical stock market data for companies in the S&P 500 index using Python and data analysis libraries. The goal is to clean and transform raw financial data, engineer meaningful features, and perform exploratory analysis to uncover trends in stock performance, volatility, market movements, and recovery patterns.

The project demonstrates practical skills in data cleaning, feature engineering, time-series analysis, and exploratory data analysis using real-world financial data.

---

## Dataset

The analysis uses the **S&P 500 Stocks (Daily Updated)** dataset from Kaggle.

### Dataset Highlights

- Historical stock data for S&P 500 companies
- Daily trading records since 2010
- Open, High, Low, Close (OHLC) prices
- Adjusted Close prices
- Trading Volume

### Available Columns

| Column | Description |
|----------|-------------|
| Date | Trading date |
| Symbol | Stock ticker symbol |
| Open | Opening price |
| High | Highest price of the day |
| Low | Lowest price of the day |
| Close | Closing price |
| Adj Close | Adjusted closing price |
| Volume | Trading volume |

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

---

## Project Structure

```text
sp500-stock-analysis/
│
├── notebooks/
│   └── sp500_analysis.ipynb
│
├── data/
│   └── (excluded from version control)
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Data Preparation

Before analysis, the dataset was cleaned and standardized to ensure consistency and reliability.

### Tasks Performed

- Converted date columns to datetime format
- Removed duplicate records
- Handled missing values
- Verified and corrected data types
- Sorted records by stock symbol and date
- Prepared the dataset for time-series calculations

---

## Feature Engineering

Several new features were created to enhance the analysis and provide additional insights into stock behavior.

### Daily Return

Measures the percentage change in closing price compared to the previous trading day.

### Percentage Change

Measures the percentage difference between opening and closing prices.

### 7-Day Moving Average (MA7)

Provides a short-term view of stock price trends.

### 30-Day Moving Average (MA30)

Provides a medium-term view of stock price trends.

### Volatility

Calculated using the rolling standard deviation of daily returns.

### Volume Change

Measures day-to-day changes in trading volume.

### Engineered Features

- Daily_Return
- pct_change
- MA7
- MA30
- Volatality
- Volume_Change

---

## Exploratory Data Analysis

The exploratory analysis focused on understanding stock performance, market volatility, and significant market events.

### Questions Investigated

#### Which Stocks Performed Best?

Calculated average daily returns for each stock and identified the strongest performers.

#### Which Stocks Were Most Volatile?

Measured the standard deviation of daily returns to determine which stocks experienced the largest price fluctuations.

#### What Did the 2020 COVID-19 Market Crash Look Like?

Analyzed market-wide average returns during the COVID-19 crash period to observe the impact on stock prices.

#### Which Stocks Recovered Fastest?

Compared stock recovery percentages from historical lows to recent closing prices.

#### Does Trading Volume Influence Returns?

Explored the relationship between changes in trading volume and daily stock returns.

---

## Key Insights

- Stock performance varies significantly across companies.
- Some stocks exhibit substantially higher volatility than others.
- The COVID-19 market crash produced a noticeable decline across the market.
- Recovery rates differ considerably between stocks.
- Changes in trading volume do not necessarily correspond to large changes in returns.

---

## Sample Analysis Outputs

- Top-performing stocks by average daily return
- Most volatile stocks
- COVID-19 market crash trends
- Recovery rankings across stocks
- Volume versus return analysis

---

## Skills Demonstrated

- Data Cleaning
- Data Wrangling
- Feature Engineering
- Time-Series Analysis
- Financial Data Analysis
- Exploratory Data Analysis (EDA)
- Statistical Analysis
- Data Visualization
- Python Programming

---

## Future Enhancements

Potential extensions to this project include:

- Correlation analysis between stocks
- Portfolio-level analysis
- Risk and return comparisons
- Predictive modeling
- Interactive dashboards using Plotly or Streamlit

---

## Author

Financial market analysis project developed using Python and historical S&P 500 stock data as part of a data analytics portfolio.