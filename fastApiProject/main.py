from fastapi import FastAPI

# Создание экземпляра FastAPI приложения
app = FastAPI()


@app.get("/")
async def root():
    """
    Корневой endpoint приложения.

    Returns:
        dict: Словарь с приветственным сообщением
    """
    return {"Hello World!"}