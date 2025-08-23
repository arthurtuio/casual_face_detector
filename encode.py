import face_recognition
import pickle
from pathlib import Path


def encode_known_faces(
        encodings_path,
        training_path,
        model: str = "hog",
) -> None:

    encodings_location = Path(f"{encodings_path}/encodings.pkl")

    names = []
    encodings = []
    for filepath in training_path.glob("*/*"):
        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)

        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)

    name_encodings = {"names": names, "encodings": encodings}
    with encodings_location.open(mode="wb") as f:
        pickle.dump(name_encodings, f)

if __name__ == '__main__':
    encode_known_faces()
