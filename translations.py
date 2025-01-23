TRANSLATIONS = {
    'en': {
        'window_title': 'NoteNodes',
        'notes': 'Notes',
        'new': 'New',
        'delete': 'Delete',
        'save': 'Save',
        'new_node': 'New node',
        'node_title': 'Node title:',
        'delete_confirm': 'Do you really want to delete this node and all its children?',
        'success': 'Success',
        'note_saved': 'Note saved!',
        'confirmation': 'Confirmation',
        'error': 'Error',
        'move_error': 'Cannot move node: {}',
    },
    'fr': {
        'window_title': 'NoteNodes',
        'notes': 'Notes',
        'new': 'Nouveau',
        'delete': 'Supprimer',
        'save': 'Enregistrer',
        'new_node': 'Nouveau nœud',
        'node_title': 'Titre du nœud:',
        'delete_confirm': 'Voulez-vous vraiment supprimer ce nœud et tous ses enfants ?',
        'success': 'Succès',
        'note_saved': 'Note enregistrée !',
        'confirmation': 'Confirmation',
        'error': 'Erreur',
        'move_error': 'Impossible de déplacer le nœud : {}',
    }
}

class Translator:
    def __init__(self):
        self.current_language = 'en'
    
    def set_language(self, lang_code):
        if lang_code in TRANSLATIONS:
            self.current_language = lang_code
    
    def get_text(self, key):
        return TRANSLATIONS[self.current_language].get(key, key) 