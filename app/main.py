from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from app.DBmodels import *
import uvicorn
from dataclasses import dataclass
from uuid import uuid4
import io
from pydub import AudioSegment
import base64
import binascii
from sqlalchemy.exc import SQLAlchemyError


app = FastAPI()
NAME_IS_EXIST = 666
host = 'localhost'
port = 8080


@dataclass
class NewUserInput:
    user_name: str


@dataclass
class NewUser:
    id: int
    token: str


@dataclass
class NewRecordsInput:
    user_id: int
    token: str
    file: str


@app.post('/create_user')
def create_user(user_name: NewUserInput):
    if user_name and user_name.user_name:
        new_user = db.query(Users).filter(Users.name == user_name.user_name).first()
        if new_user:
            return JSONResponse(content={}, status_code=NAME_IS_EXIST)
        token = str(uuid4())
        try:
            db.add(Users(UUID=token, name=user_name.user_name))
            db.commit()
        except SQLAlchemyError:
            return JSONResponse(content={}, status_code=500)
        new_user = db.query(Users).filter(Users.name == user_name.user_name).first()
        if new_user:
            return NewUser(id=new_user.id, token=token)
        else:
            return JSONResponse(content={}, status_code=500)
    return JSONResponse(content={}, status_code=400)


@app.post('/add_audio')
def add_audio(file: NewRecordsInput):
    if file and file.file:
        wav_data = file.file
        try:
            b_data = base64.b64decode(wav_data)
        except binascii.Error:
            return PlainTextResponse(content='', status_code=400)
        id = file.user_id
        token = file.token
        try:
            if db.query(Users).filter(Users.id == id, Users.UUID == token).first():
                s = io.BytesIO(b_data)
                x = io.BytesIO()
                AudioSegment.from_wav(s).export(x, format='mp3')
                token_mp3 = str(uuid4())
                audio = Audio(user_id=id, UUID=token_mp3, data=x.read())
                db.add(audio)
                db.commit()
                url_audio = f'http://{host}:{port}/record?id={token_mp3}&user={id}'
                return PlainTextResponse(content=url_audio, status_code=200)
            else:
                return PlainTextResponse(content='', status_code=401)
        except SQLAlchemyError:
            return PlainTextResponse(content='', status_code=500)
    else:
        return PlainTextResponse(content='', status_code=400)


@app.get('/record')
def access_audio(id, user):
    try:
        user = int(user)
        audio = db.query(Audio).filter(Audio.UUID == id, Audio.user_id == user).first()
        if audio:
            mp3_data = audio.data
            return Response(content=mp3_data, media_type='audio/mpeg', status_code=200)
    except:
        return PlainTextResponse(content='', status_code=400)


if __name__ == '__main__':
    db = Session()
    uvicorn.run(app, host='0.0.0.0', port=port)