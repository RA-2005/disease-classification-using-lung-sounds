"""
Master script: Run all preprocessing steps in order
"""
import pandas as pd
from pathlib import Path
from audio_standardizer import AudioStandardizer

def prepare_kaggle(raw_kaggle_path, processed_audio_path, output_metadata_path):
    """
    Process Kaggle Lung Dataset
    
    Kaggle structure (typical):
    - audio files organized by disease folder
    - 001.wav, 002.wav, etc. per disease
    """
    
    raw_kaggle_path = Path(raw_kaggle_path)
    processed_audio_path = Path(processed_audio_path)
    processed_audio_path.mkdir(parents=True, exist_ok=True)
    
    # Kaggle label mapping
    label_mapping = {
        'healthy': 'Normal',
        'COPD': 'COPD',
        'asthma': 'Asthma',
        'bronchiectasis': 'Bronchiectasis',
        'bronchiolitis': 'Bronchiolitis',
        'pneumonia': 'Pneumonia',
        'URTI': 'URTI',
    }
    
    metadata_rows = []
    sample_counter = 1
    
    # Find all audio files in disease subdirectories
    for disease_folder in raw_kaggle_path.iterdir():
        if not disease_folder.is_dir():
            continue
        
        disease_name = disease_folder.name.lower()
        disease_label = label_mapping.get(disease_name, 'Other')
        
        audio_files = list(disease_folder.glob("*.wav"))
        
        for audio_file in audio_files:
            patient_id = f"KAGGLE_{disease_name}_{audio_file.stem}"
            
            # Standardize audio
            processed_filename = f"KAGGLE_{sample_counter:06d}.wav"
            processed_filepath = processed_audio_path / processed_filename
            
            success, error = AudioStandardizer.standardize(str(audio_file), str(processed_filepath))
            
            if success:
                metadata_rows.append({
                    'sample_id': f"KAGGLE_{sample_counter:06d}",
                    'patient_id': patient_id,
                    'source_dataset': 'KAGGLE',
                    'filepath': f"audio/{processed_filename}",
                    'disease_label': disease_label,
                    'age': -1,
                    'sex': 'Other',
                    'chest_location': 'Unknown',
                    'recording_device': 'Unknown',
                    'severity_level': -1,
                    'original_label': disease_name
                })
                sample_counter += 1
                print(f"✓ Processed: {audio_file.name} → {disease_label}")
            else:
                print(f"✗ Failed: {audio_file.name} - {error}")
    
    # Save metadata
    df = pd.DataFrame(metadata_rows)
    df.to_csv(output_metadata_path, index=False)
    print(f"\n✓ Kaggle processing complete: {len(metadata_rows)} samples")
    print(f"  Metadata saved to: {output_metadata_path}")
    
    return df

if __name__ == "__main__":
    prepare_kaggle(
        raw_kaggle_path="data_raw/arashnic-lung-dataset",
        processed_audio_path="data_processed/audio",
        output_metadata_path="data_processed/meta_kaggle.csv"
    )
