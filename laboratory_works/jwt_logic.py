from fastapi import HTTPException, Depends, Request
from jose import JWTError, jwt, ExpiredSignatureError
import datetime

class JWTAuth:
    def __init__(self, secret: str, hash_algo: str = "HS256", required_role: str = None):
        self.secret_key = secret
        self.hash_algo = hash_algo
        self.required_role = required_role

    def encode_token(self, profile_id: int) -> str:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            "iat": datetime.datetime.utcnow(),
            "sub": profile_id,
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.hash_algo)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.hash_algo])
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        finally:
            raise HTTPException(status_code=500, detail="Server error - can't decode token")

    def __call__(self, handler):
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if request is None:
                raise HTTPException(400, detail="Invalid Request")

            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Missing or invalid token")

            token_val = auth_header.split(" ")[1]
            token_data = self.decode_token(token_val)
            return await handler(*args, **kwargs)
        return wrapper
