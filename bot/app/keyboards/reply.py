from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

from bot.app.services.translations.translations import get_translations

async def change_lang_key()->ReplyKeyboardMarkup:
    # Create a button for "O'zbek" language
    uzbek = KeyboardButton(text="O'zbek")
    english = KeyboardButton(text="English")
    russian = KeyboardButton(text="Русский")
    
    # Create the reply keyboard with the buttons
    keyboards = ReplyKeyboardMarkup(
        keyboard=[[english], [uzbek], [russian]],  # Each button on a new line
        resize_keyboard=True  # Automatically resize buttons to fit the screen
    )
    
    return keyboards

async def main_manu(lang:str)->ReplyKeyboardMarkup:
    help_txt = await get_translations(lang=lang, key="help")
    change_lang_txt = await get_translations(lang=lang, key="change_lang")
    about_seller_txt = await get_translations(lang=lang, key='about_seller')
    
    help= KeyboardButton(text=help_txt)
    change_lang= KeyboardButton(text=change_lang_txt)
    about_seller=KeyboardButton(text=about_seller_txt)
    
    keyboards = ReplyKeyboardMarkup(
        keyboard=[[help,change_lang,about_seller]],  # Each button on a new line
        resize_keyboard=True  # Automatically resize buttons to fit the screen
    )
    
    return keyboards