from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class Agent:
    id: Optional[int]
    name: str
    category: str
    query: Dict[str, Any]
    created_at: datetime = datetime.now()

    @classmethod
    def from_db_row(cls, row):
        """Create Agent instance from database row"""
        import json
        return cls(
            id=row[0],
            name=row[1],
            category=row[2],
            query=json.loads(row[3]),
            created_at=datetime.fromisoformat(row[4]) if len(row) > 4 else datetime.now()
        )

    def to_dict(self):
        """Convert Agent to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'query': self.query,
            'created_at': self.created_at.isoformat()
        }