from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

class Videos(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, index=True)
    creator_id = Column(String, nullable=False)
    video_created_at = Column(DateTime, nullable=False)
    views_count = Column(Integer)
    likes_count = Column(Integer)
    comments_count = Column(Integer)
    reports_count = Column(Integer)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class VideoSnapshots(Base):
    __tablename__ = "video_snapshots"

    id = Column(String, primary_key=True)
    video_id = Column(String, ForeignKey('videos.id'), nullable=False)
    views_count = Column(Integer)
    likes_count = Column(Integer)
    comments_count  = Column(Integer)
    reports_count = Column(Integer)
    delta_views_count = Column(Integer)
    delta_likes_count = Column(Integer)
    delta_comments_count = Column(Integer)
    delta_reports_count = Column(Integer)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autoflush=False, bind=engine, expire_on_commit=False)
