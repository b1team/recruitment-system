from fastapi import APIRouter, HTTPException
from src.app.schemas.login import LoginRequestBody, LoginResponse
from src.app.api import auth
from src.app.models import User, Employee, Employer
from src.app.db.session import session_scope

router = APIRouter()


user_type_models_mapping = {
    "employee": Employee,
    "employer": Employer
}

user_type_fields_mapping = {
    "employee": "employee_id",
    "employer": "employer_id"
}


@router.post("/login", response_model=LoginResponse)
async def login(user: LoginRequestBody):
    with session_scope() as db:
        db_user = db.query(User).filter(User.email == user.email, User.password == user.password).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="Email or Password is incorrect")
        
        payload = {
            "id": db_user.id,
            "email": db_user.email,
            "name": db_user.name,
            "phone_number": db_user.phone_number,
            "user_type": db_user.user_type
        }
        
        UserTypeModel = user_type_models_mapping.get(db_user.user_type)
        if UserTypeModel:
            user_type = db.query(UserTypeModel.id).filter(UserTypeModel.user_id == db_user.id).first()
            if user_type:
                field_name = user_type_fields_mapping[db_user.user_type]
                payload.update({field_name: user_type.id})
        
        token = auth.create_token(payload)
        response = LoginResponse(**token.dict(), **payload)
        return response
