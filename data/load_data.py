import pandas as pd
from datasets import Dataset
from sklearn.model_selection import train_test_split

def load_and_split(tsv):
    df = pd.read_csv(tsv, sep="\t", header=None, on_bad_lines="skip")
    df.columns = ["source", "target"]

    train, temp = train_test_split(df, test_size=0.2, random_state=42)
    val, test = train_test_split(temp, test_size=0.5, random_state=42)

    def to_ds(d):
        return Dataset.from_pandas(d).remove_columns(["__index_level_0__"])

    return to_ds(train), to_ds(val), to_ds(test)
