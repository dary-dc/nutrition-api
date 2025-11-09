from fastapi.responses import JSONResponse
from fastapi import FastAPI

def register_exception_handler(app: FastAPI):
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        import traceback
        tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        return JSONResponse({"error": str(exc), "traceback": tb}, status_code=500)