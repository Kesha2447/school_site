# -*- coding: utf-8 -*-
'''Endpoints for working with subject and lessons'''

from typing import Union, List
from fastapi import Depends, APIRouter, File
from db.database import get_db
from sqlalchemy.orm import Session
from custom_exceptions import exceptions
from models.lessons import SubjectCreate, LessonCreate, ResultCreate
from db.crud import SubjectCrud, LessonCrud, ResultCrud
from models import users
from dependencies import security

subject_router = APIRouter(prefix='/subject', tags=['Subject'])
lesson_router = APIRouter(prefix='/lesson', tags=['Lesson'])
result_router = APIRouter(prefix='/result', tags=['Result'])


@subject_router.get('/all')
async def get_subject(db: Session = Depends(get_db)):
    subjects = SubjectCrud.get_all(db)
    
    return subjects


@subject_router.get('/{title}')
async def get_subjects(title: str, db: Session = Depends(get_db)):
    subject = SubjectCrud.get(db, title)
    
    if subject is None:
        raise exceptions.SUBJECT_NOT_FOUNT_ERROR
    
    return subject


@subject_router.post('/add')
async def add_subject(subject: SubjectCreate, db: Session = Depends(get_db), current_user: users.User = Depends(security.get_current_user)):
    last = SubjectCrud.get(db, subject.title)
    
    if not last is None:
        raise exceptions.SUBJECT_NOT_UNIQUE_ERROR
    
    subject_in_db = SubjectCrud.create(db, subject)
    
    if subject_in_db:
        return {"status": 0, "subjectTitle": subject_in_db.title}
    
    return {"status": 1} 


@subject_router.delete('/{title}')
async def del_subject(title: str, db: Session = Depends(get_db), current_user: users.User = Depends(security.get_current_user)):
    SubjectCrud.delete(db, title)
    
    return {"status": 0}


@lesson_router.get('/all')
async def get_lessons(subject: str, db: Session = Depends(get_db)):
    lessons = LessonCrud.get_all(db, subject=subject)
    
    return lessons


@lesson_router.post('/add')
async def add_lesson(lesson: LessonCreate, db: Session = Depends(get_db), current_user: users.User = Depends(security.get_current_user)):
    lesson_in_db = LessonCrud.create(db, lesson)
    
    if lesson_in_db:
        return {"status": 0, "lesson_id": lesson_in_db.id}
    
    return {"status": 1} 


@lesson_router.delete('/{id}')
async def del_lesson(id: int, db: Session = Depends(get_db), current_user: users.User = Depends(security.get_current_user)):
    LessonCrud.delete(db, id)
    
    return {"status": 0}


@lesson_router.get('/addHomework')
async def add_homework(lesson_id: int, homework: str, db: Session = Depends(get_db), current_user: users.User = Depends(security.get_current_user)):
    
    LessonCrud.update(db, lesson_id, 'homework', homework)
    
    return {"status": 0}


@lesson_router.get('/addVideo')
async def add_video(lesson_id: int, record: str, db: Session = Depends(get_db), current_user: users.User = Depends(security.get_current_user)):
    LessonCrud.update(db, lesson_id, 'record', record)
    
    return {"status": 0}


@lesson_router.get('/{id}')
async def get_lesson(id: int, db: Session = Depends(get_db)):
    lesson = LessonCrud.get(db, id)
    
    if lesson is None:
        raise exceptions.SUBJECT_NOT_FOUNT_ERROR
    
    return lesson


@result_router.post('/add')
async def add_result(result: ResultCreate, db: Session = Depends(get_db)):
    result_in_db = ResultCrud.create(db, result)
    
    if result_in_db:
        #result_in_db.homework = result_in_db.lesson.homework
        
        return {"status": 0, "result": result_in_db}
    
    return {"status": 1} 


@result_router.post('/addHomework/{result_id}')
async def add_homework(result_id: int, file: List[bytes] = File(), db: Session = Depends(get_db)):
    
    ResultCrud.update(db, result_id, 'homework', file)
    
    return {"status": 0}


@result_router.get('/all/{userId}')
async def get_results(userId: int, db: Session = Depends(get_db)):
    results = ResultCrud.get_all(db, userId)
    
    return results


@result_router.get('/{userId}')
async def get_result(userId: int, lesson_id: int, db: Session = Depends(get_db)):
    result = ResultCrud.get(db, userId, lesson_id)
    
    if result is None:
        raise exceptions.SUBJECT_NOT_FOUNT_ERROR
    
    return result


