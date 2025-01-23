class Node:
    def __init__(self, node_id, parent_id, title, content, collapsed):
        self.node_id = node_id
        self.parent_id = parent_id
        self.title = title
        self.content = content
        self.collapsed = bool(collapsed)
    
    @classmethod
    def from_db_row(cls, row):
        if row is None:
            return None
        return cls(row[0], row[1], row[2], row[3], row[4])
    
    def __repr__(self):
        return f"Node(id={self.node_id}, title={self.title})" 