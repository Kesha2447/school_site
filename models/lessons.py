# -*- coding: utf-8 -*-
'''Creating models for lessons and subjects'''

from typing import Union
from pydantic import BaseModel, Field


#Subject
class SubjectCreate(BaseModel):
    title: str = Field(min_length=2)
    description: str


class Subject(SubjectCreate):
    id: int

    class Config:
        orm_mode = True


#Lesson
class LessonBase(BaseModel):
    title: str = Field(min_length=2)
    description: str


class LessonCreate(LessonBase):
    subject_title: str


class Lesson(LessonBase):
    id: int
    subject: Subject

    class Config:
        orm_mode = True


#Result
class ResultCreate(BaseModel):
    user_id: int
    lesson_id: int    


class Result(ResultCreate):
    homework: Union[str, None] = None
    homework_score: int = Field(le=5, ge=0, default=0)
    progress: float = Field(le=100, ge=0, default=0)    
    
    class Config:
        orm_mode = True


