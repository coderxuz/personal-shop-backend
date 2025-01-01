from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.app.services.translations.translations import get_translations
from bot.app.keyboards.inline import start_inline_keyboard


router = Router()

@router.message(CommandStart())
async def start(message:Message, state:FSMContext):
    user_lang = "ru" #type:ignore
    answer = await get_translations(lang=user_lang, key='start')
    keyboard = await start_inline_keyboard(lang=user_lang)
    await message.answer(answer, reply_markup=keyboard)
