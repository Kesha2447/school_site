# -*- coding: utf-8 -*-
'''Data models for the database, this file contains data on users and lessons'''

from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, PrimaryKeyConstraint, Float

from db.database import Base, sqlalchemy_engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_teacher = Column(Boolean, default=False)
    last_auth = Column(DateTime)
    photo = Column(String, default=None)

    subjects = relationship('Subject', back_populates='users', secondary='user_subjects')
    results = relationship('Results', back_populates='user')


class Subject(Base):
    __tablename__ = 'subjects'

    title = Column(String, index=True, unique=True, primary_key=True)
    description = Column(String)

    users = relationship('User', back_populates='subjects', secondary='user_subjects')
    lessons = relationship('Lesson', back_populates='subject')


class UserSubject(Base):
    __tablename__ = 'user_subjects'
    __table_args__ = (PrimaryKeyConstraint('user_id', 'subject_title'),)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    subject_title = Column(String, ForeignKey('subjects.title', ondelete='CASCADE'))


class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    record = Column(String)
    homework = Column(String)
    subject_title = Column(String, ForeignKey("subjects.title", ondelete='CASCADE'))

    subject = relationship('Subject', back_populates='lessons')
    results = relationship('Results', back_populates='lesson')


class Results(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    lesson_id = Column(Integer, ForeignKey('lessons.id', ondelete='CASCADE'))

    homework = Column(String)
    homework_score = Column(Float, default=0)
    progress = Column(Float, default=0)

    lesson = relationship('Lesson', back_populates='results')
    user = relationship('User', back_populates='results')


Base.metadata.create_all(bind=sqlalchemy_engine)