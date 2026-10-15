import pandas as pd
import os

def clean_dataset(raw_data_path="data/raw/synthetic_student_data.csv", output_path="data/processed/cleaned_data.csv"):
    """Loads raw data, handles missing values, and exports cleaned data."""
    # Ensure processed directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df = pd.read_csv(raw_data_path)
    
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Fill missing numerical values with the median
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(num_cols) > 0:
        df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    
    # Fill missing categorical values with the mode
    cat_cols = df.select_dtypes(include=['object']).columns
    if len(cat_cols) > 0:
        df[cat_cols] = df[cat_cols].fillna(df[cat_cols].mode().iloc[0])
    
    # Save the cleaned dataset
    df.to_csv(output_path, index=False)
    return df

if __name__ == "__main__":
    print("Cleaning dataset...")
    clean_dataset()
    print("Cleaned data saved to data/processed/cleaned_data.csv")