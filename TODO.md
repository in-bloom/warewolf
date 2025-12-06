# Warewolf - Audio Processing Pipeline

## ✅ Completed

### Data Import & DB

- [x] SQLite database schema (recordings + sequences tables)
- [x] Database connection utilities (`db_conn.py`)
- [x] CRUD operations for recordings (`insert_recordings`, `delete_recordings`, `get_recordings`)
- [x] CRUD operations for sequences (`insert_sequences`, `delete_sequences`, `get_sequences`, `update_sequence`)
- [x] Data loader to index files from folder (`data_loader.py`)
- [x] CLI interface for import (`main.py`)
- [x] Unit tests for CRUD operations
- [x] Streamlit web UI for data import and management (`ui_test_main.py`)

## 🔄 In Progress

### Data Cleaning & Splitting

- [ ] Audio analysis module (`clean.py` / `audio_processor.py`)
  - [ ] Audio file reading (librosa)
  - [ ] Split raw audio into sequences/clips
  - [ ] Detect silence and split points
  - [ ] Use pyaudioanalysis for sequence detection
  - [ ] Store sequence metadata in DB (timestamp, duration, label)

## 📋 To Do

### Data Processing

- [ ] Feature extraction
  - [ ] FFT analysis on audio sequences
  - [ ] MFCC (Mel-frequency cepstral coefficients)
  - [ ] Spectral features
  - [ ] Store features in DB

### Data Labeling

- [ ] Labeling interface (`labels.py`)
  - [ ] Web UI component for manual annotation
  - [ ] Bulk labeling options
  - [ ] Category management
  - [ ] Update sequence labels in DB

### Machine Learning

- [ ] Model architecture definition
  - [ ] CNN/RNN for audio classification
  - [ ] Training pipeline
  - [ ] Model evaluation metrics
- [ ] Training script (`train.py`)
  - [ ] Load features from DB
  - [ ] Train/validation/test split
  - [ ] Hyperparameter tuning
- [ ] Inference/Prediction (`predict.py`)
  - [ ] Load trained model
  - [ ] Classify new audio sequences
  - [ ] Store predictions in DB

### UI/UX Enhancements

- [ ] Add delete recordings functionality to web UI
- [ ] Add visualization dashboard (charts, metrics)
- [ ] Real-time import progress
- [ ] Export functionality (CSV, JSON)

### Deployment & Distribution

- [ ] Create `requirements.txt` with all dependencies
- [ ] Package project for distribution (pip installable)
- [ ] Docker containerization (optional)
- [ ] Documentation & setup guide
