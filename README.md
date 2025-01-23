# NoteNodes

NoteNodes is a hierarchical note-taking application that allows you to organize your notes in a tree structure. It supports Markdown formatting and provides a live preview of your notes.

## Features

- Hierarchical organization of notes in a tree structure
- Markdown support with live preview
- Drag and drop functionality to reorganize notes
- Multi-language support (English, French, Spanish, Korean)
- Keyboard shortcuts for common operations
- Context menu for quick actions
- Automatic saving of tree state (expanded/collapsed nodes)

## Requirements

- Python 3.x
- PyQt5
- Markdown
- Pygments (for code highlighting)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/notenodes.git
cd notenodes
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate # On Unix/macOS
```

or

```bash
.\venv\Scripts\activate # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

### Basic Operations

- **Create a new note**: Click the "New" button or use the context menu
- **Delete a note**: Select a note and click "Delete" or use the context menu
- **Save changes**: Click "Save" or use Ctrl+S (Cmd+S on macOS)
- **Rename a note**: Double-click the note title or use the context menu
- **Move notes**: Drag and drop notes to reorganize them
- **Change language**: Settings → Language → Select your preferred language

### Keyboard Shortcuts

- **Ctrl+S** (Cmd+S on macOS): Save current note
- More shortcuts coming soon...

## Project Structure

- `main.py`: Application entry point
- `ui_main.py`: Main user interface implementation
- `database.py`: Database operations
- `models.py`: Data models
- `translations.py`: Internationalization support
- `utils.py`: Utility functions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
