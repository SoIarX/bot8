from aiogram import Bot, types, asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from Config import TOKEN
import Config as cfg

bot = Bot(token=TOKEN)


async def check_sub_channels(channels, user_id):
  for channel in channels:
    chat_memeber = await bot.get_chat_member(chat_id=channel[0], user_id=user_id)
    if chat_memeber['status'] == 'left':
        return False
  return True