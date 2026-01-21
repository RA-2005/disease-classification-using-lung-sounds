import pandas as pd
from pathlib import Path

def merge_all_datasets(meta_icbhi_path, meta_kaggle_path, meta_resp_tr_path, output_path):
    """
    Combine all three dataset metadata CSVs into one unified CSV
    """
    
    print("Loading individual metadata files...")
    
    # Load each dataset's metadata
    df_icbhi = pd.read_csv(meta_icbhi_path)
    df_kaggle = pd.read_csv(meta_kaggle_path)
    df_resp_tr = pd.read_csv(meta_resp_tr_path)
    
    print(f"  ICBHI: {len(df_icbhi)} samples")
    print(f"  KAGGLE: {len(df_kaggle)} samples")
    print(f"  RESP_TR: {len(df_resp_tr)} samples")
    
    # Concatenate
    combined_df = pd.concat([df_icbhi, df_kaggle, df_resp_tr], ignore_index=True)
    
    # Reset sample_id to be globally unique
    combined_df['sample_id'] = [f"UNIFIED_{i:06d}" for i in range(len(combined_df))]
    
    # Save
    combined_df.to_csv(output_path, index=False)
    
    print(f"\n✓ Merged successfully!")
    print(f"  Total samples: {len(combined_df)}")
    print(f"  Combined metadata saved to: {output_path}")
    
    # Print summary statistics
    print("\n--- Dataset Summary ---")
    print(f"Samples per source:\n{combined_df['source_dataset'].value_counts()}")
    print(f"\nDisease distribution:\n{combined_df['disease_label'].value_counts()}")
    print(f"\nCOPD severity distribution:\n{combined_df[combined_df['disease_label']=='COPD']['severity_level'].value_counts()}")
    
    return combined_df

if __name__ == "__main__":
    merge_all_datasets(
        meta_icbhi_path="data_processed/meta_icbhi.csv",
        meta_kaggle_path="data_processed/meta_kaggle.csv",
        meta_resp_tr_path="data_processed/meta_resp_tr.csv",
        output_path="data_processed/combined_metadata.csv"
    )
