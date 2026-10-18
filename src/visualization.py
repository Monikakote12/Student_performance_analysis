import pandas as pd
import matplotlib.pyplot as plt

def plot_data(df):
    pdf = df.toPandas()

    plt.figure(figsize=(8,5))
    plt.bar(pdf["Name"], pdf["InternalMarks"])
    plt.title("Student Internal Marks")
    plt.xlabel("Students")
    plt.ylabel("Marks")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()