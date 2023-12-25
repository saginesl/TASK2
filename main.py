from fastapi import FastAPI, APIRouter, Request, HTTPException
from models.classes import User, Task

# Создаем основной объект FastAPI
app = FastAPI()

users = [
    User(id=1, name="User 1", email="olya@email.ru"),
    User(id=2, name="User 2", email="katya@email.ru"),
]

users_task = [
    Task(id=1, id_user=1, title="работа", content="совещание в 12:00"),
    Task(id=2, id_user=2, title="праздники", content="день рождения дочери")
]

# Создаем объект APIRouter для работы с пользователями
users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# Создаем методы для работы с пользователями

# чтение информации о пользователе по его id
@users_router.get("/{user_id}")
async def read_user(user_id: int):
    user = next((u for u in users if u.id == user_id), None)
    if user:
        return user.dict()
    else:
        return {"message": "User not found"}

# cоздание информации о новом пользователе
@users_router.post("/")
async def create_user(user: User):
    users.append(user)
    return user.dict()

# изменение информации о пользователе
@users_router.put("/{user_id}")
async def update_user(user_id: int, user: User):
    for u in users:
        if u.id == user_id:
            u.name = user.name
            u.email = user.email
            return u.dict()
    raise HTTPException(status_code=404, detail="User not found")

# удаление информации о пользователе по id
@users_router.delete("/{user_id}")
async def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u.id == user_id:
            del users[i]
            return {"message": f"User with id {user_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

# Создаем методы для работы с задачами пользователя

# чтение задачи пользователя
@users_router.get("/{id}/Task")
async def read_user_task(id: int):
    user_task = next((u for u in users_task if u.id == id), None)
    if user_task:
        return user_task.dict()
    else:
        return {"message": "User not found"}

# создание задачи пользователя
@users_router.post("/{id}/Task")
async def create_user_task(id: int, task: Task):
    task.id = id
    users_task.append(task)
    return task.dict()

# изменение задачи пользователя
@users_router.put("/{id}/Task")
async def update_user_task(id: int, task: Task):
    for p in users_task:
        if p.id == id:
            p.id_user = task.id_user
            p.title = task.title
            p.content = task.content
            return p.dict()
    raise HTTPException(status_code=404, detail="User not found")

# удаление задачи пользователя
@users_router.delete("/{id}/Task")
async def delete_user_task(id: int):
    for i, p in enumerate(users_task):
        if p.id == id:
            del users_task[i]
            return {"message": f"Profile for user with id {id} deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

# Подключаем маршруты для работы с пользователями к приложению
app.include_router(users_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)