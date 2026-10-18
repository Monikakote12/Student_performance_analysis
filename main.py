from src.preprocess import load_data
from src.analysis import analyze_data
from src.visualization import plot_data

def main():
    spark, df = load_data()

    analyze_data(df)

    plot_data(df)

    spark.stop()

if __name__ == "__main__":
    main()