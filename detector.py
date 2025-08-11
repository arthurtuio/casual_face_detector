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

def process_all_images(
    model: str = "hog",
    encodings_location: Path = DEFAULT_ENCODINGS_PATH,
    draw_boxes: bool = False
):
    """
    Process all images in the IMAGES_TO_DETECT_PATH folder to detect and recognize faces,
    then save copies of the images renamed based on detected person names with a counter suffix.

    Parameters:
    - model (str): The face detection model to use ('hog' or 'cnn'). Default is 'hog'. NUNCA MEXI, E PROVAVELMENTE N PRECISA MEXER
    - encodings_location (Path): Path to the pickle file containing known face encodings.
    - draw_boxes (bool): Whether to draw bounding boxes and names on the output images before saving.
                         If False, images are saved without annotations but still renamed accordingly.

    Behavior:
    - Loads known face encodings from the specified encodings_location.
    - Scans existing output files to maintain a per-person naming counter to avoid overwriting.
    - For each image in IMAGES_TO_DETECT_PATH:
        - Detects faces and recognizes known individuals.
        - Builds a filename from the recognized names joined by underscores, with a numeric suffix.
        - Saves a copy of the image (with or without drawn boxes) into OUTPUT_IDENTIFIED_PATH.

    Notes:
    - If multiple people are detected, all their names are concatenated in the filename.
    - Unknown faces are labeled as "Unknown".
    - Original images are not modified or deleted.
    """
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

    # Build counters dict from existing files
    counters = {}
    for file in OUTPUT_IDENTIFIED_PATH.glob("*.png"):
        stem = file.stem
        if "_" in stem:
            name_part, number_part = stem.rsplit("_", 1)
            if number_part.isdigit():
                number = int(number_part)
                counters[name_part] = max(counters.get(name_part, 0), number)
        else:
            counters[stem] = max(counters.get(stem, 0), 0)

    for img_path in IMAGES_TO_DETECT_PATH.glob("*.*"):
        input_image = face_recognition.load_image_file(img_path)
        input_face_locations = face_recognition.face_locations(input_image, model=model)
        input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)

        if not input_face_encodings:
            print(f"No faces found in {img_path.name}")
            continue

        detected_names = []
        if draw_boxes:
            pillow_image = Image.fromarray(input_image)
            draw = ImageDraw.Draw(pillow_image)

        for bounding_box, face_encoding in zip(input_face_locations, input_face_encodings):
            name = _recognize_face(face_encoding, loaded_encodings)
            if not name:
                name = "Unknown"
            detected_names.append(name)
            if draw_boxes:
                _display_face(draw, bounding_box, name)

        if draw_boxes:
            del draw

        detected_names = list(dict.fromkeys(detected_names))
        names_str = "_".join(detected_names)

        count = counters.get(names_str, 0) + 1
        counters[names_str] = count

        output_file = OUTPUT_IDENTIFIED_PATH / f"{names_str}_{count}.png"

        if draw_boxes:
            pillow_image.save(output_file)
        else:
            img_to_save = Image.fromarray(input_image)
            img_to_save.save(output_file)

        print(f"{img_path.name} -> {names_str}_{count}")

# Run the process
process_all_images()
