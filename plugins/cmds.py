#https://github.com/PredatorHackerzZ/RENAMER-BOT


import os
import asyncio
import sqlite3
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import time
import logging
import pyrogram
from pyrogram.errors import UserNotParticipant, UserBannedInChannel
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

if bool(os.environ.get("WEBHOOK", False)):

    from sample_config import Config
else:
    from config import Config

from PIL import Image
from database.database import *
from pyrogram import filters
from scripts import Scripted
from pyrogram import Client as Clinton
from functions.display_progress import progress_for_pyrogram
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, Message



@Clinton.on_message(filters.private & filters.reply & filters.text)
async def rep_rename_call(c, m):
  bot_msg = await c.get_messages(m.chat.id, m.reply_to_message.message_id) 
  todown = bot_msg.reply_to_message # msg with media
  new_f_name = m.text # new name
  media = todown.document or todown.video or todown.audio or todown.voice or todown.video_note or todown.animation
  try:
    media_name = media.file_name
    extension = media_name.split(".")[-1]
  except:
    extension = "mkv"
  await bot_msg.delete() # delete name asked msg 
  if len(new_f_name) > 64:
      await m.reply_text(text=f"Lɪᴍɪᴛs Oꜰ Tᴇʟᴇɢʀᴀᴍ Fɪʟᴇ Nᴀᴍᴇ Is 64 Cʜᴀʀᴇᴄᴛᴇʀs Oɴʟʏ")
      return
  d_msg = await m.reply_text(Scripted.TRYING_TO_DOWNLOAD, True)
  d_location = Config.DOWNLOAD_LOCATION + "/"
  d_time = time.time()
  downloaded_file = await c.download_media(
    message=todown,
    file_name=d_location,
    progress=progress_for_pyrogram,
    progress_args=(Scripted.DOWNLOAD_START, d_msg, d_time) )
  
  if downloaded_file is not None:
    try:
       df = await d_msg.edit(
                text=Scripted.TRYING_TO_UPLOAD
           )
    except:
        pass
  new_file_name = d_location + new_f_name + "." + extension
  os.rename(downloaded_file,new_file_name)
  logger.info(downloaded_file)
  thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(m.from_user.id) + ".jpg"
  await c.send_message(
      Config.DB_CHANNEL,
      f"""<b>Bᴏᴛ ɴᴀᴍᴇ :</b> [Rᴇɴᴀᴍᴇʀ Bᴏᴛ](https://t.me/AIOM_RENAMER_PRO_BOT)

<b>Uꜱᴇʀ ɴᴀᴍᴇ :  [{m.from_user.first_name}](tg://user?id={m.from_user.id})</b>

<b>Uꜱᴇʀ ɪᴅ :</b>  `{m.from_user.id}`

<b>Tᴀꜱᴋ : #Rᴇɴᴀᴍɪɴɢ</b>

<b>Tᴇxᴛ :</b> `{new_f_name}`""",
      disable_web_page_preview=True
  )
  if not os.path.exists(thumb_image_path):
                mes = await sthumb(m.from_user.id)
                if mes != None:
                    h = await c.get_messages(m.chat.id, mes.msg_id)
                    await h.download(file_name=thumb_image_path)
                    thumb_image_path = thumb_image_path
                else:
                    thumb_image_path = None

  else:
       width = 0
       height = 0
       metadata = extractMetadata(createParser(thumb_image_path))
       if metadata.has("width"):
           width = metadata.get("width")
       if metadata.has("height"):
           height = metadata.get("height")
       Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
       img = Image.open(thumb_image_path)
       img.resize((320, height))
       img.save(thumb_image_path, "JPEG")
       c_time = time.time()
       await c.send_document(
       chat_id=m.chat.id,
       document=new_file_name,
       thumb=thumb_image_path,
       reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton(text='Aɪ๏ᴍ Bᴏᴛs', url="https://t.me/AIOM_Bots")]]),
       reply_to_message_id=m.reply_to_message.message_id,
       progress=progress_for_pyrogram,
       progress_args=(Scripted.UPLOAD_START, df, c_time))
  try:
      await df.delete()
      os.remove(d_location)
      os.remove(thumb_image_path)
  except:
      pass
  await c.send_message(
      text=Scripted.UPLOAD_SUCCESS,
      chat_id=m.chat.id
  )

