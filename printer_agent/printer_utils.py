import os
import platform

def send_to_printer(file_path):
    """
    Sends the document to the default printer.
    """
    try:
        if platform.system() == "Windows":
            os.startfile(file_path, "print")  # Windows default print command
        elif platform.system() == "Linux":
            os.system(f"lp {file_path}")  # Linux print command
        elif platform.system() == "Darwin":
            os.system(f"lp {file_path}")  # macOS print command
        else:
            raise Exception("Unsupported OS for printing.")

        return True
    except Exception as e:
        print(f"Printing failed: {e}")
        return False
