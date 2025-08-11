import pickle
from collections import Counter
from PIL import Image, ImageDraw
import face_recognition
from config import *


# Ensure output dirs
Path("training").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)
OUTPUT_IDENTIFIED_PATH.mkdir(exist_ok=True)

def _display_face(draw, bounding_box, name):
    top, right, bottom, left = bounding_box
    draw.rectangle(((left, top), (right, bottom)), outline=BOUNDING_BOX_COLOR)
    text_left, text_top, text_right, text_bottom = draw.textbbox(
        (left, bottom), name
    )
    draw.rectangle(
        ((text_left, text_top), (text_right, text_bottom)),
        fill=BOUNDING_BOX_COLOR,
        outline=BOUNDING_BOX_COLOR,
    )
    draw.text((text_left, text_top), name, fill=TEXT_COLOR)


def _recognize_face(unknown_encoding, loaded_encodings):
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )
    votes = Counter(
        name for match, name in zip(boolean_matches, loaded_encodings["names"]) if match
    )
    if votes:
        return votes.most_common(1)[0][0]

def process_all_images(model: str = "hog", encodings_location: Path = DEFAULT_ENCODINGS_PATH):
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

    for img_path in IMAGES_TO_DETECT_PATH.glob("*.*"):
        input_image = face_recognition.load_image_file(img_path)
        input_face_locations = face_recognition.face_locations(input_image, model=model)
        input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)

        if not input_face_encodings:
            print(f"No faces found in {img_path.name}")
            continue

        pillow_image = Image.fromarray(input_image)
        draw = ImageDraw.Draw(pillow_image)

        detected_names = []
        for bounding_box, face_encoding in zip(input_face_locations, input_face_encodings):
            name = _recognize_face(face_encoding, loaded_encodings)
            if not name:
                name = "Unknown"
            detected_names.append(name)
            _display_face(draw, bounding_box, name)

        del draw

        # Remove duplicates while keeping order
        detected_names = list(dict.fromkeys(detected_names))

        # Build filename
        names_str = "_".join(detected_names)
        output_file = OUTPUT_IDENTIFIED_PATH / f"{names_str}_{img_path.name}"
        pillow_image.save(output_file)

        print(f"{img_path.name} -> {names_str}")

# Run the process
process_all_images()