@Clinton.on_message(filters.command(["start"]))
async def start(bot, update):
          await bot.send_message(
          chat_id=update.chat.id,
          text=Scripted.START_TEXT.format(update.from_user.mention),
          parse_mode="html",
          disable_web_page_preview=True,
          reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton(text='Hᴇʟᴩ', callback_data='help'), InlineKeyboardButton(text='Aʙᴏᴜᴛ', callback_data='about') ],[ InlineKeyboardButton(text='Cʟᴏꜱᴇ', callback_data='close') ] ] ) )
          await bot.send_message(
          Config.DB_CHANNEL,
          f"""<b>Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ: 

Mʏ Nᴇᴡ Fʀɪᴇɴᴅ [{update.from_user.first_name}](tg://user?id={update.from_user.id}) Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !</b>""",
          disable_web_page_preview=True
          )



@Clinton.on_message(filters.command(["helvp"]))
async def helpme(bot, update):
          df = await bot.reply_text("Processing.")
          await df.edit("Processing..")
          await df.edit("Processing...")
          await df.edit(
          chat_id=update.chat.id,
          text=Scripted.HELP_TEXT,
          parse_mode="html",
          disable_web_page_preview=True,
          reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton(text='🔐 ᴄʟᴏꜱᴇ', callback_data='DM') ] ] ) )
         
@Clinton.on_message(filters.command(["aboufft"]))
async def abot(bot, update):
          await bot.send_message(
          chat_id=update.chat.id,
          text=Scripted.ABOUT_TEXT,
          parse_mode="html",
          disable_web_page_preview=True,
          reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton(text='ᴄʟᴏꜱᴇ 🔐', callback_data='DM') ] ] ) )



@Clinton.on_message(filters.command(["upgradef"]))
async def upgra(bot, update):
          await bot.send_message(
          chat_id=update.chat.id,
          text=Scripted.UPGRADE_TEXT,
          parse_mode="html",
          disable_web_page_preview=True,
          reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton(text='🔐 ᴄʟᴏꜱᴇ', callback_data='DM') ] ] ) )

@Clinton.on_callback_query()
async def button(c, m):
    if m.data == "rename":
     await m.message.delete(True)
     await c.send_message(
         chat_id=m.message.chat.id,
         text="✎ Nᴏᴡ Sᴇɴᴅ Mᴇ A Nᴇᴡ Fɪʟᴇ Nᴀᴍᴇ",
         reply_to_message_id=m.message.reply_to_message.message_id,
         reply_markup=ForceReply(False)
    )

    elif m.data == "convert":
       await m.message.edit("Coming Soon")

    elif m.data == "about":
       await m.message.edit(Scripted.ABOUT_TEXT,
                            parse_mode="html",
                            disable_web_page_preview=True,
                            reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton(text='« Bᴀᴄᴋ', callback_data='home') ] ] ) )

    elif m.data == "help":
       await m.message.edit(Scripted.HELP_TEXT,
                            parse_mode="html",
                            disable_web_page_preview=True,
                            reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton(text='« Bᴀᴄᴋ', callback_data='home') ] ] ) )

    elif m.data == "home":
       await m.message.edit(Scripted.START_TEXT.format(m.from_user.mention),
                            parse_mode="html",
                            disable_web_page_preview=True,
                            reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton(text='Hᴇʟᴩ', callback_data='help'), InlineKeyboardButton(text='Aʙᴏᴜᴛ', callback_data='about') ],[ InlineKeyboardButton(text='Cʟᴏꜱᴇ', callback_data='close') ] ] ) )

    elif m.data == "close":
       await m.message.delete()



                                                              
