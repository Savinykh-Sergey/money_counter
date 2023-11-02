import asyncio
import logging
import uvicorn
from fastapi.staticfiles import StaticFiles
from aiogram import types

from endpoints.users import users_router
from endpoints.photos import photos_router
from endpoints.admins import admin_router
from endpoints.login import login_router
from endpoints.history import history_router

from telegramBot.bot import bot, dp
from telegramBot.config import WEBHOOK_PATH
from telegramBot.requests_to_swaggers import app


app.include_router(users_router)
app.include_router(photos_router)
app.include_router(login_router)
app.include_router(admin_router)
app.include_router(history_router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.on_event("startup")
async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.process_update(telegram_update)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()


if __name__ == '__main__':
    # uvicorn.run(
    #     "main:app",
    #     host="0.0.0.0",
    #     port=10000,
    #     reload=True
    # )
    logging.basicConfig(level=logging.INFO)
    asyncio.run(on_startup())
