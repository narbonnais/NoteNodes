import sys
from PyQt5.QtWidgets import QApplication
import database
from ui_main import MainWindow

def main():
    # Initialiser la base de données
    database.init_db()
    
    # Lancer l'application Qt
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 