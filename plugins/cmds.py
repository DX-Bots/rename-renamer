#https://github.com/PredatorHackerzZ/RENAMER-BOT


import os
import sqlite3
import logging
import pyrogram
from pyrogram.errors import UserNotParticipant, UserBannedInChannel

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

if bool(os.environ.get("WEBHOOK", False)):

    from sample_config import Config
else:
    from config import Config

from pyrogram import filters
from scripts import Scripted
from pyrogram import Client as Clinton
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, Message



@Clinton.on_message(filters.command(["start"]))
async def start(bot, update):
          await bot.send_message(
          chat_id=update.chat.id,
          text=Scripted.START_TEXT,
          parse_mode="html",
          disable_web_page_preview=True,
          reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton(text='⭕ Cʜᴀɴɴᴇʟ ⭕', url=f'https://t.me/{Config.UPDATE_CHANNEL}'),
                                                 InlineKeyboardButton(text='⭕ Sᴜᴘᴘᴏʀᴛ ⭕', url=f'https://t.me/{Config.UPDATE_GROUP}') ],
                                               [ InlineKeyboardButton(text='👮 DᴇvᴇlopᴇR', url='https://t.me/TheTeleRoid'),
                                                 InlineKeyboardButton(text='🚸 Pᴏweʀᴇd By', url='https://t.me/MoviesFlixers_DL') ],
                                               [ InlineKeyboardButton(text='🔐 Cʟᴏꜱᴇ 🔐', callback_data='DM') ] ] ) )



@Clinton.on_message(filters.command(["help"]))
async def helpme(bot, update):
          await bot.send_message(
          chat_id=update.chat.id,
          text=Scripted.HELP_TEXT,
          parse_mode="html",
          disable_web_page_preview=True,
          reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton(text='🔐 ᴄʟᴏꜱᴇ', callback_data='DM') ] ] ) )



@Clinton.on_message(filters.command(["about"]))
async def abot(bot, update):
          await bot.send_message(
          chat_id=update.chat.id,
          text=Scripted.ABOUT_TEXT,
          parse_mode="html",
          disable_web_page_preview=True,
          reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton(text='ᴄʟᴏꜱᴇ 🔐', callback_data='DM') ] ] ) )



@Clinton.on_message(filters.command(["upgrade"]))
async def upgra(bot, update):
          await bot.send_message(
          chat_id=update.chat.id,
          text=Scripted.UPGRADE_TEXT,
          parse_mode="html",
          disable_web_page_preview=True,
          reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton(text='🔐 ᴄʟᴏꜱᴇ', callback_data='DM') ] ] ) )

@Clinton.on_callback_query()
async def button(bot, update):
    if update.data == "rename":
     await update.message.delete(True)
     await bot.send_message(
         chat_id=update.message.chat.id,
         text="now send me a new name for the file",
         reply_to_message_id=updete.message.reply_to_message.message_id,
         reply_markup=ForceReply(False)
    )
