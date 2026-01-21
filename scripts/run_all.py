"""
Master script: Run all preprocessing steps in order
"""

from prepare_icbhi import prepare_icbhi
from prepare_kaggle import prepare_kaggle
from prepare_resp_tr import prepare_resp_tr
from merge_datasets import merge_all_datasets

print("=" * 60)
print("LUNG SOUND DATASET UNIFICATION PIPELINE")
print("=" * 60)

# Step 1: Process ICBHI
print("\n[STEP 1/4] Processing ICBHI 2017...")
prepare_icbhi(
    raw_icbhi_path="data_raw/ICBHI",
    processed_audio_path="data_processed/audio",
    output_metadata_path="data_processed/meta_icbhi.csv"
)

# Step 2: Process Kaggle
print("\n[STEP 2/4] Processing Kaggle Lung Dataset...")
prepare_kaggle(
    raw_kaggle_path="data_raw/KAGGLE",
    processed_audio_path="data_processed/audio",
    output_metadata_path="data_processed/meta_kaggle.csv"
)

# Step 3: Process RespiratoryDatabase@TR
print("\n[STEP 3/4] Processing RespiratoryDatabase@TR...")
prepare_resp_tr(
    raw_resp_tr_path="data_raw/RESP_TR",
    metadata_csv_path="data_raw/RESP_TR/metadata.csv",
    processed_audio_path="data_processed/audio",
    output_metadata_path="data_processed/meta_resp_tr.csv"
)

# Step 4: Merge all
print("\n[STEP 4/4] Merging all datasets...")
merge_all_datasets(
    meta_icbhi_path="data_processed/meta_icbhi.csv",
    meta_kaggle_path="data_processed/meta_kaggle.csv",
    meta_resp_tr_path="data_processed/meta_resp_tr.csv",
    output_path="data_processed/combined_metadata.csv"
)

print("\n" + "=" * 60)
print("✓ UNIFICATION COMPLETE!")
print("=" * 60)
print("\nYour unified dataset is ready:")
print("  - Audio files: data_processed/audio/")
print("  - Metadata: data_processed/combined_metadata.csv")
print("\nNext steps:")
print("  1. Feature extraction (MFCC, Mel-spectrogram, etc.)")
print("  2. Train/val/test split at patient level")
print("  3. Model training")
