class HTMLReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_html_file(self):
        """Read HTML file with different encodings and return its content."""
        encodings = ['utf-8', 'windows-1252', 'iso-8859-1']  # List of encodings to try
        for encoding in encodings:
            try:
                with open(self.file_path, 'r', encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                print(f"Failed decoding with {encoding}, trying next.")
            except FileNotFoundError:
                print("The file was not found.")
                return None
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

        print("All encoding attempts failed.")
        return None
