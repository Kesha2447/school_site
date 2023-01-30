# -*- coding: utf-8 -*-

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
    def get(db: Session, subject_id: int):
        return db.query(db_models.Subject).filter(db_models.Subject.id == subject_id).first()


    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(db_models.Subject).offset(skip).limit(limit).all()


    @staticmethod
    def create(db: Session, subject: lessons.SubjectCreate):
        subject_dict = subject.dict()
        db_subject = db_models.User(**subject_dict)
        db.add(db_subject)
        db.commit()
        db.refresh(db_subject)
        return db_subject


    @staticmethod
    def update(db: Session, subject: lessons.SubjectCreate):
        return SubjectCrud.create(db, subject)


class LessonCrud:
    '''A class for storing database operations related to lessons'''

    @staticmethod
    def get(db: Session, user_id: int):
        pass


    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        pass


    @staticmethod
    def create(db: Session, user: users.UserCreate):
        pass

    @staticmethod
    def update():
        pass


class ResultCrud:
    '''A class for storing user-related database operations'''

    @staticmethod
    def get_user(db: Session, user_id: int):
        pass


    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        pass


    @staticmethod
    def create_user(db: Session, user: users.UserCreate):
        pass

    @staticmethod
    def update_user():
        pass

