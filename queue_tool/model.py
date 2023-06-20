from dataclasses import dataclass, field
from datetime import datetime
from typing import Type

from sqlalchemy import Column, DateTime, Integer, String, update
from sqlalchemy.orm import scoped_session

from queue_tool.database import Base
from queue_tool.database import Session

INVALID_JOB: dict = {'item': 'INVALID_JOB_REQUEST', 'valor': 0}

session = Session()

@dataclass
class Job(Base):
    
    __tablename__ = 'jobs'

    hash: str = Column(String, autoincrement=False, primary_key=True, nullable=False)
    item: str = Column('descricao_item', String, nullable=False)
    valor: int = Column(Integer, default=0)
    status: str = Column('status', String, default=False)
    
    create_at: datetime = Column(DateTime, default=datetime.now)
    finished_at: datetime = Column(DateTime, nullable=True)
    
    duration: int = field(init=False)
    
    def __init__(self, data):

        self.hash = data['hash']
        self.item = data['item']
        self.valor = data['valor']
        self.status = 'Em processamento'

    def __str__(self) -> str:
        return str(self.item)

    def __repr__(self) -> str:
        return f"Job(item='{self.item}')"

    @property
    def duration(self) -> int:
        if self.finished_at:
            return (self.finished_at - self.create_at).seconds
        
    def as_dict(self) -> dict:
        return {
            'item': self.item,
            'valor': self.valor,
            'status': self.status,
        }

    def create(self) -> Type['Job']:
        session.add(self)
        session.commit()
        session.refresh(self)

    @staticmethod
    def select(hash: str) -> Type['Job']:
        job = session.query(Job).where(Job.hash == hash).first()
        return job        

    def update(self) -> Type['Job']:
        setattr(self, 'status', 'Finalizado')
        setattr(self, 'finished_at', datetime.now())
        session.commit()
        session.refresh(self)
        
        return self
