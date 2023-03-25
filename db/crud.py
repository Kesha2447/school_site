# -*- coding: utf-8 -*-

from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.orm import Session

from models import *
from models import db_models, users, lessons


class UserCrud:
    '''A class for storing user-related database operations'''

    @staticmethod
    def get(db: Session, user_id: int):
        return db.query(db_models.User).filter(db_models.User.id == user_id).first()


    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(db_models.User).filter(db_models.User.email == email).first()


    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(db_models.User).offset(skip).limit(limit).all()


    @staticmethod
    def create(db: Session, user: users.UserCreate):
        user_dict = user.dict()
        user_dict['last_auth'] = datetime.now()
        db_user = db_models.User(**user_dict)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


    @staticmethod
    def update(db: Session, user: users.User):
        user_dict = user.dict()
        user_dict.pop('id')
        user_dict.pop('email')

        if user_dict.get('last_auth') is None:
            user_dict['last_auth'] = datetime.now()

        db_user = db_models.User(**user_dict)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


class SubjectCrud:
    '''A class for storing database operations related to school subjects'''

    @staticmethod
    def get(db: Session, subject_title: str):
        return db.query(db_models.Subject).filter(db_models.Subject.title == subject_title).first()


    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(db_models.Subject).offset(skip).limit(limit).all()


    @staticmethod
    def create(db: Session, subject: lessons.SubjectCreate):
        subject_dict = subject.dict()
        db_subject = db_models.Subject(**subject_dict)
        db.add(db_subject)
        db.commit()
        db.refresh(db_subject)
        return db_subject


    @staticmethod
    def update(db: Session, subject: lessons.SubjectCreate):
        return SubjectCrud.create(db, subject)
    
    
    @staticmethod
    def delete(db: Session, subject_title: str):
        i = db.query(db_models.Subject).filter(db_models.Subject.title == subject_title).first()
        db.delete(i)
        db.commit()        
        

class LessonCrud:
    '''A class for storing database operations related to lessons'''

    @staticmethod
    def get(db: Session, lesson_id: int):
        return db.query(db_models.Lesson).filter(db_models.Lesson.id == lesson_id).first()


    @staticmethod
    def get_all(db: Session, subject: str, skip: int = 0, limit: int = 100):
        return db.query(db_models.Lesson).filter(db_models.Lesson.subject_title == subject).order_by(db_models.Lesson.title).offset(skip).limit(limit).all()


    @staticmethod
    def create(db: Session, lesson: lessons.LessonCreate):
        lesson_dict = lesson.dict()
            
        db_lesson = db_models.Lesson(**lesson_dict)
        db.add(db_lesson)
        db.commit()
        db.refresh(db_lesson)
        return db_lesson


    @staticmethod
    def update(db: Session, lesson_id: int, column_name, data):
        db.query(db_models.Lesson).filter(db_models.Lesson.id == lesson_id).update({column_name: data})
        db.commit()
    
    
    @staticmethod
    def delete(db: Session, lesson_id: int):
        i = db.query(db_models.Lesson).filter(db_models.Lesson.id == lesson_id).first()
        db.delete(i)
        db.commit()


class ResultCrud:
    '''A class for storing user-related database operations'''

    @staticmethod
    def get(db: Session, user_id: int, lesson_id: int):
        return db.query(db_models.Results).filter(db_models.Results.user_id == user_id, db_models.Results.lesson_id == lesson_id).first()


    @staticmethod
    def get_all(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return db.query(db_models.Results).filter(db_models.Results.user_id == user_id).offset(skip).limit(limit).all()


    @staticmethod
    def create(db: Session, result: lessons.Result):
        result_dict = result.dict()
        db_result = db_models.Results(**result_dict)
        db.add(db_result)
        db.commit()
        db.refresh(db_result)
        return db_result
    
    
    @staticmethod
    def update(db: Session, result_id: int, column_name, data):
        db.query(db_models.Results).filter(db_models.Results.id == result_id).update({column_name: data})
        db.commit()    



