import pandas as pd

class DatasetProcessor:
    def __init__(self, input_file, output_file=None):
        self.input_file = input_file
        self.output_file = output_file or self._default_parquet_name()
        self.data = None

    def _default_parquet_name(self):
        return self.input_file.rsplit(".", 1)[0] + ".parquet"

    def load_data(self):
        self.data = pd.read_csv(self.input_file)
        print(f"✅ Loaded data: {self.data.shape[0]} rows x {self.data.shape[1]} columns")

    def save_to_parquet(self):
        # Convert object columns to string in one line
        self.data = self.data.astype({col: "string" for col in self.data.select_dtypes(include="object").columns})
        self.data.to_parquet(self.output_file, index=False, engine="pyarrow", compression="snappy")
        print(f"✅ Data saved to Parquet: {self.output_file}")

    def compute_statistics(self):
        numeric_data = self.data.select_dtypes(include="number")
        stats = pd.DataFrame({
            "max": numeric_data.max(),
            "min": numeric_data.min(),
            "mean": numeric_data.mean(),
            "absolute_sum": numeric_data.abs().sum()
        })
        print("\n📊 Column Statistics:")
        print(stats)
        return stats


if __name__ == "__main__":
    input_csv = r"C:\Users\DTMAR\OneDrive\Desktop\automobile\automobile_imports.csv"
    processor = DatasetProcessor(input_csv)

    processor.load_data()
    processor.save_to_parquet()
    processor.compute_statistics()