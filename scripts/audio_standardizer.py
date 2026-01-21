import librosa
import soundfile as sf
import numpy as np
from pathlib import Path

class AudioStandardizer:
    """Convert any audio to unified format: 4kHz, mono, 5 seconds, 16-bit WAV"""
    
    SAMPLE_RATE = 4000
    DURATION_SEC = 5
    TARGET_SAMPLES = SAMPLE_RATE * DURATION_SEC  # 20,000
    
    @staticmethod
    def standardize(input_path, output_path):
        """
        Load audio, resample, convert to mono, pad/trim to 5 seconds, save as WAV
        
        Args:
            input_path: Path to input audio file
            output_path: Path to save standardized WAV
        """
        try:
            # Load audio (librosa auto-detects format)
            audio, sr = librosa.load(input_path, sr=AudioStandardizer.SAMPLE_RATE, mono=True)
            
            # Pad or trim to exactly 5 seconds
            if len(audio) < AudioStandardizer.TARGET_SAMPLES:
                # Zero-pad
                audio = np.pad(audio, (0, AudioStandardizer.TARGET_SAMPLES - len(audio)), mode='constant')
            else:
                # Trim
                audio = audio[:AudioStandardizer.TARGET_SAMPLES]
            
            # Normalize to [-1, 1] range for 16-bit
            audio = audio / (np.max(np.abs(audio)) + 1e-8)
            
            # Save as 16-bit mono WAV
            sf.write(output_path, audio, AudioStandardizer.SAMPLE_RATE, subtype='PCM_16')
            
            return True, None
        except Exception as e:
            return False, str(e)

if __name__ == "__main__":
    # Test example
    AudioStandardizer.standardize("sample.wav", "standardized.wav")
