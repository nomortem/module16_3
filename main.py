from fastapi import FastAPI, Path, HTTPException
from typing import Dict

app = FastAPI()

# Словарь пользователей
users: Dict[str, str] = {'1': 'Имя: Example, возраст: 18'}


@app.get("/users")
async def get_users() -> Dict[str, str]:
    return users


@app.post("/user/{username}/{age}")
async def create_user(username: str, age: int) -> str:
    # Проверяем валидацию имени и возраста
    if len(username) < 5 or len(username) > 20 or age < 18 or age > 120:
        raise HTTPException(status_code=400, detail="Неверные данные для пользователя")

    # Находим максимальный ID и добавляем нового пользователя
    new_user_id = str(max(map(int, users.keys())) + 1)
    users[new_user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {new_user_id} is registered"


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: str = Path(..., description="ID пользователя для обновления"),
        username: str = Path(..., description="Имя пользователя"),
        age: int = Path(..., description="Возраст пользователя")
) -> str:
    # Валидация
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if len(username) < 5 or len(username) > 20 or age < 18 or age > 120:
        raise HTTPException(status_code=400, detail="Неверные данные для пользователя")

    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {user_id} has been updated"


@app.delete("/user/{user_id}")
async def delete_user(user_id: str = Path(..., description="ID пользователя для удаления")) -> str:
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    del users[user_id]
    return f"User {user_id} has been deleted"