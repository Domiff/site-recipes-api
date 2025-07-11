import uvicorn
from fastapi import FastAPI

from endpoints.delete_endpoints import router_delete
from endpoints.get_endpoints import router_get
from endpoints.post_enpoints import router_post
from endpoints.put_endpoints import router_put


app = FastAPI()

app.include_router(router_get)
app.include_router(router_post)
app.include_router(router_put)
app.include_router(router_delete)


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
