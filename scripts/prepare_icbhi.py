import pandas as pd
from pathlib import Path
from audio_standardizer import AudioStandardizer

def prepare_icbhi(
    raw_root="data_raw/resp_sounds/Respiratory_Sound_Database",
    processed_audio_path="data_processed/audio",
    output_metadata_path="data_processed/meta_icbhi.csv"
):
    raw_root = Path(raw_root)
    audio_dir = raw_root / "audio_and_txt_files"
    diag_path = raw_root / "patient_diagnosis.csv"

    # 1) load patient-level diagnosis
    diag_df = pd.read_csv(diag_path, header=0)

    # rename weird headers to something meaningful
    diag_df = diag_df.rename(columns={
        "101": "patient_id",
        "URTI": "diagnosis"
    })

    diag_df["patient_id"] = diag_df["patient_id"].astype(str)

    # map diagnosis text -> your unified labels
    diag_map = {
        "COPD": "COPD",
        "Asthma": "Asthma",
        "Pneumonia": "Pneumonia",
        "Bronchiectasis": "Bronchiectasis",
        "Bronchiolitis": "Bronchiolitis",
        "URTI": "URTI",
        "LRTI": "Other",
        "Healthy": "Normal"
    }
    diag_df["disease_label"] = diag_df["diagnosis"].map(
        lambda x: diag_map.get(str(x), "Other")
    )

    patient2label = dict(zip(diag_df["patient_id"], diag_df["disease_label"]))

    processed_audio_path = Path(processed_audio_path)
    processed_audio_path.mkdir(parents=True, exist_ok=True)

    rows = []
    sample_idx = 1

    for wav_path in audio_dir.glob("*.wav"):
        # e.g. 101_1_Tc_mc_AKGC417L.wav → "101"
        patient_id_raw = wav_path.stem.split("_")[0]
        disease_label = patient2label.get(patient_id_raw, "Other")

        out_name = f"ICBHI_{sample_idx:06d}.wav"
        out_path = processed_audio_path / out_name

        ok, err = AudioStandardizer.standardize(str(wav_path), str(out_path))
        if not ok:
            print(f"FAILED: {wav_path.name} -> {err}")
            continue

        parts = wav_path.stem.split("_")
        chest_loc = parts[2] if len(parts) > 2 else "Unknown"
        device = "_".join(parts[4:]) if len(parts) > 4 else "Unknown"

        rows.append({
            "sample_id": f"ICBHI_{sample_idx:06d}",
            "patient_id": f"ICBHI_{patient_id_raw}",
            "source_dataset": "ICBHI",
            "filepath": f"audio/{out_name}",
            "disease_label": disease_label,
            "age": -1,
            "sex": "Other",
            "chest_location": chest_loc,
            "recording_device": device,
            "severity_level": -1,
            "original_label": diag_df.loc[
                diag_df["patient_id"] == patient_id_raw, "diagnosis"
            ].iloc[0] if patient_id_raw in patient2label else "Unknown",
        })
        print(f"OK: {wav_path.name} → {disease_label}")
        sample_idx += 1

    pd.DataFrame(rows).to_csv(output_metadata_path, index=False)
    print(f"\nSaved {len(rows)} samples to {output_metadata_path}")

if __name__ == "__main__":
    prepare_icbhi()
