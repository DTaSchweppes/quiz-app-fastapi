from sqlalchemy.orm import Session
from models.models import Question
from fastapi import Query
import requests


def get_question_by_id(db: Session, question_id: int):
    '''

    :param db: database ORM sessionmaker sqlalchemy из config
    :param question_id: id вопроса в БД
    :return:
    '''
    response = db.query(Question).filter(Question.id == question_id).first()
    return response


def get_question_by_text(db: Session,
                         text: str):  # В случае, если в БД имеется такой же вопрос, к публичному API с викторинами должны выполняться дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины.
    return db.query(Question).filter(Question.text == text).first()


# def create_question(db: Session, nums: int):
#     nums_check = 0# ??? запросы до тех пор, пока не будет получен уникальный
#     while nums_check < nums:
#         response = request_api(1) # ??? тут тогда можно убрать вообще у request_api (кол-во)
#         for question in response: # ??? тут цикл не убрать, т.к. JSON все равно приходит по запросу
#             _question = Question(text=question['question'], answer=question['answer'])
#             if get_question_by_text(db=db, text=question['question']) is None:
#                 db.add(_question)
#                 db.commit()
#                 db.refresh(_question)
#                 nums_check += 1 # ??? запросы до тех пор, пока не будет получен уникальный

def create_question(db: Session, questions_num: int = Query(None, min_length=1, description="Number of questions")):
    '''

    :param db: database ORM sessionmaker sqlalchemy из config
    :param questions_num: количество вопросов для запроса api и занесения в БД
    :return: последний созданный Question
    '''
    response = request_api(questions_num)
    for question in response:
        _question = Question(text=question['question'], answer=question['answer'])
        if get_question_by_text(db=db, text=question['question']) is not None:
            create_question(db, 1)  # рекурсия
        db.add(_question)
        db.commit()
        db.refresh(_question)
    return _question


def remove_question(db: Session, question_id: int):
    _question = get_question_by_id(db=db, question_id=question_id)
    db.delete(_question)
    db.commit()


def request_api(questions_num: int):
    '''

    :param questions_num: количество вопросов запрашиваемое у api
    :return: json ответ от апи
    '''
    r = requests.get(f'https://jservice.io/api/random?count={questions_num}')
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 404:
        print('Not Found.')
