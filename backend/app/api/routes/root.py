from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
def read_root(request: Request):
    if request.state.is_authenticated:
        return {"message": "Welcome back, authenticated user!"}
    else:
        return {"message": "Hello, please log in to access more features."}
