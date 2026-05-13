import pandas as pd

def process_data(input_path, output_path):

    # Read CSV file
    df = pd.read_csv(input_path)

    print("Original Shape:", df.shape)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing values
    df["salary"] = df["salary"].fillna(0)

    print("Processed Shape:", df.shape)

    # Save cleaned CSV
    df.to_csv(output_path, index=False)

    # Convert CSV to parquet
    parquet_path = output_path.replace(".csv", ".parquet")
    df.to_parquet(parquet_path, index=False)

    print("Processing Complete!")

if __name__ == "__main__":

    process_data(
    "data/raw/sample.csv",
    "data/processed/cleaned_data.csv"
)