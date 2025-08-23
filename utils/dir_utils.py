import shutil
from pathlib import Path



def _add_folder_prefix_to_username(logged_username):
    return f"user__{logged_username}"

class DirUtils:
    def __init__(self, logged_username):
        self.user_folder = _add_folder_prefix_to_username(logged_username)

    def create_user_paths(self):
        """
        Creates user-specific directories for training, detection and output.
        Returns the 4 paths as Path objects.
        """
        base = Path(self.user_folder)

        training_dir = base / "training"
        detect_dir = base / "images_to_detect"
        output_dir = base / "output" / "identified_photos"
        encondings_dir = base / "output"

        for p in [training_dir, detect_dir, output_dir]:
            p.mkdir(parents=True, exist_ok=True)

        return training_dir, detect_dir, output_dir, encondings_dir


    def wipe_user_paths(self):
        """Deletes all user-specific directories (safe cleanup)."""
        print(f"Cleaning up user '{self.user_folder}' folder")
        if not self.user_folder:
            return

        base = Path(self.user_folder)
        if base.exists() and base.is_dir():
            shutil.rmtree(base, ignore_errors=True)
