from fastapi import FastAPI
import models
from database import engine
from routers import users, clients


# Crée les tables une seule fois au démarrage
models.Base.metadata.create_all(engine)

app = FastAPI()

# Inclusion des routeurs
app.include_router(users.router)
app.include_router(clients.router)
