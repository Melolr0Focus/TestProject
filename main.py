import asyncio
import random
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
)
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.filters import Command

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "-1003137717417"

bot = Bot(token=TOKEN)
dp = Dispatcher()

 #Проверка на то что пользыватель админ
async def is_admin(chat_id: int, user_id: int) -> bool:
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]

@dp.message(Command("mute"))
async def mute_handler(message: Message, command: Command):
    chat_id = message.chat.id
    sender_id = message.from_user.id

    # Проверка на то что бот админ
    bot_member = await bot.get_chat_member(chat_id, bot.id)
    if bot_member.status != ChatMemberStatus.ADMINISTRATOR:
        await message.reply("")
        return

    # Проверка на то что отправитель админ
    member = await bot.get_chat_member(chat_id, sender_id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        await message.reply("К сожелению ты админ.")
        return

    # Проверка на ответ
    if not message.reply_to_message:
        await message.reply("Чтобы я замутил человека нужно ответить на его собщение.")
        return

    # аргументы
    args = command.args.split()
    if len(args) < 1:
        await message.reply("Укажи на сколько замутить, или навсегда?")
        return

    time_str = args[0]
    reason = " ".join(args[1:]) if len(args) > 1 else "Не указано"

    # проверка времени
    try:
        unit = time_str[-1]
        value = int(time_str[:-1])
        if unit == "m":
            until_date = datetime.now() + timedelta(minutes=value)
        elif unit == "h":
            until_date = datetime.now() + timedelta(hours=value)
        elif unit == "d":
            until_date = datetime.now() + timedelta(days=value)
        else:
            await message.reply("Чтобы правильно замутить человека нужно после числа написать m, h или d.")
            return
    except:
        await message.reply("Тун тун тун серун")
        return

    # строка отображения
    until_str = until_date.strftime("%A %H:%M %d.%m.%Y")

    target_id = message.reply_to_message.from_user.id
    permissions = ChatPermissions(can_send_messages=False)

    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=target_id,
        permissions=permissions,
        until_date=until_date
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Анмут", callback_data=f"unmute:{target_id}")
    ]])

    await message.reply(
            f"✅ Юзер замучен на {time_str}.\n📄 Причина: {reason}\n До Размута: {until_str}",
            reply_markup=keyboard
        )
    


#анмут
@dp.callback_query(F.data.startswith("unmute:"))
async def unmute_callback(call):
    chat_id = call.message.chat.id
    sender_id = call.from_user.id
#проверка на то что пользыватель админ
    member = await bot.get_chat_member(chat_id, sender_id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        await call.answer("Я не могу сделать это без разрешения админа.", show_alert=True)
        return

    target_id = int(call.data.split(":")[1])

    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_change_info=False,
        can_invite_users=True,
        can_pin_messages=False
    )

    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=target_id,
        permissions=permissions
    )

    await call.message.edit_text("🔓 Пользыватель теперь может говорить🎆🎇.")
    await call.answer("Пользыватель размучен.")

# Команда /secret
@dp.message(Command("secret"))
async def brak_command(message: Message):
    await message.answer("хз не придумал что писать")

# Команда /Аdmins
@dp.message(Command("admins"))
async def admin_list_command(message: Message):
    admin_text = (
        "Власник: @h1caro\n\n"
        "Зами власника:  , \n\n"
        "Админы: @IADERKA8, @Hitman_TymofeiM1, @Focus_TikTok, @wiqerst, @poshe1_nahyi, @mr_matvii \n\n"
    )
    await message.answer(admin_text)

# Команда /sudya
@dp.message(Command("sudya"))
async def judge_command(message: Message):
    user_mention = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ТГ", url="https://t.me/central_UA_RP")],
        [InlineKeyboardButton(text="Зайти на сервер", url="https://www.roblox.com/games/start?placeId=7711635737&launchData=joinCode=c20e90w3")]
    ])
    await message.answer(f", игрок |{user_mention}| вызывает вас в суд, время ожидания 5 минут", reply_markup=keyboard)

# Команда /server
@dp.message(Command("server"))
async def status_command(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ТГ", url="https://t.me/central_UA_RP")],
        [InlineKeyboardButton(text="Зайти на сервер", url="https://www.roblox.com/games/start?placeId=7711635737&launchData=joinCode=c20e90w3")]
    ])
    await message.answer("Код на сервер : c20e90w3", reply_markup=keyboard)

# Команда /адвокат  
@dp.message(Command("unuse"))
async def lawyer_command(message: Message):
    user_mention = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ТГ", url="https://t.me/central_UA_RP")],
        [InlineKeyboardButton(text="Зайти на сервер", url="https://www.roblox.com/games/start?placeId=7711635737&launchData=joinCode=c20e90w3")]
    ])
    await message.answer(f"адвокат , гравець |{user_mention}| викликає вас у суд!", reply_markup=keyboard)

# Команда /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(f"{message.from_user.full_name}, бот працює.")

# Команда /help
@dp.message(Command("help"))
async def help_command(message: Message):
    user_mention = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name
    help_text = (
        f"{user_mention}, привіт! Доступні команди:\n"
        "/sudya - позвати суддю в суд.\n"
        "/не юзается пока-что - викликати адвоката в суд.\n"
        "/start - стан боту.\n"
        "/help - Список команд.\n"
        "/test - випадкова відповідь так/ні.\n"
        "/admins - список администраторов (там не все админы!).\n"
        "/status - стан боту.\n"
        "/mute - замутити користувача (ответить на сообщение).\n"
        "/unmute - розмутити користувача (ответить на сообщение)."
    )
    await message.answer(help_text)

# Команда /Test
@dp.message(Command("test"))
async def test_command(message: Message):
    response = random.choice(["Так", "Ні"])
    await message.answer(response)

# Команда /Chat
@dp.message(Command("Chat"))
async def get_chat_id(message: Message):
    await message.reply(f"chat ID: {message.chat.id}")


#Ручной ввод онлайна сервера + сслыки на запуск
@dp.message(Command("server2"))
async def status_command(message: Message):
        await message.delete()
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Зайти на сервер",
                        url="https://www.roblox.com/games/start?placeId=7711635737&launchData=joinCode%c20e90w3"
                                        ),
                    InlineKeyboardButton(
                    text="Наш ТГ",
                    url="https://t.me/Central_UA_RP"
                    )
                ]
            ])




        args = message.text.split(maxsplit=1)
        onlik = args[1] if len(args) > 1 else "Не указано"
        await message.answer(
            f" Онлайн сервера: {onlik}\n\n"
            f" Код на сервер: c20e90w35\n\n"
            f"чтобы зайти на сервер нажми на кнопку ниже ⬇️",
            reply_markup=keyboard
        )
        
        #пример : 
        #/server2 40 (Снизу указать сообщение команды list)




#Сообщение при запуске
async def on_startup(bot: Bot):
    changelog_text = f"07.10.25 09:48 Govno Entertainme был обновлен✅, запущен в {datetime.now().strftime('%H:%M %d.%m')}. и мы вам представляем Ченжлог:\n\n- мы кароче добавили какую-то хуйню"
    await bot.send_message(CHAT_ID, changelog_text)

# Консольный ввод сообщений
async def console_input_loop():
    while True:
        text = await asyncio.to_thread(input, "Введите сообщение (или 'exit' для выхода): ")
        if text.lower() == "exit":
            print("Выход из режима отправки сообщений.")
            break
        await bot.send_message(CHAT_ID, text)

# Запуск
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup(bot)
    console_task = asyncio.create_task(console_input_loop())
    await dp.start_polling(bot)
    await console_task

if __name__ == "__main__":
    asyncio.run(main())
