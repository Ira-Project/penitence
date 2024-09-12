from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .physics.router import router as physics_router

origins = [
    "http://localhost:3000",
    "https://app.iraproject.com",
    "https://converge-dev.vercel.app"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(physics_router)
# app.include_router(math.router)


@app.post("/")
async def root():
    return {"Hello": "World"}


# Use Enum from docs to handle the different questions
# Set up Pydantic model validation for verification JSON
# Read up on the file structure
# Background tasks is also super useful
