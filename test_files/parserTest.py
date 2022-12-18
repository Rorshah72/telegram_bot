from aiogram import Bot, Dispatcher, executor, types
from config import tokenBot, url
from bs4 import BeautifulSoup as BS
from users import Users
import requests




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
    if message.is_command() and message.get_command() == "/online":
        for users_online in html.find_all(class_="selectable friend_block_v2 persona in-game"):
            user_data_name = users_online.get("data-search").split(';')
            if user_data_name[1] == " dota 2":
                for item in users:
                    if item.user_check(users_online.get('data-steamid')):
                        await message.answer(f'В доті: {user_data_name[0]}, {item.get_userid()}')
                    else:
                        continue
            print(f'В мережі: {user_data_name[0]} його steamid: {users_online.get("data-steamid")}')

    elif message.is_command() == "/hi":
        await message.answer('hi')


# run long-polling
if __name__ == "__main__":
    users: list = [Users('@Sashkevi4', '76561198065251397'),
                   Users('@l0relin', '76561198858879137'),
                   Users('@l0relin', '76561198064750200'),
                   Users('@BurykM', '76561198182949221'),
                   Users('@BurykM', '76561198822497440'),
                   Users('@BurykM', '76561198285340550'),
                   Users('@BurykM', '76561198310652935'),
                   Users('@BurykM', '76561198312191263'),
                   Users('Міша Гіщак', '76561198087121251'),
                   Users('Міша Гіщак', '76561198826397154'),
                   Users('@souIar', '76561198821062514'),
                   Users('@souIar', '76561198088817498'),
                   Users('@MrSwatty', '76561198130828797'),
                   Users('@yuraa_god', '76561198396937234'),
                   Users('Роман Гіщак', '76561198195936319'),
                   Users('Олег', '76561197999742756')]
    executor.start_polling(dp, skip_updates=True)
