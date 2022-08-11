from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# local imports
from app import models, schemas, utils, database, oAuth2

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.TokenResponse)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: database.SessionLocal = Depends(database.get_db)):
    user = db.query(models.Users).filter(
        models.Users.email == credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Sorry no user found with provided email: {credentials.username}")

    if not utils.verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Sorry no user found")

    access_token = oAuth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.UsersResponse)
async def create_user(new_user: schemas.NewUser, db: Session = Depends(database.get_db)):
    secure_password = utils.hash_password(new_user.password)
    new_user.password = secure_password

    # ORM query (SqlAlchemy)
    created_user = models.Users(**new_user.dict())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user
