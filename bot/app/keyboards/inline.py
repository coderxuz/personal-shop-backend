from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from bot.app.services.translations.translations import get_translations


async def start_inline_keyboard(lang: str) -> InlineKeyboardMarkup:
    login_txt= await get_translations(lang=lang, key="login")
    sign_up_txt = await get_translations(lang=lang, key="sign_up")
    change_lang_txt = await get_translations(lang=lang, key="change_lang")
    help_txt = await get_translations(lang=lang, key="help")

    login = InlineKeyboardButton(text=login_txt, callback_data="login")
    sign_up = InlineKeyboardButton(text=sign_up_txt, callback_data="sign_up")
    change_lang = InlineKeyboardButton(
        text=change_lang_txt, callback_data="change_lang"
    )
    help = InlineKeyboardButton(text=help_txt, callback_data="help")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[login,sign_up ], [change_lang],[help]]
    )

    return keyboard
