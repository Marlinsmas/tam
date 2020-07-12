from peewee import *
import peewee
import tortoise
import database_pattern
from peewee_async import Manager
import asyncio
from database_pattern import *
from vk_api.keyboard import VkKeyboardColor, VkKeyboard
from config import *





async def add_user(user_id):
    try:
        u = await Users.get_or_none(user_id=user_id)
        if u is None:
            user_info =await bot.api.users.get(user_ids=user_id, fields='city')
            first_name = user_info[0].first_name
            user_id = int(user_id)
            await Users.create(user_id=user_id, name=first_name, balance=0, donut=0, happiness=10, hunger=10,
                         health=10, energy=10)
        else:
            return True
    except:
        print("проблема в add_user")



async def check_training(user_id):
    u = await Users.get(user_id=user_id)
    if u.train:
        return True
    else:
        return False


@bot.on.message(text=["начать", "начало", "старт"], lower=True)
async def start(ans: Message):
    if await check_training(ans.from_id):
        await ans("Вы уже начали!")
        await menu(ans)
    else:
        await add_user(ans.from_id)
        pass

#1






@bot.on.message(PayloadRule(10))
@bot.on.message(text="меню", lower=True)
async def menu(ans: Message):


    # await loop.run_until_complete(await my_async_func())
    # await loop.close()
    await add_user(ans.from_id)

    u = await Users.get(user_id=ans.from_id)
    print(u.energy)

    if await check_training(ans.from_id):
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("🏦 Город", VkKeyboardColor.DEFAULT)
        keyboard.add_button("🗒 Задания", VkKeyboardColor.DEFAULT)
        keyboard.add_button("🌽 Ресурсы", VkKeyboardColor.DEFAULT)
        keyboard.add_line()
        keyboard.add_button("💰 Баланс", VkKeyboardColor.PRIMARY)
        keyboard.add_button("🎁 Бонус", VkKeyboardColor.PRIMARY)
        keyboard.add_button("📊 Статистика", VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button("📋 Документация", VkKeyboardColor.POSITIVE)
        keyboard.add_button("📢 Рассылка", VkKeyboardColor.POSITIVE)
        keyboard.add_button("💸 Доход", VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("🏗 Строительство", VkKeyboardColor.NEGATIVE)
        keyboard = keyboard.get_keyboard()
        await ans("Меню:", keyboard=keyboard)
    else:
        await ans("Вы еще не начали игру."
                             "\nДля начала напишите \"Начать\"")

































bot.run_polling(skip_updates=True, on_startup=init_db)