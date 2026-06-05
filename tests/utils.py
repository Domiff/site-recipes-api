import httpx

from src.auth.schemas import CredentialsSchema


async def authenticate(client: httpx.AsyncClient, credentials: CredentialsSchema):
    response = await client.post("/auth/registration", json=credentials.model_dump())
    session_id = response.cookies.get("session_id")
    if session_id:
        client.cookies["session_id"] = session_id
