from flask import Request

from quizer.model import Question

def validate_ans(question: Question, request: Request) -> bool:
    user_answer = list(request.form.to_dict().keys())[0]
    if user_answer == 'option1':
        if question.option1 == question.answer:
            return True 
    elif user_answer == 'option2':
        if question.option2 == question.answer:
            return True 
    elif user_answer == 'option3':
        if question.option3 == question.answer:
            return True 
    elif user_answer == 'option4':
        if question.option4 == question.answer:
            return True 
    return False  