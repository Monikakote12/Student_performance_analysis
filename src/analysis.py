from pyspark.sql.functions import avg, max, min

def analyze_data(df):
    print("===== Student Dataset =====")
    df.show()

    print("===== Average Study Hours =====")
    df.select(avg("StudyHours")).show()

    print("===== Maximum Internal Marks =====")
    df.select(max("InternalMarks")).show()

    print("===== Minimum Internal Marks =====")
    df.select(min("InternalMarks")).show()

    print("===== Passed Students =====")
    df.filter(df.Result == "Pass").show()

    print("===== Failed Students =====")
    df.filter(df.Result == "Fail").show()