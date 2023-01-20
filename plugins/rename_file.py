#https://github.com/PredatorHackerzZ/RENAMER-BOT

import os
import time
import logging
import pyrogram
import math
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

if bool(os.environ.get("WEBHOOK", False)):

    from sample_config import Config
else:
    from config import Config

from PIL import Image
from pyrogram import filters, types
from scripts import Scripted
from database.database import *
from pyrogram import Client as Clinton
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from functions.display_progress import progress_for_pyrogram
from pyrogram.errors import UserNotParticipant, UserBannedInChannel
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton



@Clinton.on_message(filters.command(["rename"]))
async def rename_doc(bot, update):

    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text(Scripted.ACCESS_DENIED)
               return
        except UserNotParticipant:
            await update.reply_text(text=Scripted.JOIN_NOW_TEXT,
                  reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton(text="ᴊᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{Config.UPDATE_CHANNEL}") ]
                ] 
              )
            )
            return
        except Exception:
            await update.reply_text(Scripted.CONTACT_MY_DEVELOPER)
            return

    if (" " in update.text) and (update.reply_to_message is not None):
        cmd, file_name = update.text.split(" ", 1)
        new_file = file_name[:60] + file_name[-4:]
        description = Scripted.CUSTOM_CAPTION.format(file_name)
        download_location = Config.DOWNLOAD_LOCATION + "/"
        c = await bot.send_message(
            chat_id=update.chat.id,
            text=Scripted.TRYING_TO_DOWNLOAD,
            reply_to_message_id=update.message_id
        )
        c_time = time.time()
        the_real_download_location = await bot.download_media(
            message=update.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(Scripted.DOWNLOAD_START, c, c_time) )

        if the_real_download_location is not None:
            try:
                await bot.edit_message_text(
                    text=Scripted.TRYING_TO_UPLOAD,
                    chat_id=update.chat.id,
                    message_id=c.message_id
                )
            except:
                pass
            new_file_name = download_location + file_name
            os.rename(the_real_download_location, new_file_name)
            logger.info(the_real_download_location)
            thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
            if not os.path.exists(thumb_image_path):
                mes = await sthumb(update.from_user.id)
                if mes != None:
                    m = await bot.get_messages(update.chat.id, mes.msg_id)
                    await m.download(file_name=thumb_image_path)
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
            await bot.send_document(
            chat_id=update.chat.id,
            document=new_file_name,
            thumb=thumb_image_path,
            caption=description,
            reply_to_message_id=update.reply_to_message.message_id,
            progress=progress_for_pyrogram,
            progress_args=(Scripted.UPLOAD_START, c, c_time))

            try:
                os.remove(the_real_download_location)
                os.remove(thumb_image_path)
            except:
                pass
            await bot.edit_message_text(
                  text=Scripted.UPLOAD_SUCCESS,
                  chat_id=update.chat.id,
                  message_id=c.message_id
            )

    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Scripted.REPLY_TO_FILE,
            reply_to_message_id=update.message_id)

@Clinton.on_message(filters.document | filters.video | filters.audio | filters.voice | filters.video_note | filters.animation) 
async def on_media_handler(c: Clinton, m: "types.Message"):
    media = m.document or m.video or m.audio or m.voice or m.video_note or m.animation
    file_name = media.file_name
    file_type = media.mime_type
    file_size = humanbytes(media.file_size)
    await c.send_message(  
        chat_id=m.chat.id,
        text=f"""<b>Fɪʟᴇ Nᴀᴍᴇ :</b> `{file_name}`

<b>Fɪʟᴇ Exᴛᴇɴsɪᴏɴ :</b> {file_name.rsplit('.', 1)[-1].upper()}

<b>Fɪʟᴇ Tʏᴘᴇ :</b> {file_type}

<b>Fɪʟᴇ Sɪᴢᴇ :</b> {file_size}""",
        reply_markup=InlineKeyboardMarkup([[
                                          InlineKeyboardButton("↻ Cᴏɴᴠᴇʀᴛ", callback_data="convert"),
                                          InlineKeyboardButton("✎ Rᴇɴᴀᴍᴇ", callback_data="rename")
                                          ],[
                                          InlineKeyboardButton("Cᴀɴᴄᴇʟ", callback_data="close")
                                          ]]
        ),
        disable_web_page_preview=True,
        reply_to_message_id=m.message_id
    )

def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'
