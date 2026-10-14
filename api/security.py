import hashlib
import hmac
import os
import secrets
import time
from fastapi import HTTPException

_local_secret = secrets.token_hex(32)

def auth_throttle(database, request, email):
    now = time.time()
    window = int(now // 900)
    secret = os.getenv('RESTRICTAPP_RATE_SECRET', _local_secret).encode()
    client_ip = request.client.host if request.client else 'unknown'
    # Forwarded headers are handled only by the trusted Uvicorn proxy configuration.
    limits = [(f'ip:{client_ip}',60),(f'email:{email}',10)]
    blocked = False
    with database() as db:
        db.execute('DELETE FROM auth_attempts WHERE expires<=?', (now,))
        for identity, limit in limits:
            digest = hmac.new(secret,identity.encode(),hashlib.sha256).hexdigest()
            bucket = f'{window}:{digest}'
            row = db.execute('INSERT INTO auth_attempts(bucket,attempts,expires) VALUES (?,1,?) ON CONFLICT(bucket) DO UPDATE SET attempts=auth_attempts.attempts+1 RETURNING attempts', (bucket,(window+1)*900)).fetchone()
            blocked = blocked or row['attempts'] > limit
    # Raise after committing the counters so failed attempts cannot roll them back.
    if blocked:
        raise HTTPException(429,'Too many sign-in attempts. Please try again later.',headers={'Retry-After':str(max(1,int((window+1)*900-now)))})
