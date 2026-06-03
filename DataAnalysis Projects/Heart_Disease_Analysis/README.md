# ❤️ Heart Disease Prediction — Mini Data Science Project

A beginner-friendly Machine Learning project that predicts heart disease using real patient data. Built with Python in a Jupyter Notebook, with every step explained in plain English.

---

## 📌 Project Overview

| | |
|---|---|
| **Domain** | Healthcare / Medical |
| **Dataset** | Heart Disease UCI (Kaggle) |
| **Goal** | Predict whether a patient has heart disease |
| **Type** | Binary Classification |
| **Level** | Beginner–Intermediate |

---

## 📂 Files

```
📁 project/
├── heart_disease_analysis.ipynb   ← Main Jupyter Notebook
└── README.md                      ← You are here
```

---

## 🗂️ Dataset

**Source:** [Heart Disease UCI — Kaggle](https://www.kaggle.com/datasets/ronitf/heart-disease-uci)

- **303 patients**, 14 columns
- No missing values
- Target: `1` = Has heart disease, `0` = No heart disease

### Column Reference

| Column | Meaning |
|--------|---------|
| `age` | Patient's age in years |
| `sex` | 1 = Male, 0 = Female |
| `cp` | Chest pain type (0–3) |
| `trestbps` | Resting blood pressure (mmHg) |
| `chol` | Serum cholesterol (mg/dl) |
| `fbs` | Fasting blood sugar > 120 mg/dl (1 = Yes) |
| `restecg` | Resting ECG results (0–2) |
| `thalach` | Maximum heart rate achieved |
| `exang` | Exercise induced angina (1 = Yes) |
| `oldpeak` | ST depression induced by exercise |
| `slope` | Slope of peak exercise ST segment |
| `ca` | Number of major vessels (0–3) |
| `thal` | Thalassemia type |
| `target` | **1 = Heart disease, 0 = No heart disease** |

---

## 🛠️ Libraries Used

```python
pandas        # Data manipulation
numpy         # Numerical operations
matplotlib    # Plotting charts
seaborn       # Prettier visualizations
scikit-learn  # Machine learning models & metrics
```

Install all at once:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

---

## 🔬 What the Notebook Covers

### Step-by-Step Breakdown

1. **Import Libraries** — All tools explained with comments
2. **Load Dataset** — Auto-loads from URL with a built-in fallback
3. **Explore Data** — Shape, data types, missing value check
4. **Visualize Data** — Age distribution, correlation heatmap, feature comparisons
5. **Prepare Data** — Train/test split (80/20) and feature scaling
6. **Train Models** — Three ML models built and trained
7. **Compare Models** — Side-by-side accuracy and AUC chart
8. **Evaluate** — Confusion matrix and classification report
9. **Predict** — Run a prediction for a new hypothetical patient
10. **Summary** — Key findings and next steps

---

## 🤖 Models Compared

| Model | How It Works |
|-------|-------------|
| **Logistic Regression** | Draws a boundary line to separate the two groups |
| **Decision Tree** | Asks a series of Yes/No questions like a flowchart |
| **Random Forest** | 100 decision trees that vote together on the answer |

---

## 📊 Sample Results

| Model | Accuracy | AUC Score |
|-------|----------|-----------|
| Logistic Regression | ~82% | ~0.89 |
| Decision Tree | ~78% | ~0.78 |
| **Random Forest** | **~85%** | **~0.91** |

> Results may vary slightly due to random state and dataset version.

---

## ▶️ How to Run

### Option 1 — Kaggle (Recommended, no setup needed)
1. Go to [kaggle.com/code](https://www.kaggle.com/code)
2. Click **New Notebook**
3. Upload `heart_disease_analysis.ipynb`
4. Click **Run All**

### Option 2 — Jupyter Locally
```bash
# Clone or download the files, then:
pip install pandas numpy matplotlib seaborn scikit-learn notebook
jupyter notebook heart_disease_analysis.ipynb
```

### Option 3 — Google Colab
1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Upload the `.ipynb` file
3. Click **Runtime → Run All**

---

## 💡 Key Concepts Explained

**Why scale the data?**
Features like age (29–77) and cholesterol (126–564) have very different ranges. Scaling puts them on the same level so the model doesn't think cholesterol is more important just because its numbers are bigger.

**Why train/test split?**
We keep 20% of data hidden from the model during training, then test on it. Like studying from a textbook and then taking an unseen exam — it checks if the model truly learned or just memorized.

**Why Recall matters in healthcare?**
Missing a patient who actually has disease (false negative) is more dangerous than a false alarm. A high Recall means we're catching most of the sick patients.

---

## 🚀 Ideas to Extend This Project

- [ ] Try **XGBoost** or **Gradient Boosting** for better accuracy
- [ ] Add **cross-validation** for more reliable evaluation
- [ ] Use **GridSearchCV** to tune model hyperparameters
- [ ] Add **SHAP values** to explain individual predictions
- [ ] Build a simple **Streamlit web app** for the predictor
- [ ] Try the larger [Cleveland Heart Disease dataset](https://archive.ics.uci.edu/ml/datasets/Heart+Disease)

---

## ⚠️ Disclaimer

This project is built **for educational purposes only**. The predictions made by these models should never be used for actual medical diagnosis. Always consult a qualified healthcare professional.

---

## 👤 Author

Built as a beginner-friendly Data Science mini project.  
Dataset credit: [Kaggle — Heart Disease UCI](https://www.kaggle.com/datasets/ronitf/heart-disease-uci)
