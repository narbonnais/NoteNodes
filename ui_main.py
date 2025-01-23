from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QTextEdit, QLabel, QInputDialog, QMessageBox, QSplitter,
    QMenu, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import database
from models import Node
from utils import markdown_to_html

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("CherryTree Clone")
        self.resize(1200, 800)
        
        # Layout principal
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        # Splitter principal
        self.splitter = QSplitter(Qt.Horizontal)
        
        # -- Panneau gauche --
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_panel.setLayout(self.left_layout)
        
        # Arbre des nœuds avec support du drag & drop
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Notes")
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDragDropMode(QTreeWidget.InternalMove)
        self.tree.itemClicked.connect(self.on_item_click)
        self.tree.itemExpanded.connect(self.on_item_expanded)
        self.tree.itemCollapsed.connect(self.on_item_collapsed)
        self.tree.dropEvent = self.handleDropEvent
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        self.left_layout.addWidget(self.tree)
        
        # Boutons de gestion des nœuds
        self.buttons_layout = QHBoxLayout()
        
        self.btn_add = QPushButton("Nouveau")
        self.btn_add.clicked.connect(self.add_node)
        self.buttons_layout.addWidget(self.btn_add)
        
        self.btn_delete = QPushButton("Supprimer")
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
        
        # Zone d'édition
        self.editor = QTextEdit()
        self.editor.textChanged.connect(self.on_text_changed)
        self.editor.setMinimumHeight(200)  # Set minimum height
        self.editor_layout.addWidget(self.editor)
        
        # Bouton de sauvegarde
        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.clicked.connect(self.save_content)
        self.editor_layout.addWidget(self.btn_save)
        
        # Preview container
        self.preview_container = QWidget()
        self.preview_layout = QVBoxLayout()
        self.preview_container.setLayout(self.preview_layout)
        
        # Aperçu HTML
        self.preview_label = QLabel()
        self.preview_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 10px;
                border: 1px solid #dee2e6;
                border-radius: 4px;
            }
        """)
        self.preview_label.setWordWrap(True)
        self.preview_label.setAlignment(Qt.AlignTop)
        self.preview_label.setTextFormat(Qt.RichText)
        self.preview_label.setMinimumHeight(200)  # Set minimum height
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
    
    def load_tree_nodes(self, parent_id, parent_item):
        children = database.get_children(parent_id)
        for row in children:
            node_id, p_id, title, content, collapsed = row
            item = QTreeWidgetItem([title])
            item.setData(0, Qt.UserRole, node_id)
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
    
    def save_content(self):
        if self.current_node_id is not None:
            content = self.editor.toPlainText()
            database.update_node(self.current_node_id, content=content)
            QMessageBox.information(self, "Succès", "Note enregistrée !")
    
    def add_node(self):
        title, ok = QInputDialog.getText(self, "Nouveau nœud", "Titre du nœud:")
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
            
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment supprimer ce nœud et tous ses enfants ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
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
            # Accepter l'événement pour permettre le déplacement visuel
            QTreeWidget.dropEvent(self.tree, event)
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Impossible de déplacer le nœud : {str(e)}")
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
        new_action = context_menu.addAction("Nouveau nœud")
        delete_action = context_menu.addAction("Supprimer")
        
        # Get the item at the clicked position
        item = self.tree.itemAt(position)
        if item:
            self.current_node_id = item.data(0, Qt.UserRole)
        else:
            self.current_node_id = None
            
        # Enable/disable delete action based on whether an item is selected
        delete_action.setEnabled(item is not None)
        
        # Show the menu and get the chosen action
        action = context_menu.exec_(self.tree.viewport().mapToGlobal(position))
        
        # Handle the chosen action
        if action == new_action:
            self.add_node()
        elif action == delete_action:
            self.delete_node() 