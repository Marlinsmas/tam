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

# Кириииил такой дебиииииииил

async def check_training(user_id):
    try:
        u = await Users.get(user_id=user_id)
        if u.train:
            return True
        else:
            return False
    except:
        return False
cvgbfg
fghgfdfghf!!
fghgfg
fggg

@bot.on.message(text=["начать", "начало", "старт"], lower=True)
async def start(ans: Message):
    if await check_training(ans.from_id):
        await ans("Вы уже прошли обучение!")
        await menu(ans)
    else:
        await add_user(ans.from_id)
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Я готов!", VkKeyboardColor.POSITIVE)
        keyboard = keyboard.get_keyboard()
        await ans("Ты готов заботиться о питомцах?", keyboard=keyboard)
        await bot.branch.add(ans.peer_id, "start_branch")


@bot.branch.simple_branch("start_branch")
async def start_branch(ans: Message, response=None):
    if ans.text.lower() == "я готов!" or ans.payload == '1':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("🐕 Собака", VkKeyboardColor.POSITIVE)
        keyboard.add_button("🐈 Кошка", VkKeyboardColor.POSITIVE)
        keyboard = keyboard.get_keyboard()
        await ans("Выбери свое бойца", keyboard=keyboard)

    elif ans.text == "🐕 Собака":
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Беру!", VkKeyboardColor.POSITIVE, payload=11)
        keyboard.add_line()
        keyboard.add_button("Я еще подумаю...", VkKeyboardColor.NEGATIVE, payload=1)
        keyboard = keyboard.get_keyboard()
        await ans("Это собка очень крутая", keyboard=keyboard)


    elif ans.text == "🐈 Кошка":
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Беру!", VkKeyboardColor.POSITIVE, payload=12)
        keyboard.add_line()
        keyboard.add_button("Я еще подумаю...", VkKeyboardColor.NEGATIVE, payload=1)
        keyboard = keyboard.get_keyboard()
        await ans("Это кошка очень крутая", keyboard=keyboard)

    elif ans.payload == '11':
        u = await Users.get(user_id=ans.peer_id)
        u.enimal = "собака"
        await u.save()
        await ans("Как будут звать ващего питомца?")

    elif ans.payload == '12':
        u = await Users.get(user_id=ans.peer_id)
        u.enimal = "кошка"
        await u.save()
        await ans("Как будут звать ващего питомца?")

    else:
        name = ans.text
        u = await Users.get(user_id=ans.peer_id)
        u.nickname = name
        u.train = True
        await u.save()
        await ans(f"{name} прекрасное имя!")
        await menu(ans)
        await bot.branch.exit(ans.peer_id)






@bot.on.message(text="1", lower=True)
async def menu(ans: Message):
    pass



@bot.on.message(PayloadRule(10))
@bot.on.message(text="меню", lower=True)
async def menu(ans: Message):


    # await add_user(ans.from_id)

    # u = await Users.get(user_id=ans.from_id)
    # print(u.energy)

    if await check_training(ans.from_id):
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("🍖 Покормить", VkKeyboardColor.POSITIVE)
        keyboard.add_button("❤️ Вылечить", VkKeyboardColor.POSITIVE)
        keyboard.add_button("⚽ Поиграть", VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("🏪 Магазин", VkKeyboardColor.NEGATIVE)
        keyboard.add_button("🏥 Больница", VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button("👥 Клубы", VkKeyboardColor.PRIMARY)
        keyboard.add_button("📢 Рассылка", VkKeyboardColor.PRIMARY)
        keyboard.add_button("📊 Статиска", VkKeyboardColor.PRIMARY)
        # keyboard.add_line()
        # keyboard.add_button("🏗 Строительство", VkKeyboardColor.NEGATIVE)
        keyboard = keyboard.get_keyboard()
        await ans("Меню:", keyboard=keyboard)
    else:
        await ans("Вы еще не начали игру."
                             "\nДля начала напишите \"Начать\"")



bot.run_polling(skip_updates=True, on_startup=init_db)