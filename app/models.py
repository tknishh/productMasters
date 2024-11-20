from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class Agent:
    id: Optional[int]
    name: str
    expertise: str
    description: str
    agent_type: str
    query: Dict[str, Any]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    is_active: bool = True

    @classmethod
    def from_db_row(cls, row):
        """Create Agent instance from database row"""
        import json
        return cls(
            id=row[0],
            name=row[1],
            expertise=row[2],
            description=row[3],
            agent_type=row[4],
            query=json.loads(row[5]),
            created_at=datetime.fromisoformat(row[6]) if len(row) > 6 else datetime.now(),
            updated_at=datetime.fromisoformat(row[7]) if len(row) > 7 else datetime.now(),
            is_active=row[8] if len(row) > 8 else True
        )

    def to_dict(self):
        """Convert Agent to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'expertise': self.expertise,
            'description': self.description,
            'agent_type': self.agent_type,
            'query': self.query,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active
        }