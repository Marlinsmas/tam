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
            await UsersBoolean.create(user_id=user_id)
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
async def start_branch(ans: Message, response=None, payload=None):
    # flagg = False
    if ans.text.lower() == "я готов!" or ans.payload == '1':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("🐕 Собака", VkKeyboardColor.POSITIVE)
        keyboard.add_button("🐈 Кошка", VkKeyboardColor.POSITIVE)
        keyboard = keyboard.get_keyboard()
        await ans("Выбери свое бойца", keyboard=keyboard)

    elif ans.text == "🐕 Собака":
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("Беру!", VkKeyboardColor.POSITIVE, payload=11)
        keyboard.add_line()
        keyboard.add_button("Я еще подумаю...", VkKeyboardColor.NEGATIVE, payload=1)
        keyboard = keyboard.get_keyboard()
        await ans("Это собка очень крутая", keyboard=keyboard)


    elif ans.text == "🐈 Кошка":
        keyboard = VkKeyboard(one_time=True)
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
        b = await UsersBoolean.get(user_id=ans.peer_id)
        b.train_flag = True
        await b.save()


        # await start_branch(ans, payload=21)

    elif ans.payload == '12':
        u = await Users.get(user_id=ans.peer_id)
        u.enimal = "кошка"
        await u.save()
        await ans("Как будут звать ващего питомца?")
        b = await UsersBoolean.get(user_id=ans.peer_id)
        b.train_flag = True
        await b.save()

        # await start_branch(ans, payload=21)

    elif ans.payload == '13':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("🍖 Покормить", VkKeyboardColor.DEFAULT, payload=13)
        keyboard.add_button("❤ Вылечить", VkKeyboardColor.DEFAULT, payload=13)
        keyboard.add_button("⚽ Поиграть", VkKeyboardColor.DEFAULT, payload=13)
        keyboard.add_line()
        keyboard.add_button("🏪 Магазин", VkKeyboardColor.POSITIVE, payload=14)
        keyboard.add_button("🏥 Больница", VkKeyboardColor.DEFAULT, payload=13)
        keyboard.add_line()
        keyboard.add_button("👥 Клубы", VkKeyboardColor.DEFAULT, payload=13)
        keyboard.add_button("📢 Рассылка", VkKeyboardColor.DEFAULT, payload=13)
        keyboard.add_button("📊 Статиска", VkKeyboardColor.DEFAULT, payload=13)
        keyboard = keyboard.get_keyboard()
        await ans(
            "➡ Настало время научить тебя обращаться со своим питомцем. Сейчас он сильно голоден 😓! Мы же не хотим чтобы он умер?\n "
            "Но для начало нужно нужно купить немного еды 🍖.\n Зайди в 🏪 Магазин", keyboard=keyboard)
        b = await UsersBoolean.get(user_id=ans.peer_id)
        b.train_flag = False
        await b.save()

    elif ans.payload == '14':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("🥛 Молоко +5🍖 -💸", VkKeyboardColor.DEFAULT, payload=14)
        keyboard.add_line()
        keyboard.add_button("🥕 Морковь +10🍖 -💸", VkKeyboardColor.DEFAULT, payload=14)
        keyboard.add_line()
        keyboard.add_button("🍞 Хлеб +15🍖 -💸", VkKeyboardColor.DEFAULT, payload=14)
        keyboard.add_line()
        keyboard.add_button("🍳 Яичница +20🍖 -💸", VkKeyboardColor.DEFAULT, payload=14)
        keyboard.add_line()
        keyboard.add_button("🎂 Торт +25🍖 -💸", VkKeyboardColor.DEFAULT, payload=14)
        keyboard.add_line()
        keyboard.add_button("🍚 Рис +30🍖 -💸", VkKeyboardColor.DEFAULT, payload=14)
        keyboard.add_line()
        keyboard.add_button("🍕 Пицца +35🍖 -💸", VkKeyboardColor.DEFAULT, payload=14)
        keyboard.add_line()
        keyboard.add_button("🍗 Куриная ножка +40🍖 -💸", VkKeyboardColor.POSITIVE, payload=15)
        keyboard.add_line()
        keyboard.add_button("🥩 Мясо +45🍖 -💸", VkKeyboardColor.DEFAULT, payload=14)
        keyboard.add_line()
        keyboard.add_button("🔙 Назад", VkKeyboardColor.DEFAULT, payload=14)
        keyboard = keyboard.get_keyboard()
        await ans("➡ Еда различается по цене и сытости. Давай купим 🍗 Куриную ножку. \n "
                  "40🍖 - показывает сытость продукта еды, а 100💸 - показывает цену продукта", keyboard=keyboard)

    elif ans.payload == '15':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("🥛 Молоко - 0", VkKeyboardColor.DEFAULT, payload=15)
        keyboard.add_line()
        keyboard.add_button("🥕 Морковь - 0", VkKeyboardColor.DEFAULT, payload=15)
        keyboard.add_line()
        keyboard.add_button("🍞 Хлеб - 0", VkKeyboardColor.DEFAULT, payload=15)
        keyboard.add_line()
        keyboard.add_button("🍳 Яичница - 0", VkKeyboardColor.DEFAULT, payload=15)
        keyboard.add_line()
        keyboard.add_button("🎂 Торт - 0", VkKeyboardColor.DEFAULT, payload=15)
        keyboard.add_line()
        keyboard.add_button("🍚 Рис - 0", VkKeyboardColor.DEFAULT, payload=15)
        keyboard.add_line()
        keyboard.add_button("🍕 Пицца - 0", VkKeyboardColor.DEFAULT, payload=15)
        keyboard.add_line()
        keyboard.add_button("🍗 Куриная ножка - 1", VkKeyboardColor.POSITIVE, payload=16)
        keyboard.add_line()
        keyboard.add_button("🥩 Мясо - 0", VkKeyboardColor.DEFAULT, payload=15)
        keyboard.add_line()
        keyboard.add_button("🔙 Назад", VkKeyboardColor.DEFAULT, payload=15)
        keyboard = keyboard.get_keyboard()
        await ans("➡ Здесь ты можешь контролировать рацион своего питомца\n"
                  "Покорми его 🍖!", keyboard=keyboard)

    elif ans.payload == '16':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("🍖 Покормить", VkKeyboardColor.DEFAULT, payload=16)
        keyboard.add_button("❤ Вылечить", VkKeyboardColor.DEFAULT, payload=16)
        keyboard.add_button("⚽ Поиграть", VkKeyboardColor.DEFAULT, payload=16)
        keyboard.add_line()
        keyboard.add_button("🏪 Магазин", VkKeyboardColor.DEFAULT, payload=16)
        keyboard.add_button("🏥 Больница", VkKeyboardColor.POSITIVE, payload=17)
        keyboard.add_line()
        keyboard.add_button("👥 Клубы", VkKeyboardColor.DEFAULT, payload=16)
        keyboard.add_button("📢 Рассылка", VkKeyboardColor.DEFAULT, payload=16)
        keyboard.add_button("📊 Статиска", VkKeyboardColor.DEFAULT, payload=16)
        keyboard = keyboard.get_keyboard()
        await ans("➡ Есть хорошая и плохая новость.\n"
                  "✅ Хорошая - твой питомец больше не голоден ☺! \n"
                  "❌ Плохая - он плохо себя чувствует 😟 \n"
                  "Такое происходит, когда долго не кормишь своего питомца. \n"
                  "Ему срочно нужно в 🏥 Больницу!", keyboard=keyboard)

    elif ans.payload == '17':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("💊 Таблетка +10❤ -💸", VkKeyboardColor.DEFAULT, payload=17)
        keyboard.add_line()
        keyboard.add_button("💉 Шприц +40❤ -💸", VkKeyboardColor.POSITIVE, payload=18)
        keyboard.add_line()
        keyboard.add_button("🔙 Назад", VkKeyboardColor.DEFAULT, payload=17)
        keyboard = keyboard.get_keyboard()
        await ans("➡ Давай подлатаем товего мальца!\n"
                  "Купи 💉 Шприц, он полностью восстановит здоровье твоего питомца.", keyboard=keyboard)

    elif ans.payload == '18':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("🍖 Покормить", VkKeyboardColor.DEFAULT, payload=18)
        keyboard.add_button("❤ Вылечить", VkKeyboardColor.POSITIVE, payload=19)
        keyboard.add_button("⚽ Поиграть", VkKeyboardColor.DEFAULT, payload=18)
        keyboard.add_line()
        keyboard.add_button("🏪 Магазин", VkKeyboardColor.DEFAULT, payload=18)
        keyboard.add_button("🏥 Больница", VkKeyboardColor.DEFAULT, payload=18)
        keyboard.add_line()
        keyboard.add_button("👥 Клубы", VkKeyboardColor.DEFAULT, payload=18)
        keyboard.add_button("📢 Рассылка", VkKeyboardColor.DEFAULT, payload=18)
        keyboard.add_button("📊 Статиска", VkKeyboardColor.DEFAULT, payload=18)
        keyboard = keyboard.get_keyboard()
        await ans("➡ Лечить питомца придётся самому.", keyboard=keyboard)

    elif ans.payload == '19':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("💊 Таблетка 0", VkKeyboardColor.DEFAULT, payload=19)
        keyboard.add_line()
        keyboard.add_button("💉 Шприц 1", VkKeyboardColor.POSITIVE, payload=20)
        keyboard.add_line()
        keyboard.add_button("🔙 Назад", VkKeyboardColor.DEFAULT, payload=19)
        keyboard = keyboard.get_keyboard()
        await ans("➡ Здесь находится твоя импровизированная аптечка \n"
                  "Давай подлатаем твоего пета ❤", keyboard=keyboard)

    elif ans.payload == '20':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Завершить обучение", VkKeyboardColor.POSITIVE, payload=100)
        keyboard = keyboard.get_keyboard()
        await ans("➡ Вот и все! Твое обучение завершено, заботься о своем питомце и не обижай его", keyboard=keyboard)
        u = await Users.get(user_id=ans.peer_id)
        u.train = True
        await u.save()
        await bot.branch.exit(ans.peer_id)

    else:
        b = await UsersBoolean.get(user_id=ans.peer_id)
        if b.train_flag:
            print(1)
            name = ans.text
            u = await Users.get(user_id=ans.peer_id)
            u.nickname = name
            await u.save()
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button("Продолжить", VkKeyboardColor.POSITIVE, payload=13)
            keyboard = keyboard.get_keyboard()
            await ans(f"{name} прекрасное имя!", keyboard=keyboard)


        # await menu(ans)
        # await bot.branch.exit(ans.peer_id)






@bot.on.message(text="1", lower=True)
async def menu(ans: Message):
    pass



@bot.on.message(PayloadRule(100))
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