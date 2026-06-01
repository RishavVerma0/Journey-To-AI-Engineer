# 🎬 TMDB Movie Data Analysis

A beginner-level Exploratory Data Analysis (EDA) project on the TMDB 5000 Movie Dataset using Python, Pandas, Matplotlib, and Seaborn.

## 📌 Project Overview

This project explores the TMDB 5000 Movie Dataset to understand trends in movie budgets, revenues, ratings, popularity, runtime, and profitability.

The goal is to practice data cleaning, data exploration, visualization, and extracting insights from real-world data.

---

## 📂 Project Structure

```text
DataAnalysis Project/
│
├── Data/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
├── Notebook/
│   └── TMDB_Movie_Analysis.ipynb
│
└── Output/
    ├── revenue_analysis.png
    ├── rating_distribution.png
    └── runtime_distribution.png
```

---

## 📊 Dataset

Dataset: TMDB 5000 Movie Dataset

Files Used:

- tmdb_5000_movies.csv
- tmdb_5000_credits.csv

Dataset contains information about:

- Movie titles
- Genres
- Budget
- Revenue
- Popularity
- Runtime
- Ratings
- Cast and Crew
- Release Dates

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

---

## 🔍 Analysis Performed

### 1. Data Exploration

- Dataset shape
- Data types
- Summary statistics
- Missing value analysis

### 2. Revenue Analysis

- Highest revenue-generating movies
- Revenue distribution

### 3. Budget Analysis

- Budget distribution
- Budget trends

### 4. Ratings Analysis

- Vote average distribution
- User rating trends

### 5. Popularity Analysis

- Most popular movies
- Popularity comparisons

### 6. Runtime Analysis

- Runtime distribution
- Average movie duration

### 7. Correlation Analysis

Relationships between:

- Budget
- Revenue
- Popularity
- Vote Count
- Runtime

### 8. Profit Analysis

Profit calculated as:

Profit = Revenue − Budget

- Most profitable movies
- Profit trends

### 9. Release Year Analysis

- Movies released per year
- Growth in movie production

---

## 📈 Visualizations

The project includes:

- Bar Charts
- Histograms
- Scatter Plots
- Correlation Heatmaps
- Distribution Plots

---

## 💡 Key Insights

- Most movies have ratings between 6 and 7.
- Revenue generally increases with budget.
- Popular movies tend to receive more votes.
- Most movie runtimes fall between 90 and 120 minutes.
- A small number of blockbuster movies generate exceptionally high profits.
- Movie releases increased significantly after the year 2000.

---

## ▶️ How to Run

1. Clone the repository

```bash
git clone https://github.com/your-username/tmdb-movie-analysis.git
```

2. Install required libraries

```bash
pip install pandas numpy matplotlib seaborn
```

3. Open Jupyter Notebook

```bash
jupyter notebook
```

4. Run the notebook located in the `Notebook` folder.

---

## 📚 Learning Outcomes

Through this project, I learned:

- Data cleaning using Pandas
- Exploratory Data Analysis (EDA)
- Data visualization techniques
- Correlation analysis
- Feature engineering
- Deriving insights from data

---

## 👨‍💻 Author

Your Name

GitHub: https://github.com/your-username

---

## ⭐ Future Improvements

- Genre-wise analysis
- Director analysis
- Cast popularity analysis
- Movie recommendation system
- Interactive dashboard using Plotly or Stream