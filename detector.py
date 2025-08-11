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

    # Build counters dict from existing files
    counters = {}
    for file in OUTPUT_IDENTIFIED_PATH.glob("*.png"):
        # filename like "Joao_2.png" or "Maria_1.png"
        stem = file.stem  # e.g. "Joao_2"
        if "_" in stem:
            name_part, number_part = stem.rsplit("_", 1)
            if number_part.isdigit():
                number = int(number_part)
                counters[name_part] = max(counters.get(name_part, 0), number)
        else:
            # If filename doesn't have _, treat whole as name with counter=0
            counters[stem] = max(counters.get(stem, 0), 0)

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

        detected_names = list(dict.fromkeys(detected_names))  # Remove duplicates keeping order
        names_str = "_".join(detected_names)

        # Update counter for this combined name string
        count = counters.get(names_str, 0) + 1
        counters[names_str] = count

        output_file = OUTPUT_IDENTIFIED_PATH / f"{names_str}_{count}.png"
        pillow_image.save(output_file)

        print(f"{img_path.name} -> {names_str}_{count}")

# Run the process
process_all_images()
