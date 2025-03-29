import sys
import os
import shutil
import datetime
import json
import glob
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QRadioButton, QButtonGroup, QLineEdit, QPushButton, QListWidget, QMessageBox, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
from tkinter import filedialog  # Import tkinter for file dialog

# Flask app setup
flask_app = Flask(__name__)
CORS(flask_app)

# Global variable to store problems received from the extension
problems_data = None

# Flask route to receive problem data from the extension
@flask_app.route('/receive_problems', methods=['POST'])
def receive_problems():
    global problems_data
    problems_data = request.json
    print("Received problems:", problems_data)  # Debug log
    return jsonify({"message": "Problems received successfully"})

# Main Window Class
class GeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Competitive Coding File Generator")
        self.setGeometry(100, 100, 600, 300)  # Adjusted height to reduce empty space
        self.setStyleSheet("background-color: #2D2D2D;")  # Dark gray background

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)  # Reduced spacing for tighter layout

        # Title
        title_label = QLabel("Competitive Coding File Generator")
        title_label.setFont(QFont("Consolas", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #D0D0D0;")  # Light gray
        main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        username_label.setStyleSheet("color: #D0D0D0;")
        username_layout.addWidget(username_label)
        self.username_combo = QComboBox()
        self.username_combo.setFont(QFont("Consolas", 12))
        self.username_combo.setEditable(True)  # Make editable
        self.username_combo.setStyleSheet("background-color: #3A3A3A; color: #D0D0D0; border: 1px solid #555555; border-radius: 5px; padding: 5px;")
        self.username_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Responsive width
        self.username_combo.setMinimumWidth(150)  # Minimum width to avoid too small size
        username_layout.addWidget(self.username_combo, stretch=1)  # Allow expansion
        main_layout.addLayout(username_layout)
        self.load_usernames()

        # Language Selection
        language_layout = QHBoxLayout()
        language_label = QLabel("Language:")
        language_label.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        language_label.setStyleSheet("color: #D0D0D0;")
        language_layout.addWidget(language_label)
        self.language_group = QButtonGroup()
        languages = ["C++", "Python", "Java"]
        for i, lang in enumerate(languages):
            radio = QRadioButton(lang)
            radio.setFont(QFont("Consolas", 12))
            radio.setStyleSheet("""
                color: #D0D0D0;
                background-color: none;
                border: none;
                padding: 2px;
                spacing: 10px;
            """)
            if i == 0:
                radio.setChecked(True)
            radio.toggled.connect(lambda checked, r=radio: self.highlight_radio(r) if checked else None)
            language_layout.addWidget(radio)
            self.language_group.addButton(radio)
        main_layout.addLayout(language_layout)

        # Target Folder
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Target Folder:")
        folder_label.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        folder_label.setStyleSheet("color: #D0D0D0;")
        folder_layout.addWidget(folder_label)
        self.folder_edit = QLineEdit()
        self.folder_edit.setFont(QFont("Consolas", 12))
        self.folder_edit.setStyleSheet("background-color: #3A3A3A; color: #D0D0D0; border: 1px solid #555555; border-radius: 5px; padding: 5px;")
        self.folder_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Responsive width
        self.folder_edit.setMinimumWidth(150)  # Minimum width to avoid too small size
        folder_layout.addWidget(self.folder_edit, stretch=1)  # Allow expansion
        browse_button = QPushButton("Browse")
        browse_button.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        browse_button.setStyleSheet("""
            background-color: #5C4033;
            color: #D0D0D0;
            border-radius: 5px;
            padding: 5px;
            border: 1px solid #6D4B3A;
            min-width: 80px;
        """)
        browse_button.setFixedWidth(80)  # Smaller button
        browse_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(browse_button)
        main_layout.addLayout(folder_layout)

        # Autocomplete setup
        self.suggestion_list = QListWidget()
        self.suggestion_list.setFont(QFont("Consolas", 10))
        self.suggestion_list.setStyleSheet("background-color: #3A3A3A; color: #D0D0D0; border: 1px solid #555555; border-radius: 5px;")
        self.suggestion_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Responsive width
        self.suggestion_list.setMinimumWidth(150)  # Match minimum input width
        self.suggestion_list.hide()
        main_layout.addWidget(self.suggestion_list)
        self.folder_edit.textChanged.connect(self.autocomplete_path)
        self.suggestion_list.itemClicked.connect(self.select_suggestion)

        # Generate Button
        generate_button = QPushButton("Generate")
        generate_button.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        generate_button.setStyleSheet("""
            background-color: #5C4033;
            color: #D0D0D0;
            border-radius: 5px;
            padding: 8px;
            border: 1px solid #6D4B3A;
            min-width: 100px;
        """)
        generate_button.setFixedWidth(100)  # Adjusted for "Generate"
        generate_button.clicked.connect(self.generate_files)
        main_layout.addWidget(generate_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Instruction Label
        instruction_label = QLabel("Ensure the 'Competitive Coding Helper' extension is enabled in chrome://extensions/")
        instruction_label.setFont(QFont("Consolas", 10))
        instruction_label.setStyleSheet("color: #D0D0D0;")
        main_layout.addWidget(instruction_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Bottom Message
        bottom_label = QLabel("Happy Coding!")
        bottom_label.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        bottom_label.setStyleSheet("color: #D0D0D0;")
        main_layout.addWidget(bottom_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Start Flask server in a separate thread
        self.start_flask_server()

    def load_usernames(self):
        # Load previously used usernames from JSON file
        try:
            with open("usernames.json", "r") as f:
                usernames = json.load(f)
        except FileNotFoundError:
            usernames = []
        self.username_combo.addItems(usernames)

    def save_username(self, username):
        # Save new username to JSON file
        try:
            with open("usernames.json", "r") as f:
                usernames = json.load(f)
        except FileNotFoundError:
            usernames = []
        if username and username not in usernames:
            usernames.append(username)
            with open("usernames.json", "w") as f:
                json.dump(usernames, f)
            self.username_combo.clear()
            self.username_combo.addItems(usernames)

    def highlight_radio(self, radio):
        # Unhighlight all other radio buttons and highlight the selected one
        for btn in self.language_group.buttons():
            if btn == radio and radio.isChecked():
                btn.setStyleSheet("""
                    color: #D0D0D0;
                    background-color: #5C4033;
                    border-radius: 5px;
                    padding: 2px;
                """)
            else:
                btn.setStyleSheet("""
                    color: #D0D0D0;
                    background-color: none;
                    border: none;
                    padding: 2px;
                """)

    def browse_folder(self):
        try:
            folder = filedialog.askdirectory()
            if folder:
                self.folder_edit.setText(folder)
                self.suggestion_list.hide()
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Error selecting folder: {str(e)}")

    def autocomplete_path(self):
        partial_path = self.folder_edit.text().strip()
        if not partial_path:
            self.suggestion_list.hide()
            return

        # Get directory suggestions
        try:
            base_path = os.path.dirname(partial_path) if os.path.dirname(partial_path) else "."
            search_pattern = os.path.join(base_path, partial_path.split("/")[-1] + "*")
            suggestions = [path for path in glob.glob(search_pattern) if os.path.isdir(path)]
        except Exception:
            suggestions = []

        # Update the suggestion list
        self.suggestion_list.clear()
        if suggestions:
            self.suggestion_list.addItems(suggestions)
            self.suggestion_list.show()
        else:
            self.suggestion_list.hide()

    def select_suggestion(self, item):
        self.folder_edit.setText(item.text())
        self.suggestion_list.hide()

    def start_flask_server(self):
        def run_flask():
            flask_app.run(port=5000, debug=False, use_reloader=False, host="127.0.0.1")
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

    def generate_files(self):
        global problems_data
        username = self.username_combo.currentText().strip()
        language = next((btn.text() for btn in self.language_group.buttons() if btn.isChecked()), "C++")
        folder = self.folder_edit.text().strip()

        if not all([username, language, folder]):
            QMessageBox.critical(self, "Error", "All fields must be filled.")
            return

        if not problems_data:
            QMessageBox.critical(self, "Error", "No problems data received. Ensure the extension is working.")
            return

        # Save username for future use
        self.save_username(username)

        # Determine contest id, platform, and problems list.
        if isinstance(problems_data, dict) and "contestId" in problems_data:
            contest_id = problems_data["contestId"]
            platform = problems_data.get("platform", "Codeforces")
            problems = problems_data["problems"]
        else:
            contest_id = "Unknown"
            platform = "Codeforces"
            problems = problems_data

        # Create contest folder named "<platform>_<contestId>"
        contest_folder = os.path.join(folder, f"{platform}_{contest_id}")
        try:
            os.makedirs(contest_folder, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot create contest folder: {str(e)}")
            return

        # Create a README in the contest folder listing contest info and problems
        readme_lines = []
        readme_lines.append(f"# {platform} Contest {contest_id}")
        readme_lines.append("")
        readme_lines.append(f"Platform: {platform}")
        readme_lines.append(f"Contest ID: {contest_id}")
        if platform.lower() == "codeforces":
            readme_lines.append(f"URL: https://codeforces.com/contest/{contest_id}")
        elif platform.lower() == "atcoder":
            readme_lines.append(f"URL: https://atcoder.jp/contests/{contest_id}")
        readme_lines.append("")
        readme_lines.append("## Problems")
        readme_lines.append("")
        for prob in problems:
            letter = prob.get("letter", "Unknown")
            samples = prob.get("samples", [])
            readme_lines.append(f"### Problem {letter}")
            readme_lines.append(f"- URL: (Not available via generator)")
            readme_lines.append(f"- Test Cases: {len(samples)}")
            readme_lines.append("")
        readme_content = "\n".join(readme_lines)
        readme_path = os.path.join(contest_folder, "README.md")
        try:
            with open(readme_path, "w") as f:
                f.write(readme_content)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot write README: {str(e)}")
            return

        # Load language template.
        templates_dir = os.path.join(os.path.dirname(__file__), "./templates")
        if not os.path.exists(templates_dir):
            templates_dir = os.path.join(sys._MEIPASS, "templates") if hasattr(sys, '_MEIPASS') else os.path.join(os.path.dirname(__file__), "templates")
        if not os.path.exists(templates_dir):
            QMessageBox.critical(self, "Error", "Templates folder not found.")
            return

        templates = {
            "C++": ("template.cpp", ".cc"),
            "Python": ("template.py", ".py"),
            "Java": ("Main.java", ".java")
        }
        if language not in templates:
            QMessageBox.critical(self, "Error", f"Unsupported language: {language}")
            return

        template_file, ext = templates[language]
        template_path = os.path.join(templates_dir, template_file)
        if not os.path.exists(template_path):
            QMessageBox.critical(self, "Error", f"Template file {template_file} not found in templates/")
            return
        try:
            with open(template_path, "r") as f:
                template_content = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error reading template file: {str(e)}")
            return

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # For each problem, create a subfolder and generate solution and test files.
        for prob in problems:
            letter = prob.get("letter", "Unknown")
            samples = prob.get("samples", [])
            # Create problem folder: "Problem_<letter>"
            problem_folder = os.path.join(contest_folder, f"Problem_{letter}")
            try:
                os.makedirs(problem_folder, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Cannot create problem folder for {letter}: {str(e)}")
                continue

            # Generate solution file using the template.
            content = template_content.replace("${USERNAME}", username)
            content = content.replace("${TASK}", letter)
            content = content.replace("${LANGUAGE}", language)
            content = content.replace("${T}", str(len(samples)))
            if language == "Java":
                file_name = "Main" + ext  # Use Main.java for Java
            else:
                file_name = "solution" + ext
            file_path = os.path.join(problem_folder, file_name)
            try:
                with open(file_path, "w") as f:
                    f.write(content)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Cannot write solution file for {letter}: {str(e)}")
                continue

            # Generate test files: test.in and test-expected.out.
            test_in_path = os.path.join(problem_folder, "test.in")
            test_out_path = os.path.join(problem_folder, "test-expected.out")
            try:
                with open(test_in_path, "w") as f_in, open(test_out_path, "w") as f_out:
                    for sample_in, sample_out in samples:
                        f_in.write(sample_in)
                        if not sample_in.endswith("\n"):
                            f_in.write("\n")
                        f_out.write(sample_out)
                        if not sample_out.endswith("\n"):
                            f_out.write("\n")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Cannot write test files for {letter}: {str(e)}")
                continue

        QMessageBox.information(self, "Success", f"Files generated successfully in {contest_folder}")
        problems_data = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneratorApp()
    window.show()
    sys.exit(app.exec())