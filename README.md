# Competitive Coding File Generator

## Project Description
The **Competitive Coding File Generator** is a desktop application designed to streamline the process of setting up coding files for competitive programming contests, particularly on platforms like Codeforces. It features a user-friendly GUI built with PyQt6, a Flask server for communication with a Chrome extension, and automation to generate solution files and test cases based on problem data. The application supports C++, Python, and Java, allowing users to select their preferred language, specify a username, and choose a target folder for file generation. The Chrome extension extracts problem data from Codeforces and sends it to the app for processing.

This project was developed to enhance productivity for competitive programmers by automating repetitive tasks, such as creating solution files and test case files, with a focus on a clean, Sublime Text-inspired dark mode interface.

## Features
- **GUI with PyQt6**: A responsive and modern interface with dynamic input boxes, highlight-only language selection (no radio circles), and a compact layout.
- **Flask Server**: A lightweight server to handle communication between the Chrome extension and the app, running on `http://127.0.0.1:5000`.
- **Chrome Extension**: Extracts problem data (e.g., problem letter, sample inputs/outputs) from Codeforces and sends it to the Flask server.
- **File Generation**: Automatically generates solution files (e.g., `a.cc`, `a.py`, `A.java`) and test case files (e.g., `test_a_1.in`, `test_a_1.out`) based on templates.
- **Responsive Inputs**: Input boxes for username and target folder expand or contract based on text length.
- **Username Persistence**: Saves usernames to a `usernames.json` file for easy reuse.
- **Path Autocompletion**: Suggests folder paths as the user types in the target folder field.
- **Dark Mode**: Sublime Text-inspired dark theme with a dark gray background (`#2D2D2D`), light gray text (`#D0D0D0`), and muted brown highlights/buttons (`#5C4033`).

## Project Structure
```
CompetitiveCodingTool/
│
├── generator_app.py          # Main script for GUI and Flask server
├── templates/                # Template files for file generation
│   ├── template.cpp          # C++ template
│   ├── template.py           # Python template
│   ├── template.java         # Java template
│   └── debug.h               # Debug header for C++
├── chrome_extension/         # Chrome extension files
│   ├── manifest.json         # Extension manifest
│   ├── popup.html            # Extension popup UI
│   └── popup.js              # Extension logic
├── README.md                 # Project documentation
├── requirements.txt          # Dependencies list
└── LICENSE                   # MIT License
```

## Prerequisites
- **Python 3.7+**: Required to run the application.
- **Google Chrome**: For the Chrome extension to interact with Codeforces.
- **Dependencies**:
  - `PyQt6`: For the GUI.
  - `Flask`: For the server.
  - `flask-cors`: For cross-origin requests.
  - `tkinter`: For the file dialog (included with Python on most systems).

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/CompetitiveCodingFileGenerator.git
   cd CompetitiveCodingFileGenerator
   ```

2. **Set Up a Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   - **Directly**:
     ```bash
     python generator_app.py
     ```
   - **As an Executable** (One-Click Setup):
     1. Install PyInstaller:
        ```bash
        pip install pyinstaller
        ```
     2. Package the app:
        ```bash
        pyinstaller --add-data "templates;templates" --onefile --noconsole --name CompetitiveCodingHelper generator_app.py
        ```
        Note: On macOS/Linux, use `:` instead of `;` in `--add-data "templates:templates"`.
     3. Run the executable:
        - On Windows: Double-click `dist/CompetitiveCodingHelper.exe`.
        - On macOS/Linux: Run `dist/CompetitiveCodingHelper` (may need `chmod +x` permissions).

5. **Install the Chrome Extension**:
   1. Open Chrome and go to `chrome://extensions/`.
   2. Enable "Developer mode" (top-right toggle).
   3. Click "Load unpacked" and select the `chrome_extension` folder.
   4. The extension should appear in your Chrome toolbar.

## Usage
1. **Launch the Application**:
   - Run the app using the executable or `python generator_app.py`.
   - The GUI will open with fields for username, language, and target folder.

2. **Configure the App**:
   - Enter your Codeforces username (saved automatically for future use).
   - Select a programming language (C++, Python, or Java).
   - Specify a target folder (use the Browse button or type with autocompletion).

3. **Use the Chrome Extension**:
   - Navigate to a Codeforces problem page (e.g., a contest problem).
   - Click the extension icon in Chrome’s toolbar.
   - The extension will send problem data to the app.

4. **Generate Files**:
   - Click the "Generate" button in the app.
   - The app will create solution files (e.g., `a.cc`) and test case files (e.g., `test_a_1.in`, `test_a_1.out`) in the specified folder.

## Skills Learned
Through this project, I have gained the following skills and knowledge:

- **Python Programming**:
  - Advanced file handling and directory management (`os`, `shutil`, `glob`).
  - Working with JSON for data persistence (`usernames.json`).
  - Threading for running a Flask server alongside a GUI (`threading`).

- **GUI Development with PyQt6**:
  - Building a desktop application with a modern, dark-themed interface.
  - Creating responsive layouts with `QVBoxLayout` and `QHBoxLayout`.
  - Implementing dynamic input boxes that expand/contract using `QSizePolicy.Expanding`.
  - Customizing widget styles with QSS (Qt Style Sheets) to remove radio button indicators and apply highlights.
  - Handling user interactions (e.g., button clicks, text changes) with signals and slots.
  - Adding path autocompletion using `QListWidget`.

- **Flask Server Integration**:
  - Setting up a lightweight Flask server to handle HTTP requests.
  - Using `flask-cors` to enable cross-origin requests between the Chrome extension and the app.
  - Running a server in a separate thread to avoid blocking the GUI.

- **Chrome Extension Development**:
  - Creating a Chrome extension to scrape problem data from Codeforces.
  - Communicating with a local server via HTTP POST requests.
  - Note: Since I’m already familiar with HTML, the focus was on JavaScript (`popup.js`) and Chrome API integration.

- **Packaging and Distribution**:
  - Using PyInstaller to package a Python application into a standalone executable.
  - Handling resource files (e.g., `templates` folder) in a packaged app with `sys._MEIPASS`.
  - Creating a one-click executable for easy usage.

- **Version Control with Git**:
  - Setting up a Git repository and pushing to GitHub.
  - Writing clear commit messages and maintaining a clean project structure.
  - Documenting a project with a detailed `README.md`.

- **Problem-Solving and Debugging**:
  - Resolving issues like QSS parsing errors in PyQt6.
  - Handling threading conflicts between Flask and PyQt6.
  - Debugging Flask server communication with the Chrome extension.

## Technologies Used
- **Python 3.7+**: Core programming language.
- **PyQt6**: GUI framework for the desktop application.
- **Flask**: Lightweight web server for communication.
- **flask-cors**: Handling cross-origin requests.
- **tkinter**: File dialog for folder selection.
- **PyInstaller**: Packaging the app into an executable.
- **Git/GitHub**: Version control and repository hosting.
- **Chrome Extension APIs**: For browser integration.

## Future Improvements
- Add support for more competitive programming platforms (e.g., LeetCode, AtCoder).
- Implement a feature to save and load folder paths for quicker reuse.
- Enhance the GUI with additional customization options (e.g., themes, font sizes).
- Add error logging to a file for better debugging in the packaged app.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to the PyQt6 and Flask communities for their excellent documentation.
- Inspired by the need to automate repetitive tasks in competitive programming.
```
---
