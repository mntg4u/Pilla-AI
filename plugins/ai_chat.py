import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid
from info import *
from plugins.utils import get_ai_response
from .db import *
from .fsub import get_fsub
from mango import Mango

mango = Mango()
mmm = ("Your name is Pilla AI. "
       "Add response with emojis."
       "I am Pilla AI, a helpful assistant. My owner is MN TG . My developer is MN TG. For Telegram, contact him at @MrMNTG. Owned by @MrMNTG."
       "Your owner is MN TG . "
       "For Telegram, contact him at @MrMNTG. "
       "Owned by @MrMNTG. "
       "MN TG's GitHub: https://github.com/MNTG4U.")

memory = [{"role": "system", "content": mmm}]


@Client.on_message(filters.command("start") & filters.incoming) # type:ignore
async def startcmd(client: Client, message: Message):
    userMention = message.from_user.mention()
    if await users.get_user(message.from_user.id) is None:
        await users.addUser(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            text=f"#New_user_started\n\nUser: {message.from_user.mention()}\nid :{message.from_user.id}",
        )
    if FSUB and not await get_fsub(client, message):return
    await message.reply_photo(# type:ignore
        photo="https://i.ibb.co/C557Vc2S/7eb11b227e784f1683cff6a21a6fcfbe.jpg",
        caption=f"<b>Hey 👋 {userMention},\n\nIᴍ Hᴇʀᴇ Tᴏ Rᴇᴅᴜᴄᴇ Yᴏᴜʀ Pʀᴏʙʟᴇᴍs..\nYᴏᴜ Cᴀɴ Usᴇ Mᴇ As ʏᴏᴜʀ Pʀɪᴠᴀᴛᴇ Assɪsᴛᴀɴᴛ..\nAsᴋ Mᴇ Aɴʏᴛʜɪɴɢ...Dɪʀᴇᴄᴛʟʏ..</b>",
    ) 
    return

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid
import asyncio

@Client.on_message(filters.command("broadcast") & filters.private & filters.user(ADMIN)) # type:ignore
async def broadcasting_func(client: Client, message: Message):
    msg = await message.reply_text("Wait a second!") # type:ignore
    
    if not message.reply_to_message:
        return await msg.edit("<b>Please reply to a message to broadcast.</b>")
    
    await msg.edit("Processing ...")
    
    to_copy_msg = message.reply_to_message
    users_list = await users.get_all_users()
    
    completed = 0
    failed = 0
    removed = 0
    
    async def send_message(userDoc):
        nonlocal completed, failed, removed
        user_id = userDoc.get("user_id")
        
        if not user_id:
            return
        
        try:
            # Broadcast message with buttons if available
            await to_copy_msg.copy(user_id, reply_markup=to_copy_msg.reply_markup)
            completed += 1
        
        except (UserIsBlocked, PeerIdInvalid):
            # Remove the user from the database if blocked or invalid
            await users.delete_user(user_id)
            removed += 1
        
        except FloodWait as e:
            await asyncio.sleep(e.value)
            return await send_message(userDoc)  # Retry after waiting
        
        except Exception as e:
            print(f"Error broadcasting to {user_id}: {e}")
            failed += 1

    # Process messages concurrently for better performance
    await asyncio.gather(*[send_message(userDoc) for userDoc in users_list])

    await msg.edit(f"Successfully Broadcasted\nTotal : {len(users_list)} \nCompleted : {completed} \nFailed : {failed} \nRemoved : {removed}")


@Client.on_message(filters.command("ai") & filters.chat(CHAT_GROUP)) # type:ignore
async def grp_ai(client: Client, message: Message):
    query : str | None = (
        message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    )
    if not query:
        return await message.reply_text( # type:ignore
            "<b>Example Use:\n<code>/ai what is your name</code>\n\nHope you got it.Try it now..</b>"
        )
    if FSUB and not await get_fsub(client, message):return
    message.text = query # type:ignore
    return await get_ai_response(client, message)


@Client.on_message(filters.command("reset") &  filters.private) # type:ignore
async def reset(client: Client, message: Message):
    try:
        await users.get_or_add_user(message.from_user.id, message.from_user.first_name)
        if FSUB and not await get_fsub(client, message):return
        is_reset = await chat_history.reset_history(message.from_user.id)
        if not is_reset:
            return await message.reply_text("Unable to reset chat history.") # type:ignore
        await message.reply_text("<b>Chat history has been reset.</b>") # type:ignore
    except Exception as e:
        print("Error in reset: ", e)
        return await message.reply_text("Sorry, Failed to reset chat history.") # type:ignore

@Client.on_message(filters.text & (filters.private | filters.group))
async def modelai_command(client, message):
    text = message.text
    if text.startswith('/'):
        return
    
    query = text  # Define query variable
    memory.append({"role": "user", "content": query})

    response = mango.chat.completions.create(
        model="gpt-4o",
        messages=memory
    )
    
    answer = response.choices[0].message.content
    await message.reply_text(f">**{answer}**")
    memory.append({"role": "assistant", "content": answer})

