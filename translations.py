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
        'language': 'Language',
        'settings': 'Settings',
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
        'language': 'Langue',
        'settings': 'Paramètres',
    },
    'es': {
        'window_title': 'NoteNodes',
        'notes': 'Notas',
        'new': 'Nuevo',
        'delete': 'Eliminar',
        'save': 'Guardar',
        'new_node': 'Nueva nota',
        'node_title': 'Título de la nota:',
        'delete_confirm': '¿Realmente desea eliminar esta nota y todos sus hijos?',
        'success': 'Éxito',
        'note_saved': '¡Nota guardada!',
        'confirmation': 'Confirmación',
        'error': 'Error',
        'move_error': 'No se puede mover la nota: {}',
        'language': 'Idioma',
        'settings': 'Ajustes',
    },
    'ko': {
        'window_title': 'NoteNodes',
        'notes': '노트',
        'new': '새로 만들기',
        'delete': '삭제',
        'save': '저장',
        'new_node': '새 노트',
        'node_title': '노트 제목:',
        'delete_confirm': '이 노트와 모든 하위 노트를 삭제하시겠습니까?',
        'success': '성공',
        'note_saved': '노트가 저장되었습니다!',
        'confirmation': '확인',
        'error': '오류',
        'move_error': '노트를 이동할 수 없습니다: {}',
        'language': '언어',
        'settings': '설정',
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