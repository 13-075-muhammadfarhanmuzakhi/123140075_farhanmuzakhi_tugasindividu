from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy import inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    review_text = Column(Text, nullable=False)
    product_name = Column(String(255), nullable=True)
    language = Column(String(10), nullable=True, default='id')
    sentiment = Column(String(50), nullable=False)
    confidence_score = Column(Float, nullable=False)
    key_points = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'language': self.language or 'id',
            'review_text': self.review_text,
            'sentiment': self.sentiment,
            'confidence_score': self.confidence_score,
            'key_points': self.key_points,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Ensure existing SQLite table has the new column if DB already exists
try:
    inspector = inspect(engine)
    cols = [col['name'] for col in inspector.get_columns('reviews')]
    if 'product_name' not in cols:
        with engine.connect() as conn:
            conn.execute(text('ALTER TABLE reviews ADD COLUMN product_name VARCHAR(255)'))
            conn.commit()
    if 'language' not in cols:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE reviews ADD COLUMN language VARCHAR(10)"))
            conn.commit()
except Exception:
    # If anything goes wrong (e.g., table doesn't exist yet), ignore and let metadata.create_all handle it
    pass