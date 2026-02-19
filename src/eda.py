import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def basic_overview(df):
    """Print dataset shape, info, and missing values."""
    print("🔍 Dataset Shape:", df.shape)
    print("\n📄 Data Types:\n", df.dtypes)
    print("\n🧮 Missing Values:\n", df.isnull().sum())

def plot_top10_total_cases(df):
    """Plot top 10 countries by total COVID-19 cases."""
    top = (
        df[df['iso_code'].str.len() == 3]
        .groupby('location')['total_cases']
        .max()
        .sort_values(ascending=False)
        .head(10)
    )
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top.values, y=top.index, palette='Oranges')
    plt.title("Top 10 Countries by Total COVID-19 Cases")
    plt.xlabel("Total Cases")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.show()

def plot_top10_total_deaths(df):
    """Plot top 10 countries by total COVID-19 deaths."""
    top = (
        df[df['iso_code'].str.len() == 3]
        .groupby('location')['total_deaths']
        .max()
        .sort_values(ascending=False)
        .head(10)
    )
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top.values, y=top.index, palette='Reds')
    plt.title("Top 10 Countries by Total COVID-19 Deaths")
    plt.xlabel("Total Deaths")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.show()

def plot_correlation_heatmap(df):
    """Plot correlation heatmap for numeric features."""
    numeric_df = df.select_dtypes(include='number').dropna(axis=1)
    corr = numeric_df.corr()

    plt.figure(figsize=(18,12))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("🔗 Correlation Matrix of COVID-19 Metrics")
    plt.tight_layout()
    plt.show()

