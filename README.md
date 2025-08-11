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
