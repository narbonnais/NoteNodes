from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QTextEdit, QTextBrowser, QInputDialog, QMessageBox, QSplitter,
    QMenu, QSizePolicy, QComboBox, QMainWindow, QMenuBar, QAction
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import database
from models import Node
from utils import markdown_to_html
from translations import Translator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.translator = Translator()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(self.translator.get_text('window_title'))
        self.resize(1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Layout principal
        self.layout = QHBoxLayout()
        central_widget.setLayout(self.layout)
        
        # Splitter principal
        self.splitter = QSplitter(Qt.Horizontal)
        
        # -- Panneau gauche --
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_panel.setLayout(self.left_layout)
        
        # Arbre des nœuds avec support du drag & drop
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel(self.translator.get_text('notes'))
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDragDropMode(QTreeWidget.InternalMove)
        self.tree.itemClicked.connect(self.on_item_click)
        self.tree.itemExpanded.connect(self.on_item_expanded)
        self.tree.itemCollapsed.connect(self.on_item_collapsed)
        self.tree.dropEvent = self.handleDropEvent
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        self.tree.setEditTriggers(QTreeWidget.EditKeyPressed | QTreeWidget.DoubleClicked)
        self.tree.itemChanged.connect(self.on_item_renamed)
        self.left_layout.addWidget(self.tree)
        
        # Boutons de gestion des nœuds
        self.buttons_layout = QHBoxLayout()
        
        self.btn_add = QPushButton(self.translator.get_text('new'))
        self.btn_add.clicked.connect(self.add_node)
        self.buttons_layout.addWidget(self.btn_add)
        
        self.btn_delete = QPushButton(self.translator.get_text('delete'))
        self.btn_delete.clicked.connect(self.delete_node)
        self.buttons_layout.addWidget(self.btn_delete)
        
        self.left_layout.addLayout(self.buttons_layout)
        
        # -- Panneau droit --
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout()
        self.right_panel.setLayout(self.right_layout)
        
        # Create vertical splitter for editor and preview
        self.right_splitter = QSplitter(Qt.Vertical)
        
        # Editor container
        self.editor_container = QWidget()
        self.editor_layout = QVBoxLayout()
        self.editor_container.setLayout(self.editor_layout)
        
        # Zone d'édition - force plain text
        self.editor = QTextEdit()
        self.editor.setAcceptRichText(False)
        self.editor.textChanged.connect(self.on_text_changed)
        self.editor.setMinimumHeight(200)
        self.editor_layout.addWidget(self.editor)
        
        # Bouton de sauvegarde
        self.btn_save = QPushButton(self.translator.get_text('save'))
        self.btn_save.clicked.connect(self.save_content)
        self.editor_layout.addWidget(self.btn_save)
        
        # Preview container
        self.preview_container = QWidget()
        self.preview_layout = QVBoxLayout()
        self.preview_container.setLayout(self.preview_layout)
        
        # Remplacer QLabel par QTextBrowser pour l'aperçu
        self.preview_label = QTextBrowser()
        self.preview_label.setOpenExternalLinks(True)
        self.preview_label.setStyleSheet("""
            QTextBrowser {
                background-color: #f8f9fa;
                padding: 10px;
                border: 1px solid #dee2e6;
                border-radius: 4px;
            }
        """)
        self.preview_label.setMinimumHeight(200)
        self.preview_layout.addWidget(self.preview_label)
        
        # Add containers to right splitter
        self.right_splitter.addWidget(self.editor_container)
        self.right_splitter.addWidget(self.preview_container)
        
        # Add right splitter to right layout
        self.right_layout.addWidget(self.right_splitter)
        
        # Ajouter les panneaux au splitter
        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)
        
        # Ajouter le splitter au layout principal
        self.layout.addWidget(self.splitter)
        
        # Variable pour stocker l'ID du nœud sélectionné
        self.current_node_id = None
        
        # Charger l'arbre initial
        self.load_tree_nodes(None, self.tree.invisibleRootItem())
        
        # Set size policies for panels
        self.left_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.right_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        # Set size policy for preview label to prevent auto-expansion
        self.preview_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        # Set size policy for editor to prevent auto-expansion
        self.editor.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        # Set size policy for tree to prevent auto-expansion
        self.tree.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        # Add this line at the end of init_ui
        self.setMinimumSize(800, 600)  # Set minimum size
        
        # Update text for existing widgets
        self.tree.setHeaderLabel(self.translator.get_text('notes'))
        self.btn_add.setText(self.translator.get_text('new'))
        self.btn_delete.setText(self.translator.get_text('delete'))
        self.btn_save.setText(self.translator.get_text('save'))
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # Settings menu
        settings_menu = menubar.addMenu(self.translator.get_text('settings'))
        
        # Language submenu
        language_menu = settings_menu.addMenu(self.translator.get_text('language'))
        
        # Language actions
        english_action = QAction('English', self)
        english_action.setData('en')
        english_action.triggered.connect(self.change_language)
        
        french_action = QAction('Français', self)
        french_action.setData('fr')
        french_action.triggered.connect(self.change_language)
        
        spanish_action = QAction('Español', self)
        spanish_action.setData('es')
        spanish_action.triggered.connect(self.change_language)
        
        korean_action = QAction('한국어', self)
        korean_action.setData('ko')
        korean_action.triggered.connect(self.change_language)
        
        language_menu.addAction(english_action)
        language_menu.addAction(french_action)
        language_menu.addAction(spanish_action)
        language_menu.addAction(korean_action)
    
    def change_language(self):
        action = self.sender()
        lang_code = action.data()
        self.translator.set_language(lang_code)
        self.update_ui_texts()
        # Update menu texts
        settings_menu = self.menuBar().actions()[0].menu()
        settings_menu.setTitle(self.translator.get_text('settings'))
        settings_menu.actions()[0].menu().setTitle(self.translator.get_text('language'))
    
    def update_ui_texts(self):
        """Update all UI texts after language change"""
        self.setWindowTitle(self.translator.get_text('window_title'))
        self.tree.setHeaderLabel(self.translator.get_text('notes'))
        self.btn_add.setText(self.translator.get_text('new'))
        self.btn_delete.setText(self.translator.get_text('delete'))
        self.btn_save.setText(self.translator.get_text('save'))
    
    def load_tree_nodes(self, parent_id, parent_item):
        children = database.get_children(parent_id)
        for row in children:
            node_id, p_id, title, content, collapsed = row
            item = QTreeWidgetItem([title])
            item.setData(0, Qt.UserRole, node_id)
            self.make_item_editable(item)  # Make the new item editable
            parent_item.addChild(item)
            
            if collapsed:
                item.setExpanded(False)
            else:
                item.setExpanded(True)
            
            self.load_tree_nodes(node_id, item)
    
    def on_item_click(self, item, column):
        node_id = item.data(0, Qt.UserRole)
        self.current_node_id = node_id
        node_data = database.get_node(node_id)
        if node_data:
            node = Node.from_db_row(node_data)
            self.editor.setPlainText(node.content)
            self.update_preview(node.content)
    
    def on_item_expanded(self, item):
        node_id = item.data(0, Qt.UserRole)
        database.update_node(node_id, collapsed=0)
    
    def on_item_collapsed(self, item):
        node_id = item.data(0, Qt.UserRole)
        database.update_node(node_id, collapsed=1)
    
    def update_preview(self, markdown_text):
        html = markdown_to_html(markdown_text)
        self.preview_label.setText(html)
    
    def on_text_changed(self):
        content = self.editor.toPlainText()
        self.update_preview(content)
    
    def translate_standard_buttons(self, message_box):
        """Translate standard buttons in a QMessageBox"""
        for button in message_box.buttons():
            if message_box.standardButton(button) == QMessageBox.Yes:
                button.setText(self.translator.get_text('standard_yes'))
            elif message_box.standardButton(button) == QMessageBox.No:
                button.setText(self.translator.get_text('standard_no'))
            elif message_box.standardButton(button) == QMessageBox.Cancel:
                button.setText(self.translator.get_text('standard_cancel'))
            elif message_box.standardButton(button) == QMessageBox.Ok:
                button.setText(self.translator.get_text('standard_ok'))
    
    def save_content(self):
        if self.current_node_id is not None:
            content = self.editor.toPlainText()
            database.update_node(self.current_node_id, content=content)
            msg = QMessageBox(self)
            msg.setWindowTitle(self.translator.get_text('success'))
            msg.setText(self.translator.get_text('note_saved'))
            msg.setStandardButtons(QMessageBox.Ok)
            self.translate_standard_buttons(msg)
            msg.exec_()
    
    def add_node(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle(self.translator.get_text('new_node'))
        dialog.setLabelText(self.translator.get_text('node_title'))
        dialog.setOkButtonText(self.translator.get_text('standard_ok'))
        dialog.setCancelButtonText(self.translator.get_text('standard_cancel'))
        
        ok = dialog.exec_()
        title = dialog.textValue()
        
        if ok and title:
            new_id = database.create_node(
                title, 
                parent_id=self.current_node_id,
                content="",
                collapsed=0
            )
            self.tree.clear()
            self.load_tree_nodes(None, self.tree.invisibleRootItem())
    
    def delete_node(self):
        if self.current_node_id is None:
            return
            
        msg = QMessageBox(self)
        msg.setWindowTitle(self.translator.get_text('confirmation'))
        msg.setText(self.translator.get_text('delete_confirm'))
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.translate_standard_buttons(msg)
        reply = msg.exec_()
        
        if reply == QMessageBox.Yes:
            database.delete_node(self.current_node_id)
            self.current_node_id = None
            self.editor.clear()
            self.preview_label.clear()
            self.tree.clear()
            self.load_tree_nodes(None, self.tree.invisibleRootItem())
    
    def handleDropEvent(self, event):
        # Récupérer l'item déplacé et sa nouvelle position
        item = self.tree.currentItem()
        target = self.tree.itemAt(event.pos())
        
        if not item or not target:
            event.ignore()
            return
            
        # Éviter de déplacer un nœud sur lui-même
        if item == target:
            event.ignore()
            return
            
        # Récupérer les IDs des nœuds
        node_id = item.data(0, Qt.UserRole)
        new_parent_id = target.data(0, Qt.UserRole)
        
        # Mettre à jour la base de données
        try:
            self.update_node_parent(node_id, new_parent_id)
            QTreeWidget.dropEvent(self.tree, event)
        except Exception as e:
            QMessageBox.warning(
                self, 
                self.translator.get_text('error'),
                self.translator.get_text('move_error').format(str(e))
            )
            event.ignore()

    def update_node_parent(self, node_id, new_parent_id):
        # Vérifier qu'on ne crée pas de cycle
        current = new_parent_id
        while current is not None:
            if current == node_id:
                raise ValueError("Impossible de déplacer un nœud sous un de ses descendants")
            node_data = database.get_node(current)
            if node_data:
                current = node_data[1]  # parent_id
            else:
                current = None
        
        # Mettre à jour le parent_id dans la base de données
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE nodes 
            SET parent_id = ? 
            WHERE id = ?
        """, (new_parent_id, node_id))
        conn.commit()
        conn.close()

    def show_context_menu(self, position):
        # Create context menu
        context_menu = QMenu(self)
        
        # Add actions
        new_action = context_menu.addAction(self.translator.get_text('new_node'))
        rename_action = context_menu.addAction(self.translator.get_text('rename'))
        delete_action = context_menu.addAction(self.translator.get_text('delete'))
        
        # Get the item at the clicked position
        item = self.tree.itemAt(position)
        if item:
            self.current_node_id = item.data(0, Qt.UserRole)
        else:
            self.current_node_id = None
            
        # Enable/disable actions based on whether an item is selected
        rename_action.setEnabled(item is not None)
        delete_action.setEnabled(item is not None)
        
        # Show the menu and get the chosen action
        action = context_menu.exec_(self.tree.viewport().mapToGlobal(position))
        
        # Handle the chosen action
        if action == new_action:
            self.add_node()
        elif action == rename_action:
            self.tree.editItem(item, 0)
        elif action == delete_action:
            self.delete_node()

    def on_item_renamed(self, item, column):
        """Handle item rename events"""
        if column == 0:  # Title column
            node_id = item.data(0, Qt.UserRole)
            new_title = item.text(0)
            if new_title.strip():  # Don't allow empty titles
                database.update_node(node_id, title=new_title)
            else:
                # Revert to original title if empty
                node_data = database.get_node(node_id)
                if node_data:
                    item.setText(0, node_data[2])  # Set back to original title

    def make_item_editable(self, item):
        item.setFlags(item.flags() | Qt.ItemIsEditable)