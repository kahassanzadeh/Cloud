from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from src.database.postgres import *
from src.api.rabbitMQ import *
from src.api.S3 import *
import os
from cryptography.fernet import Fernet
import uvicorn
from typing import Annotated, Union
import logging


logging.basicConfig(level=logging.INFO)
key = Fernet.generate_key()
cipher = Fernet(key)
app = FastAPI(title="serv_1")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/up")
async def up():
    return f"Hi"


@app.post("/submit_user/")
async def submit_user(email: Annotated[str, Form()], lastname: Annotated[str, Form()],
                      national_id: Annotated[str, Form()],
                      image1: UploadFile,
                      image2: UploadFile,
                      request: Request):
    query = user_table.insert().values(email=email,
                                       lastname=lastname,
                                       national_id="",
                                       IP="",
                                       image1="",
                                       image2="",
                                       state="checking")
    id = await database.execute(query=query)
    name1 = str(id) + '_1.' + image1.filename.split(".")[-1]
    name2 = str(id) + '_2.' + image2.filename.split(".")[-1]
    client_host = request.client.host
    await update_user_info(id, national_id, client_host, name1, name2)
    upload_file(image1, name1)
    upload_file(image2, name2)

    send(str(id))

    return f'your account submitted with id: {id}'


@app.get("/user_IP/")
async def get_ip(request: Request):
    client_ip = request.client.host
    print(client_ip)


@app.get("/update_fields/")
async def update_user_info(id: int, national_id: str, ip: str, name1: str, name2: str):
    encrypted_national_id = cipher.encrypt(national_id.encode()).decode()
    query = (user_table
             .update()
             .where(id == user_table.c.id)
             .values(national_id=encrypted_national_id,
                     IP=ip,
                     image1=name1,
                     image2=name2)
             )
    await database.execute(query=query)


@app.get("/check_status/")
async def check_status(national_id: str, request: Request):

    user = eng.execute("SELECT id,national_id FROM user_table")
    rows = user.fetchall()

    for i in rows:
        user_id = cipher.decrypt(i[1].encode())
        if user_id == national_id.encode("ascii"):
            user = eng.execute(f"SELECT id,IP,state FROM user_table WHERE id={i[0]}").fetchone()
            break
    if request.client.host != user[1]:
        return f"Access Denied"
    elif user[1] == "accepted":
        return f"Successful Authentication: id = {user.id}"
    elif user[1] == "rejected":
        return f"Unsuccessful Authentication: Please try later"
    elif user[1] == "checking":
        return f"We are working on that. Please wait"
    elif user is None:
        return None


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)
