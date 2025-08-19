# casual_face_detector

Made with https://realpython.com/face-recognition-with-python/ and Vibe Coding

Automate student identification in photos to simplify attendance and photo organization. Uses `face_recognition` for detection and Streamlit for a simple web UI.

---

## Features

- Upload and label student training photos.
- Generate and update face encodings.
- Detect and recognize faces in uploaded photos.
- Rename recognized photos by student names with counters (e.g., `Joao_1.png`).
- Option to save photos with or without bounding boxes.
- Download results as a ZIP archive via Streamlit.

---

## Setup

1. Install dependencies:

```bash
   pip install -r requirements.txt
  ```

   
2. Organize training photos (optional):

```
training/
├── Joao/
└── Maria/
```

3. Run the app
```bash
    streamlit run streamlit_app.py
  ```

---

## Testing locally and Deploying

To test the app locally, just run the "app_core_logic" (`streamlit run app_core_logic.py`)

- This is needed because the production code expects that the url variable is the production one

You should be able to test any module (`modules/`) indepentendely