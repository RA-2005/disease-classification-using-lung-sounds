# Unified Lung Sound Dataset Schema
    
## Audio Standard
- **Format**: WAV (PCM)
- **Sample Rate**: 4,000 Hz
- **Channels**: Mono
- **Bit Depth**: 16-bit
- **Clip Duration**: 5 seconds (20,000 samples)
- **Padding**: Zero-pad if shorter; split if longer into multiple clips

## Global Label Vocabulary (disease_label)
- Normal
- COPD
- Asthma
- Pneumonia
- Bronchiectasis
- Bronchiolitis
- URTI
- Other

## Metadata CSV Columns
| Column | Type | Description |
|--------|------|-------------|
| sample_id | string | Unique ID: DATASET_PATIENTID_CLIPNUM |
| patient_id | string | Original patient ID from source |
| source_dataset | string | ICBHI / KAGGLE / RESP_TR |
| filepath | string | Relative path to processed .wav |
| disease_label | string | One from Global Label Vocabulary |
| age | int | Patient age (optional, -1 if missing) |
| sex | string | M / F / Other (optional) |
| chest_location | string | Anterior_L, Anterior_R, Posterior_L, Posterior_R, Trachea, etc. (optional) |
| recording_device | string | Stethoscope model (optional) |
| severity_level | int | For COPD: 0-4; others: -1 (optional) |
| original_label | string | Original disease label from source dataset |

## Label Mapping Rules

### ICBHI 2017
- Crackles → Adventitious_Sound (optional: disease-level if available)
- Wheezes → Adventitious_Sound
- Normal → Normal
- (If disease-level available) → Map to vocabulary

### Kaggle Lung Dataset
- Healthy → Normal
- COPD → COPD
- Asthma → Asthma
- Bronchiectasis → Bronchiectasis
- Bronchiolitis → Bronchiolitis
- Pneumonia → Pneumonia
- URTI → URTI
- Others → Other

### RespiratoryDatabase@TR
- COPD0 → COPD, severity_level=0
- COPD1 → COPD, severity_level=1
- COPD2 → COPD, severity_level=2
- COPD3 → COPD, severity_level=3
- COPD4 → COPD, severity_level=4
