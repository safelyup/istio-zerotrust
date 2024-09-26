from fastapi import FastAPI
from pydantic import BaseModel
import python_jwt as jwt
import jwcrypto.jwk as jwk
import datetime
import os
private_key = os.environ['JWT_PRIVATE']
public_key = os.environ['JWT_PUBLIC']

app = FastAPI()

class JWT(BaseModel):
    token: str

class TokenPayLoad(BaseModel):
    username: str

@app.post("/token")
async def gen_token(payload:TokenPayLoad):
    """
    Generate Token: return a JWT token, valid for 1 hour
    """
    if not len(payload.username):
        return "username is required"

    raw_payload = {
        'iss':'demo.local',
        'sub':'example',
        'permission':'all',
        'role': "developer",
        'username': payload.username
    }
    jwt_token = jwt.generate_jwt(
        raw_payload, jwk.JWK.from_json(private_key), 'RS256', datetime.timedelta(hours=1))
    return jwt_token

@app.post("/validate")
async def validate_token(jwt_obj: JWT):
    """
    Validate Token: return message indicating valid/invalid JWT token
    """
    try:
        return jwt.verify_jwt(jwt_obj.token, jwk.JWK.from_json(public_key), ['RS256'])
    except:
        return "Invalid Token"
