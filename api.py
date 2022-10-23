import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from mic_looping import mic_looping
from pydantic import BaseModel

USERNAME = b"tcc_teste"
PASSWORD = b"tcc_vai_dar_certo"

app = FastAPI(
    title="TCC BABYSITTER API",
    docs_url="/"
    )

class Audio_Payload(BaseModel):
    audio_b64: str

security = HTTPBasic()

mic_looping_api = mic_looping()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = USERNAME
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = PASSWORD
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.post("/classificar")
def classificar_audio(payload: Audio_Payload, credentials: HTTPBasicCredentials = Depends(security)):
    mic_looping_api.transform_b64(payload.audio_b64)
    return mic_looping_api.predict()