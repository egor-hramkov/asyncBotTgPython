from aiogram import Bot, Dispatcher, executor
import os
import dotenv
import databases

dotenv.load_dotenv('.env')

bot = Bot(token=os.environ['api_key'])
dispatcher = Dispatcher(bot=bot)

@dispatcher.message_handler(commands=['join'])
async def join_room(message):
    my_user = message.from_user.id

    if databases.take_waiting(my_user):
        await bot.send_message(chat_id=my_user,
                               text="Вы в комнате ожидания, пожалуйста подождите пока мы ищем вам собеседника")
    elif databases.check_waiting():
        another_user = databases.pop_waiting()[0]
        databases.add_chating(my_user, another_user)
        databases.add_chating(another_user, my_user)

        await bot.send_message(chat_id=my_user,
                               text="Собеседник найден, общайтесь! Чтобы покинуть чат напишите /leave.")

        await bot.send_message(chat_id=another_user,
                               text="Собеседник найден, общайтесь! Чтобы покинуть чат напишите /leave")
    else:
        if databases.take_chat(my_user) is None:
            databases.add_waiting(my_user)
            await bot.send_message(chat_id=my_user, text="Вы в комнате ожидания")
        else:
            await bot.send_message(chat_id=my_user, text="Вы уже находитесь в чате")

@dispatcher.message_handler(commands=['leave'])
async def leave_room(message):
    my_user = message.from_user.id
    if databases.take_waiting(my_user):
        databases.delete_waiting(my_user)
        await bot.send_message(chat_id=my_user, text="Вы вышли из очереди")
    elif databases.take_chat(my_user):
        another_user = databases.take_chat(my_user)[0]
        databases.delete_chat_rooms(my_user)
        databases.delete_chat_rooms(another_user)
        await bot.send_message(chat_id=my_user, text="Вы вышли из чата")
        await bot.send_message(chat_id=another_user, text="Ваш собеседник покинул чат")
    else:
        await bot.send_message(chat_id=my_user, text="Вы не в чате, напишите /join для общения")

@dispatcher.message_handler()
async def seng_message_on_room(message):
    my_user = message.from_user.id
    if databases.take_chat(my_user):
        await bot.send_message(chat_id=databases.take_chat(my_user)[0], text=message.text)
    elif databases.take_waiting(my_user):
        await bot.send_message(chat_id=my_user,
                               text="Вы в комнате ожидания, пожалуйста подождите пока мы ищем вам собеседника")
    else:
        await bot.send_message(chat_id=my_user, text="Вы не в чате, напишите /join для общения")

if __name__ == '__main__':
    executor.start_polling(dispatcher=dispatcher)

