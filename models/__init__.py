# -*- coding: utf-8 -*-
'''Creating data schemas that we store'''

from typing import List
from .users import User, UserInfo
from .lessons import Lesson, Subject, Result, LessonBase


class UserSchema(User):
    subjects: List[Subject] = []
    result: List[Result] = []


class SubjectSchema(Subject):
    users: List[UserInfo] = []
    lessons: List[LessonBase] = []


class LessonSchema(Lesson):
    results: List[Result]


class ResultSchema(Result):
    pass


__all__ = ['UserSchema', 'SubjectSchema', 'LessonSchema', 'ResultSchema']