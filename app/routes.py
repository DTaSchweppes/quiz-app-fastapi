from fastapi import APIRouter
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from models.schemas import Response, RequestQuestion

import orl

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/question/{id}")
def get_question_by_id(id: int, db: Session = Depends(get_db)):
    result = orl.get_question_by_id(db, id)
    if not result:
        return None
    else:
        return Response(status="Ok",
                        code="200",
                        message="Question created successfully",
                        result=result).dict(exclude_none=True)


@router.post("/question/{questions_num}")
async def create_question_service(questions_num: int, db: Session = Depends(get_db)):
    result = orl.create_question(db, questions_num)
    responce_last_qestion = orl.get_question_by_id(db, result.id - questions_num)
    if responce_last_qestion != None:
        return Response(status="Ok",
                        code="200",
                        message="Question created successfully",
                        result=responce_last_qestion).dict(exclude_none=True)
    else:
        return None


@router.delete("/question/{id}")
async def delete_question_service(id: int, db: Session = Depends(get_db)):
    orl.remove_question(db, question_id=id)
    return Response(status="Ok",
                    code="200",
                    message="Question created successfully").dict(exclude_none=True)


@router.post("/create_test/{nums}")
async def create_question_test(request: RequestQuestion, nums: int, db: Session = Depends(get_db)):
    orl.create_question_test(db, nums)
    return Response(status="Ok",
                    code="200",
                    message="Question created successfully").dict(exclude_none=True)
