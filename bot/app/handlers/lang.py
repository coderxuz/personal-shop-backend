from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.app.services.translations.translations import (
    get_user_lang_from_callbackQuery,
    get_translations,
)
from bot.app.keyboards.reply import change_lang_key, main_manu
from bot.app.services.redis.redis_db import get_redis, set_user_language_redis

router = Router()


@router.callback_query(lambda c: c.data == "change_lang")  # type: ignore
async def change_lang(callback_query: CallbackQuery, state: FSMContext):

    user_lang = await get_user_lang_from_callbackQuery(callback_query=callback_query)
    choose_lang_txt = await get_translations(user_lang, "change_lang_txt")

    keyboard = await change_lang_key()

    if callback_query.message:
        await callback_query.message.delete()  # type: ignore
        await callback_query.message.answer(choose_lang_txt, reply_markup=keyboard)


@router.message(lambda msg: msg.text in ["English", "O'zbek", "Русский"])  # type: ignore
async def change_lang(message: Message):

    match message.text:
        case "English":
            lang = "en"
        case "O'zbek":
            lang = "uz"
        case "Русский":
            lang = "ru"
        case _:
            lang = "ru"  # default language
    
    redis = await get_redis()
    
    if message.from_user:
        await set_user_language_redis(redis_client=redis, user_id=message.from_user.id, lang_code=lang)
        lang_changed_txt= await  get_translations(lang=lang, key='language_changed')
        main_keys = await main_manu(lang=lang)
        await message.answer(lang_changed_txt, reply_markup=main_keys)
    