from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ContentType, FSInputFile
from aiogram.filters import Command
from aiogram import flags
from aiogram.fsm.context import FSMContext
from telegramBot.utils import *
from telegramBot.states import Gen
from telegramBot.kb import *
from telegramBot.text import *
from telegramBot.db import DBHelper
from telegramBot.requests_to_swaggers import *


db = DBHelper('telegramBot.db')
router = Router()
id = None

@router.message(Command("start"))
async def start_handler(msg: Message):
    await create_user(msg.from_user.id, msg.from_user.full_name, 10)
    global id
    if msg.from_user.id == 856088953:
        db.insert_info_admin(msg.from_user.id, msg.from_user.full_name)
    id = db.insert_info_user(msg.from_user.id, msg.from_user.full_name)
    await msg.answer(f'Привет, {msg.from_user.full_name}, я нейросеть, которая умеет распознавать купюры/деньги на фото') 

@router.message(Command("help"))
async def message_handler(msg: Message):
    await msg.answer('Ты можешь управлять ботом, используя эти команды:\n/start - начать работу с ботом\n/menu - меню с командами для работы с ботом')

@router.message(Command("menu"))
async def message_handler(msg: Message):
    await msg.answer('Выберите пункт меню', reply_markup=menu.as_markup(resize_keyboard=True))

@router.message(Command("admin"))
async def message_handler(msg: Message):
    if msg.from_user.id == 856088953:
        await msg.answer('Выберите пункт меню', reply_markup=menu_admin.as_markup(resize_keyboard=True))
    else:
        await msg.answer('Вы не являетесь администратором')

@router.message(lambda message: message.text == "Загрузить фото")
async def load_photo_callback(message: Message, state: FSMContext):
    await state.set_state(Gen.img_prompt)
    await message.reply(gen_image)

@router.message(lambda message: message.text == "История")
@flags.chat_action("typing")
async def get_history(msg: Message):
    global id
    history = db.get_history_photos(id)
    if history:
        await msg.answer(history)
    else:
        await msg.answer('История запросов пуста\nНажмите загрузить фото :)')

@router.message(lambda message: message.text == "Избранное")
@flags.chat_action("typing")
async def get_favorite(msg: Message):
    global id
    info_favorite = db.get_data_favorite_photos(id)
    await msg.reply(favorite)
    if info_favorite:
        for el in range(len(info_favorite[0])):
            photo_message = await msg.answer_photo(photo=info_favorite[1][el], caption=info_favorite[0][el], reply_markup=del_favorite_photo)
            db.update_message_id(photo_message.message_id, el + 1)
    else:
        await msg.answer('У вас не избранных фото\nДобавьте в избранное :)')

@router.callback_query(F.data == "del_photo")
async def input_image_prompt(callback_query: CallbackQuery):
    db.delete_favorite_photo(callback_query.message.message_id)
    await callback_query.answer(delete_photo)

@router.message(Gen.img_prompt)
@flags.chat_action("upload_photo")
async def detected_image(msg: Message): 
    global id
    id_photo = msg.photo[-1].file_id
    db.insert_photo(id, id_photo)
    mesg = await msg.answer(gen_wait)
    photo_res = photo_processing()
    await mesg.delete()

    db.insert_data_detected_photo(id, photo_res[0], photo_res[1], photo_res[2], id_photo)
    photo_id = db.get_photo_id(id)

    await msg.answer_photo(photo=photo_id.photo_id, caption=f'Кол-во объектов: {photo_res[0]}\nСумма: {photo_res[1]}\n{img_watermark}', reply_markup=evaluation_neural_network)
  
@router.callback_query(F.data == "right")
async def input_image_prompt(msg: Message):
    await msg.answer(good_rating)
  
@router.callback_query(F.data == "wrong")
async def input_image_prompt(callback_query: CallbackQuery):
    photo_id = db.get_id_photo_from_favorite(callback_query.message.message_id)
    db.insert_data_incorrect_detected_photo(photo_id)
    await callback_query.answer(bad_rating)

@router.callback_query(F.data == "add_favorite")
async def add_favorite(callback_query: CallbackQuery):
    global id
    count_object, summa_face_value, photo_id = db.get_data_detected_photos(id)
    db.insert_data_favorite_photo(id, count_object, summa_face_value, photo_id, callback_query.message.message_id)
    await callback_query.answer(add_favorite)

        


