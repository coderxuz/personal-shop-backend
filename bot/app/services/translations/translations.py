import aiofiles
from aiogram.types import CallbackQuery

import json
from typing import Dict
import os

from bot.app.services.redis.redis_db import get_redis, get_user_language_redis


async def load_translations() -> Dict[str, str]:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "translations.json")
    async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
        contents = await file.read()
        translations = json.loads(contents)
    return translations


async def get_translations(lang: str, key: str) -> str:
    translations = await load_translations()
    return translations.get(lang, {}).get(  # type:ignore
        key, translations["ru"].get(key)  # type:ignore
    ) 

async def get_user_lang_from_callbackQuery(callback_query:CallbackQuery):
    redis_client = await get_redis()
    user_lang_redis = await get_user_language_redis(
        redis_client=redis_client, user_id=callback_query.from_user.id
    )
    lang_code = callback_query.from_user.language_code
    user_lang = user_lang_redis if user_lang_redis else lang_code
    
    return user_lang
