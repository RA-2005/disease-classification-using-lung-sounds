import pandas as pd
from pathlib import Path
from audio_standardizer import AudioStandardizer

def prepare_resp_tr(
    raw_resp_tr_path="data_raw/ResDatabase/RespiratoryDatabase@TR",
    metadata_excel_path="data_raw/ResDatabase/Labels.xlsx",
    processed_audio_path="data_processed/audio",
    output_metadata_path="data_processed/meta_resp_tr.csv",
):
    # Paths to added 

    raw_resp_tr_path = Path(raw_resp_tr_path)
    processed_audio_path = Path(processed_audio_path)
    processed_audio_path.mkdir(parents=True, exist_ok=True)

    # 1) Load Excel with labels
    meta_df = pd.read_excel(metadata_excel_path)
    # Columns are: 'Patient ID', 'Diagnosis'
    meta_df["patient_id"] = meta_df["Patient ID"].astype(str)
    meta_df["severity"] = meta_df["Diagnosis"].astype(str)

    # Map patient → severity/diagnosis

    patient2severity = dict(zip(meta_df["patient_id"], meta_df["severity"]))

    rows = []
    sample_counter = 1

    # 2) Loop through all wavs under RespiratoryDatabase@TR


    for audio_file in raw_resp_tr_path.rglob("*.wav"):
        # Adjust to your real filename pattern; example: COPD3_patient_001_AL.wav

        parts = audio_file.stem.split("_")

        if len(parts) == 0:
            continue

        severity_class = parts[0]               # e.g. COPD3

        # try to get patient number from filename if present, else "0"

        patient_num = "0"
        if "patient" in parts:
            idx = parts.index("patient")
            if idx + 1 < len(parts):
                patient_num = parts[idx + 1]
        chest_location = parts[-1] if len(parts) > 1 else "Unknown"

        # Override with Excel diagnosis if patient exists there

        severity_from_meta = patient2severity.get(patient_num)
        if isinstance(severity_from_meta, str):
            severity_class = severity_from_meta

        # Map to disease_label + severity_level

        if str(severity_class).startswith("COPD"):
            disease_label = "COPD"
            try:
                severity_level = int(str(severity_class)[-1])
            except ValueError:
                severity_level = -1
        else:
            # non-COPD or textual labels
            
            disease_label = "Other"
            severity_level = -1

        # 3) Standardize audio
        out_name = f"RESP_TR_{sample_counter:06d}.wav"
        out_path = processed_audio_path / out_name

        ok, err = AudioStandardizer.standardize(str(audio_file), str(out_path))
        if not ok:
            print(f"Failed: {audio_file.name} -> {err}")
            continue

        rows.append(
            {
                "sample_id": f"RESP_TR_{sample_counter:06d}",
                "patient_id": f"RESP_TR_{patient_num}",
                "source_dataset": "RESP_TR",
                "filepath": f"audio/{out_name}",
                "disease_label": disease_label,
                "age": -1,
                "sex": "Other",
                "chest_location": chest_location,
                "recording_device": "Littmann_3200",
                "severity_level": severity_level,
                "original_label": str(severity_class),
            }
        )
        print(f"OK: {audio_file.name} -> {disease_label}, sev {severity_level}")
        sample_counter += 1

    df = pd.DataFrame(rows)
    df.to_csv(output_metadata_path, index=False)
    print(f"\nSaved {len(rows)} RESP_TR samples to {output_metadata_path}")

if __name__ == "__main__":
    prepare_resp_tr()
