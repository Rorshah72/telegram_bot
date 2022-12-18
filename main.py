import copy
from aiogram import Bot, Dispatcher, executor, types
from config import tokenBot, url, mongo_pass
from pymongo import MongoClient
from bs4 import BeautifulSoup as BS
from users import Users
import requests

users: list
#connect database
cluster = MongoClient(f"mongodb+srv://telegram_bot:{mongo_pass}@cluster0.gcizq3k.mongodb.net/?retryWrites=true&w=majority")
db = cluster["telegram_bot"]
collection = db['data_users_info']

# bot init
bot = Bot(token=tokenBot)
dp = Dispatcher(bot)

# request and parse url
response_html = requests.get(url)
html = BS(response_html.content, 'html.parser')


# echo
@dp.message_handler()
async def echo(message: types.Message):
    # await message.answer(message.text)
    print(message.chat.id)
    if message.is_command() and message.get_command() == "/dota":
        for users_online in html.find_all(class_="selectable friend_block_v2 persona in-game"):
            user_data_name = users_online.get("data-search").split(';')
            if user_data_name[1] == " dota 2":
                for item in users:
                    if item.user_check(users_online.get('data-steamid')):
                        await message.answer(f'В доті: {user_data_name[0]}:, {item.get_userid()}')
                    else:
                        continue
            print(f'В мережі: {user_data_name[0]} його steamid: {users_online.get("data-steamid")}')

    elif message.get_command() == "/quiz":
        print('check 1')
        await message.answer_poll(question='Хтось буде дотку?',
                                  options=['Вже заходжу',
                                           'Буду за 5хв',
                                           'Буду за 15хв',
                                           'Буду пізніше ніж за 15 хв',
                                           'Не буду'],
                                  type='regular',
                                  correct_option_id=1,
                                  is_anonymous=False)



# run long-polling
if __name__ == "__main__":

    results = collection.find({})
    users = []

    for item in results:
        users.append(copy.copy(Users(item.get("telegramid"), item.get("steamid"))))
    cluster.close()


    executor.start_polling(dp, skip_updates=True)
