from aiogram import Bot, Dispatcher, executor
import os
import dotenv

dotenv.load_dotenv('.env')

bot = Bot(token=os.environ['api_key'])
dispatcher = Dispatcher(bot=bot)

waiting_rooms = set()
chat_rooms = {}

@dispatcher.message_handler(commands=['join'])
async def join_room(message):
    my_user = message.from_user.id

    try:
        if my_user in waiting_rooms:
            await bot.send_message(chat_id=my_user, text="Вы в комнате ожидания, пожалуйста подождите пока мы ищем вам собеседника")
        else:
            another_user = waiting_rooms.pop()
            chat_rooms[another_user] = my_user
            chat_rooms[my_user] = another_user

            await bot.send_message(chat_id=my_user, text="Собеседник найден, общайтесь! Чтобы покинуть чат напишите /leave.")
            await bot.send_message(chat_id=another_user, text="Собеседник найден, общайтесь! Чтобы покинуть чат напишите /leave")

    except KeyError:
        if chat_rooms.get(my_user) is None:
            waiting_rooms.add(my_user)
            await bot.send_message(chat_id=my_user, text="Вы в комнате ожидания")
        else:
            await bot.send_message(chat_id=my_user, text="Вы уже находитесь в чате")

@dispatcher.message_handler(commands=['leave'])
async def leave_room(message):
    my_user = message.from_user.id
    try:
        if my_user in waiting_rooms:
            waiting_rooms.discard(my_user)
            await bot.send_message(chat_id=my_user, text="Вы вышли из очереди")
        another_user = chat_rooms[my_user]
        del chat_rooms[my_user], chat_rooms[another_user]

        await bot.send_message(chat_id=my_user, text="Вы вышли из чата")
        await bot.send_message(chat_id=another_user, text="Ваш собеседник покинул чат")
    except KeyError:
        await bot.send_message(chat_id=my_user, text="Вы не в чате, напишите /join для общения")


@dispatcher.message_handler()
async def seng_message_on_room(message):
    my_user = message.from_user.id
    try:
        await bot.send_message(chat_id=chat_rooms[my_user], text=message.text)
    except:
        if my_user in waiting_rooms:
            await bot.send_message(chat_id=my_user,
                                   text="Вы в комнате ожидания, пожалуйста подождите пока мы ищем вам собеседника")
        else:
            await bot.send_message(chat_id=my_user, text="Вы не в чате, напишите /join для общения")

if __name__ == '__main__':
    executor.start_polling(dispatcher=dispatcher)

