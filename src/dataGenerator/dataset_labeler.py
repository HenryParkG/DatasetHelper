import webbrowser
import os

html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset_labeler.html")
webbrowser.open(f"file:///{html_path}")