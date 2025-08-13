from pathlib import Path

import pandas as pd


def process_real_gdp_per_capita():
    """
    Process real GDP per capita data by splitting date into year and month columns
    and removing the original date column.
    """
    # Setup paths
    raw_dir = Path("data/raw/real_gdp_per_capita")
    processed_dir = Path("data/processed/real_gdp_per_capita")
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Find the real GDP per capita CSV file
    csv_files = list(raw_dir.glob("real_gdp_per_capita_last_*.csv"))
    
    if not csv_files:
        print("No real GDP per capita CSV files found in raw directory")
        return

    input_file = csv_files[0]  # Use the first (should be only one)
    print(f"Processing {input_file.name}...")

    # Load the data
    df = pd.read_csv(input_file)
    
    print(f"  • Loaded {len(df)} records")
    print(f"  • Columns: {list(df.columns)}")

    # Convert date column to datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        
        # Extract year and month
        df['year'] = df['date'].dt.strftime('%Y')
        df['month'] = df['date'].dt.strftime('%m')
        
        # Remove the original date column
        df = df.drop('date', axis=1)
        
        # Reorder columns to have year and month first
        cols = ['year', 'month'] + [col for col in df.columns if col not in ['year', 'month']]
        df = df[cols]
        
        print(f"  • Split date into year/month columns")
        print(f"  • Date range: {df['year'].min()}-{df['month'].min()} to {df['year'].max()}-{df['month'].max()}")
        
    else:
        print("  ⚠ No 'date' column found")
        return

    # Save processed data
    output_path = processed_dir / "real_gdp_per_capita_processed.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✓ Processed data saved to {output_path}")
    print(f"  • Final columns: {list(df.columns)}")
    
    # Show sample of processed data
    print(f"\nSample of processed data:")
    print(df.head().to_string(index=False))
    
    return df


if __name__ == "__main__":
    process_real_gdp_per_capita()