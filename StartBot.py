from database_pattern import *
from vk_api.keyboard import VkKeyboardColor, VkKeyboard
from config import *
from ast import literal_eval as le
import pymysql




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
            await GameValues.create(user_id=user_id)
            await GameStat.create(user_id=user_id)
        else:
            return True
    except:
        print("проблема в add_user")


async def check_training(user_id):
    try:
        u = await Users.get(user_id=user_id)
        if u.train:
            return True
        else:
            return False
    except:
        return False


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


    elif ans.payload == '12':
        u = await Users.get(user_id=ans.peer_id)
        u.enimal = "кошка"
        await u.save()
        await ans("Как будут звать ващего питомца?")
        b = await UsersBoolean.get(user_id=ans.peer_id)
        b.train_flag = True
        await b.save()


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
        keyboard.add_button("🍖 Покормить", VkKeyboardColor.POSITIVE, payload=16)
        keyboard.add_button("❤ Вылечить", VkKeyboardColor.DEFAULT, payload=15)
        keyboard.add_button("⚽ Поиграть", VkKeyboardColor.DEFAULT, payload=15)
        keyboard.add_line()
        keyboard.add_button("🏪 Магазин", VkKeyboardColor.DEFAULT, payload=15)
        keyboard.add_button("🏥 Больница", VkKeyboardColor.DEFAULT, payload=15)
        keyboard.add_line()
        keyboard.add_button("👥 Клубы", VkKeyboardColor.DEFAULT, payload=15)
        keyboard.add_button("📢 Рассылка", VkKeyboardColor.DEFAULT, payload=15)
        keyboard.add_button("📊 Статиска", VkKeyboardColor.DEFAULT, payload=15)
        keyboard = keyboard.get_keyboard()
        await ans("➡ Еда куплена, но питомец все ещё голоден.", keyboard=keyboard)
        b = await UsersBoolean.get(user_id=ans.peer_id)
        b.train_flag = False
        await b.save()

    elif ans.payload == '16':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("🍗 Куриная ножка - 1", VkKeyboardColor.POSITIVE, payload=17)
        keyboard.add_line()
        keyboard.add_button("🔙 Назад", VkKeyboardColor.DEFAULT, payload=16)
        keyboard = keyboard.get_keyboard()
        await ans("➡ Здесь ты можешь контролировать рацион своего питомца\n"
                  "Покорми его 🍖!", keyboard=keyboard)

    elif ans.payload == '17':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("🍖 Покормить", VkKeyboardColor.DEFAULT, payload=17)
        keyboard.add_button("❤ Вылечить", VkKeyboardColor.DEFAULT, payload=17)
        keyboard.add_button("⚽ Поиграть", VkKeyboardColor.DEFAULT, payload=17)
        keyboard.add_line()
        keyboard.add_button("🏪 Магазин", VkKeyboardColor.DEFAULT, payload=17)
        keyboard.add_button("🏥 Больница", VkKeyboardColor.POSITIVE, payload=18)
        keyboard.add_line()
        keyboard.add_button("👥 Клубы", VkKeyboardColor.DEFAULT, payload=17)
        keyboard.add_button("📢 Рассылка", VkKeyboardColor.DEFAULT, payload=17)
        keyboard.add_button("📊 Статиска", VkKeyboardColor.DEFAULT, payload=17)
        keyboard = keyboard.get_keyboard()
        await ans("➡ Есть хорошая и плохая новость.\n"
                  "✅ Хорошая - твой питомец больше не голоден ☺! \n"
                  "❌ Плохая - он плохо себя чувствует 😟 \n"
                  "Такое происходит, когда долго не кормишь своего питомца. \n"
                  "Ему срочно нужно в 🏥 Больницу!", keyboard=keyboard)

    elif ans.payload == '18':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("💊 Таблетка +10❤ -💸", VkKeyboardColor.DEFAULT, payload=18)
        keyboard.add_line()
        keyboard.add_button("💉 Шприц +40❤ -💸", VkKeyboardColor.POSITIVE, payload=19)
        keyboard.add_line()
        keyboard.add_button("🔙 Назад", VkKeyboardColor.DEFAULT, payload=18)
        keyboard = keyboard.get_keyboard()
        await ans("➡ Давай подлатаем товего мальца!\n"
                  "Купи 💉 Шприц, он полностью восстановит здоровье твоего питомца.", keyboard=keyboard)

    elif ans.payload == '19':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("🍖 Покормить", VkKeyboardColor.DEFAULT, payload=19)
        keyboard.add_button("❤ Вылечить", VkKeyboardColor.POSITIVE, payload=20)
        keyboard.add_button("⚽ Поиграть", VkKeyboardColor.DEFAULT, payload=19)
        keyboard.add_line()
        keyboard.add_button("🏪 Магазин", VkKeyboardColor.DEFAULT, payload=19)
        keyboard.add_button("🏥 Больница", VkKeyboardColor.DEFAULT, payload=19)
        keyboard.add_line()
        keyboard.add_button("👥 Клубы", VkKeyboardColor.DEFAULT, payload=19)
        keyboard.add_button("📢 Рассылка", VkKeyboardColor.DEFAULT, payload=19)
        keyboard.add_button("📊 Статиска", VkKeyboardColor.DEFAULT, payload=19)
        keyboard = keyboard.get_keyboard()
        await ans("➡ Лечить питомца придётся самому.", keyboard=keyboard)

    elif ans.payload == '20':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("💊 Таблетка 0", VkKeyboardColor.DEFAULT, payload=20)
        keyboard.add_line()
        keyboard.add_button("💉 Шприц 1", VkKeyboardColor.POSITIVE, payload=21)
        keyboard.add_line()
        keyboard.add_button("🔙 Назад", VkKeyboardColor.DEFAULT, payload=20)
        keyboard = keyboard.get_keyboard()
        await ans("➡ Здесь находится твоя импровизированная аптечка \n"
                  "Давай подлатаем твоего пета ❤", keyboard=keyboard)

    elif ans.payload == '21':
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Завершить обучение", VkKeyboardColor.POSITIVE, payload={"button":"меню"})
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





@bot.on.message(text="1", lower=True)
async def menu(ans: Message):
    pass



@bot.on.message(PayloadRule({"button":"меню"}))
@bot.on.message(text="меню", lower=True)
async def menu(ans: Message):

    if await check_training(ans.from_id):
        info = await UsersBoolean.get(user_id=ans.peer_id)

        if not info.check_death:
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button("🍖 Покормить", VkKeyboardColor.POSITIVE, payload={"button":"покормить"})
            keyboard.add_button("❤️ Вылечить", VkKeyboardColor.POSITIVE, payload={"button":"вылечить"})
            keyboard.add_button("⚽ Поиграть", VkKeyboardColor.POSITIVE, payload={"button":"поиграть"})
            keyboard.add_line()
            keyboard.add_button("🏪 Магазин", VkKeyboardColor.NEGATIVE, payload={"button":"магазин"})
            keyboard.add_button("🏥 Больница", VkKeyboardColor.NEGATIVE, payload={"button":"больница"})
            keyboard.add_line()
            keyboard.add_button("👥 Клубы", VkKeyboardColor.PRIMARY, payload={"button":"клубы"})
            keyboard.add_button("📢 Рассылка", VkKeyboardColor.PRIMARY, payload={"button":"рассылка"})
            keyboard.add_button("📊 Статиска", VkKeyboardColor.PRIMARY, payload={"button":"статистика"})
            keyboard = keyboard.get_keyboard()
            await ans("Меню:", keyboard=keyboard, attachment="photo-197028739_457239017")

            if not info.check_one_click:
                print("Первый раз")
                info.check_one_click = 1
                await info.save()
                await checker(ans.peer_id)
        else:
            await ans("Ваш питомец погиб...")
            await death(user_id=ans.peer_id)




    else:
        await ans("Вы еще не начали игру."
                             "\nДля начала напишите \"Начать\"")


@bot.on.message(PayloadRule({"button":"покормить"}))
async def feed(ans: Message):
    u = await GameValues.get(user_id=ans.peer_id)
    keyboard = VkKeyboard(one_time=False)
    if u.milk > 0:
        keyboard.add_button(f"🥛 Молоко +5🍖 - {u.milk}", VkKeyboardColor.DEFAULT, payload={"button":"молоко"})
        keyboard.add_line()
    if u.carrot > 0:
        keyboard.add_button(f"🥕 Морковь +10🍖 - {u.carrot}", VkKeyboardColor.DEFAULT, payload={"button":"морковь"})
        keyboard.add_line()
    if u.bread > 0:
        keyboard.add_button(f"🍞 Хлеб +15🍖 - {u.bread}", VkKeyboardColor.DEFAULT, payload={"button":"хлеб"})
        keyboard.add_line()
    if u.agg > 0:
        keyboard.add_button(f"🍳 Яичница +20🍖 - {u.agg}", VkKeyboardColor.DEFAULT, payload={"button":"яичница"})
        keyboard.add_line()
    if u.cake > 0:
        keyboard.add_button(f"🎂 Торт +25🍖 - {u.cake}", VkKeyboardColor.DEFAULT, payload={"button":"торт"})
        keyboard.add_line()
    if u.rice > 0:
        keyboard.add_button(f"🍚 Рис +30🍖 - {u.rice}", VkKeyboardColor.DEFAULT, payload={"button":"рис"})
        keyboard.add_line()
    if u.pizza > 0:
        keyboard.add_button(f"🍕 Пицца +35🍖 - {u.pizza}", VkKeyboardColor.DEFAULT, payload={"button":"пицца"})
        keyboard.add_line()
    if u.leg > 0:
        keyboard.add_button(f"🍗 Куриная ножка +40🍖 - {u.leg}", VkKeyboardColor.DEFAULT, payload={"button":"ножка"})
        keyboard.add_line()
    if u.meat > 0:
        keyboard.add_button(f"🥩 Мясо +45🍖 - {u.meat}", VkKeyboardColor.DEFAULT, payload={"button":"мясо"})
        keyboard.add_line()



    if u.milk == 0 and u.carrot == 0 and u.bread == 0 and u.cake == 0 and u.rice == 0 and u.pizza == 0 and u.leg == 0 and u.meat == 0:
        print("1")
        keyboard.add_button("🏪 Магазин", VkKeyboardColor.DEFAULT, payload={"button":"магазин"})
        keyboard.add_line()
        keyboard.add_button("🔙 Назад", VkKeyboardColor.POSITIVE, payload={"button": "меню"})
        keyboard = keyboard.get_keyboard()
        await ans("У вас совсем нет еды..\n Отправляйтесь в магазин и прикупите чего-нибудь:", keyboard=keyboard)
    else:
        info = await Users.get(user_id=ans.peer_id)
        keyboard.add_button("🔙 Назад", VkKeyboardColor.POSITIVE, payload={"button": "меню"})
        keyboard = keyboard.get_keyboard()
        await ans(f"Сытость - {info.hunger}/50", keyboard=keyboard)

    if u.milk > 0 or u.carrot > 0 or u.bread > 0 or u.cake > 0 or u.rice > 0 or u.pizza > 0 or u.leg > 0 or u.meat > 0:
        await bot.branch.add(ans.peer_id, "feed_branch")


@bot.branch.simple_branch("feed_branch")
async def feed_branch(ans: Message):
    button = None
    if ans.payload is not None:
        button = le(ans.payload)
        print(button["button"])  # Достаем из payload название кнопки чтобы не делать так: if ans.payload == "{\"button\":\"назад\"}":
        button = button["button"]
    u = await GameValues.get(user_id=ans.peer_id)
    info = await Users.get(user_id=ans.peer_id)
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("🔙 Назад", VkKeyboardColor.POSITIVE, payload={"button": "назад"})
    keyboard = keyboard.get_keyboard()
    if button == "молоко":
        if info.hunger < 50:
            u.milk = u.milk - 1
            info.hunger = info.hunger + 5
            if info.hunger > 50:
                info.hunger = 50

            await u.save()
            await info.save()
            await bot.branch.exit(ans.peer_id)
            await feed(ans)
        else:
            await ans("Ваш питомец уже наелся и спит")
            await bot.branch.exit(ans.peer_id)
            await menu(ans)

    elif button == "морковь":
        if info.hunger < 50:
            u.carrot = u.carrot - 1
            info.hunger = info.hunger + 10
            if info.hunger > 50:
                info.hunger = 50

            await u.save()
            await info.save()
            await bot.branch.exit(ans.peer_id)
            await feed(ans)
        else:
            await ans("Ваш питомец уже наелся и спит")
            await bot.branch.exit(ans.peer_id)
            await menu(ans)

    elif button == "хлеб":
        if info.hunger < 50:
            u.bread = u.bread - 1
            info.hunger = info.hunger + 15
            if info.hunger > 50:
                info.hunger = 50

            await u.save()
            await info.save()
            await bot.branch.exit(ans.peer_id)
            await feed(ans)
        else:
            await ans("Ваш питомец уже наелся и спит")
            await bot.branch.exit(ans.peer_id)
            await menu(ans)

    elif button == "яичница":
        if info.hunger < 50:
            u.agg = u.agg - 1
            info.hunger = info.hunger + 15
            if info.hunger > 50:
                info.hunger = 50

            await u.save()
            await info.save()
            await bot.branch.exit(ans.peer_id)
            await feed(ans)
        else:
            await ans("Ваш питомец уже наелся и спит")
            await bot.branch.exit(ans.peer_id)
            await menu(ans)

    elif button == "торт":
        if info.hunger < 50:
            u.cake = u.cake - 1
            info.hunger = info.hunger + 25
            if info.hunger > 50:
                info.hunger = 50

            await u.save()
            await info.save()
            await bot.branch.exit(ans.peer_id)
            await feed(ans)
        else:
            await ans("Ваш питомец уже наелся и спит")
            await bot.branch.exit(ans.peer_id)
            await menu(ans)

    elif button == "рис":
        if info.hunger < 50:
            u.rice = u.rice - 1
            info.hunger = info.hunger + 30
            if info.hunger > 50:
                info.hunger = 50

            await u.save()
            await info.save()
            await bot.branch.exit(ans.peer_id)
            await feed(ans)
        else:
            await ans("Ваш питомец уже наелся и спит")
            await bot.branch.exit(ans.peer_id)
            await menu(ans)

    elif button == "пицца":
        if info.hunger < 50:
            u.pizza = u.pizza - 1
            info.hunger = info.hunger + 35
            if info.hunger > 50:
                info.hunger = 50

            await u.save()
            await info.save()
            await bot.branch.exit(ans.peer_id)
            await feed(ans)
        else:
            await ans("Ваш питомец уже наелся и спит")
            await bot.branch.exit(ans.peer_id)
            await menu(ans)

    elif button == "ножка":
        if info.hunger < 50:
            u.leg = u.leg - 1
            info.hunger = info.hunger + 40
            if info.hunger > 50:
                info.hunger = 50

            await u.save()
            await info.save()
            await bot.branch.exit(ans.peer_id)
            await feed(ans)

        else:
            await ans("Ваш питомец уже наелся и спит")
            await bot.branch.exit(ans.peer_id)
            await menu(ans)

    elif button == "мясо":
        if info.hunger < 50:
            u.meat = u.meat - 1
            info.hunger = info.hunger + 45
            if info.hunger > 50:
                info.hunger = 50

            await u.save()
            await info.save()
            await bot.branch.exit(ans.peer_id)
            await feed(ans)
        else:
            await ans("Ваш питомец уже наелся и спит")
            await bot.branch.exit(ans.peer_id)
            await menu(ans)


    elif button == "меню":
        await menu(ans)
        await bot.branch.exit(ans.peer_id)

    elif button == "назад":
        await feed(ans)
        await bot.branch.exit(ans.peer_id)

    else:
        await ans("Команда не найдена, попробуйте еще раз или напишите \"Меню\"")




@bot.on.message(PayloadRule({"button":"вылечить"}))
async def heal(ans: Message):
    u = await GameValues.get(user_id=ans.peer_id)
    keyboard = VkKeyboard(one_time=False)
    if u.tablet > 0:
        keyboard.add_button(f"💊 Таблетка +10❤ - {u.tablet}", VkKeyboardColor.DEFAULT, payload={"button": "таблетка"})
        keyboard.add_line()
    if u.injector > 0:
        keyboard.add_button(f"💉 Шприц +40❤ - {u.injector}", VkKeyboardColor.DEFAULT, payload={"button": "шприц"})
        keyboard.add_line()
    if u.tablet == 0 and u.injector == 0:
        keyboard.add_button("🏥 Больница", VkKeyboardColor.DEFAULT, payload={"button": "больница"})
        keyboard.add_line()
        keyboard.add_button("🔙 Назад", VkKeyboardColor.POSITIVE, payload={"button": "меню"})
        keyboard = keyboard.get_keyboard()
        await ans("У вас совсем нет медикаментов..\n Отправляйтесь в больницу и прикупите чего-нибудь:", keyboard=keyboard)
    else:
        info = await Users.get(user_id=ans.peer_id)
        keyboard.add_button("🔙 Назад", VkKeyboardColor.POSITIVE, payload={"button": "меню"})
        keyboard = keyboard.get_keyboard()
        await ans(f"Здоровье {info.health}/50", keyboard=keyboard)
    if u.tablet > 0 or u.injector > 0:
        await bot.branch.add(ans.peer_id, "heal_branch")

@bot.branch.simple_branch("heal_branch")
async def heal_branch(ans: Message):
    button = None
    if ans.payload is not None:
        button = le(ans.payload)
        print(button["button"])  # Достаем из payload название кнопки чтобы не делать так: if ans.payload == "{\"button\":\"назад\"}":
        button = button["button"]
    u = await GameValues.get(user_id=ans.peer_id)
    info = await Users.get(user_id=ans.peer_id)
    if button == "таблетка":
        if info.health < 50:
            u.tablet = u.tablet - 1
            info.health = info.health + 10
            info.statBal = info.statBal + 100
            if info.health > 50:
                info.health = 50

            await u.save()
            await info.save()
            await bot.branch.exit(ans.peer_id)
            await heal(ans)
        else:
            await ans("Ваш питомец уже здоров")
            await bot.branch.exit(ans.peer_id)
            await menu(ans)

    elif button == "шприц":
        if info.health < 50:
            u.injector = u.injector - 1
            info.health = info.health + 40
            info.statBal = info.statBal + 100
            if info.health > 50:
                info.health = 50

            await u.save()
            await info.save()
            await bot.branch.exit(ans.peer_id)
            await heal(ans)
        else:
            await ans("Ваш питомец уже здоров")
            await bot.branch.exit(ans.peer_id)
            await menu(ans)

    elif button == "меню":
        await menu(ans)
        await bot.branch.exit(ans.peer_id)


    else:
        await ans("Команда не найдена, попробуйте еще раз или напишите \"Меню\"")



@bot.on.message(PayloadRule({"button":"магазин"}))
async def shop(ans: Message):
    u = await GameValues.get(user_id=ans.peer_id)
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button(f"🥛 Молоко +5🍖 - {u.milk}", VkKeyboardColor.DEFAULT, payload={"button":"молоко"})
    keyboard.add_line()

    keyboard.add_button(f"🥕 Морковь +10🍖 - {u.carrot}", VkKeyboardColor.DEFAULT, payload={"button":"морковь"})
    keyboard.add_line()

    keyboard.add_button(f"🍞 Хлеб +15🍖 - {u.bread}", VkKeyboardColor.DEFAULT, payload={"button":"хлеб"})
    keyboard.add_line()

    keyboard.add_button(f"🍳 Яичница +20🍖 - {u.agg}", VkKeyboardColor.DEFAULT, payload={"button":"яичница"})
    keyboard.add_line()

    keyboard.add_button(f"🎂 Торт +25🍖 - {u.cake}", VkKeyboardColor.DEFAULT, payload={"button":"торт"})
    keyboard.add_line()

    keyboard.add_button(f"🍚 Рис +30🍖 - {u.rice}", VkKeyboardColor.DEFAULT, payload={"button":"рис"})
    keyboard.add_line()

    keyboard.add_button(f"🍕 Пицца +35🍖 - {u.pizza}", VkKeyboardColor.DEFAULT, payload={"button":"пицца"})
    keyboard.add_line()

    keyboard.add_button(f"🍗 Куриная ножка +40🍖 - {u.leg}", VkKeyboardColor.DEFAULT, payload={"button":"ножка"})
    keyboard.add_line()

    keyboard.add_button(f"🥩 Мясо +45🍖 - {u.meat}", VkKeyboardColor.DEFAULT, payload={"button":"мясо"})
    keyboard.add_line()

    keyboard.add_button("🔙 Назад", VkKeyboardColor.POSITIVE, payload={"button": "меню"})
    keyboard = keyboard.get_keyboard()
    await ans("Доступно:", keyboard=keyboard)
    await bot.branch.add(ans.peer_id, "shop_branch")


@bot.branch.simple_branch("shop_branch")
async def shop_branch(ans: Message):
    button = None
    if ans.payload is not None:
        button = le(ans.payload)
        print(button["button"])  # Достаем из payload название кнопки чтобы не делать так: if ans.payload == "{\"button\":\"назад\"}":
        button = button["button"]
    u = await GameValues.get(user_id=ans.peer_id)
    info = await Users.get(user_id=ans.peer_id)

    if button == "молоко":
        if info.balance >= 100:
            u.milk = u.milk + 1
            info.balance = info.balance - 100
            info.statBal = info.statBal + 100
            await info.save()
            await u.save()

            await ans("Вы успешно купили молоко!")
            await bot.branch.exit(ans.peer_id)
            await shop(ans)
        else:
            await ans("У вас не хватает средств")

    elif button == "морковь":
        if info.balance >= 100:
            u.carrot = u.carrot + 1
            info.balance = info.balance - 100
            info.statBal = info.statBal + 100

            await info.save()
            await u.save()
            await ans("Вы успешно купили морковь!")
            await bot.branch.exit(ans.peer_id)
            await shop(ans)
        else:
            await ans("У вас не хватает средств")

    elif button == "хлеб":
        if info.balance >= 100:
            u.bread = u.bread + 1
            info.balance = info.balance - 100
            info.statBal = info.statBal + 100
            await info.save()
            await u.save()

            await ans("Вы успешно купили хлеб!")
            await bot.branch.exit(ans.peer_id)
            await shop(ans)
        else:
            await ans("У вас не хватает средств")

    elif button == "яичница":
        if info.balance >= 100:
            u.agg = u.agg + 1
            info.balance = info.balance - 100
            info.statBal = info.statBal + 100
            await info.save()
            await u.save()

            await ans("Вы успешно купили яичницу!")
            await bot.branch.exit(ans.peer_id)
            await shop(ans)
        else:
            await ans("У вас не хватает средств")

    elif button == "торт":
        if info.balance >= 100:
            u.cake = u.cake + 1
            info.balance = info.balance - 100
            info.statBal = info.statBal + 100
            await info.save()
            await u.save()

            await ans("Вы успешно купили торт!")
            await bot.branch.exit(ans.peer_id)
            await shop(ans)
        else:
            await ans("У вас не хватает средств")

    elif button == "рис":
        if info.balance >= 100:
            u.rice = u.rice + 1
            info.balance = info.balance - 100
            info.statBal = info.statBal + 100
            await info.save()
            await u.save()

            await ans("Вы успешно купили рис!")
            await bot.branch.exit(ans.peer_id)
            await shop(ans)
        else:
            await ans("У вас не хватает средств")

    elif button == "пицца":
        if info.balance >= 100:
            u.pizza = u.pizza + 1
            info.balance = info.balance - 100
            info.statBal = info.statBal + 100
            await info.save()
            await u.save()

            await ans("Вы успешно купили пиццу!")
            await bot.branch.exit(ans.peer_id)
            await shop(ans)
        else:
            await ans("У вас не хватает средств")

    elif button == "ножка":
        if info.balance >= 100:
            u.leg = u.leg + 1
            info.balance = info.balance - 100
            info.statBal = info.statBal + 100
            await info.save()
            await u.save()

            await ans("Вы успешно купили куриную ножку!")
            await bot.branch.exit(ans.peer_id)
            await shop(ans)
        else:
            await ans("У вас не хватает средств")

    elif button == "мясо":
        if info.balance >= 100:
            u.meat = u.meat + 1
            info.balance = info.balance - 100
            info.statBal = info.statBal + 100
            await info.save()
            await u.save()

            await ans("Вы успешно купили мясо!")
            await bot.branch.exit(ans.peer_id)
            await shop(ans)
        else:
            await ans("У вас не хватает средств")

    elif button == "меню":
        await menu(ans)
        await bot.branch.exit(ans.peer_id)



    else:
        await ans("Команда не найдена, попробуйте еще раз или напишите \"Меню\"")



@bot.on.message(PayloadRule({"button":"больница"}))
async def hospital(ans: Message):
    u = await GameValues.get(user_id=ans.peer_id)
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button(f"💊 Таблетка +10❤  $- {u.tablet}", VkKeyboardColor.DEFAULT, payload={"button": "таблетка"})
    keyboard.add_line()

    keyboard.add_button(f"💉 Шприц +40❤  $- {u.injector}", VkKeyboardColor.DEFAULT, payload={"button": "шприц"})
    keyboard.add_line()

    keyboard.add_button("🔙 Назад", VkKeyboardColor.POSITIVE, payload={"button": "меню"})
    keyboard = keyboard.get_keyboard()
    await ans(f"Доступно:", keyboard=keyboard)
    await bot.branch.add(ans.peer_id, "hospital_branch")



@bot.branch.simple_branch("hospital_branch")
async def hospital_branch(ans: Message):
    button = None
    if ans.payload is not None:
        button = le(ans.payload)
        print(button["button"])  # Достаем из payload название кнопки чтобы не делать так: if ans.payload == "{\"button\":\"назад\"}":
        button = button["button"]
    u = await GameValues.get(user_id=ans.peer_id)
    info = await Users.get(user_id=ans.peer_id)
    if button == "таблетка":
        if info.balance >= 100:
            u.tablet = u.tablet + 1
            info.balance = info.balance - 100
            await info.save()
            await u.save()

            await ans("Вы успешно купили таблетку!")
            await bot.branch.exit(ans.peer_id)
            await hospital(ans)
        else:
            await ans("У вас не хватает средств")

    elif button == "шприц":
        if info.balance >= 100:
            u.injector = u.injector + 1
            info.balance = info.balance - 100
            await info.save()
            await u.save()

            await ans("Вы успешно купили шприц!")
            await bot.branch.exit(ans.peer_id)
            await hospital(ans)
        else:
            await ans("У вас не хватает средств")

    elif button == "меню":
        await menu(ans)
        await bot.branch.exit(ans.peer_id)

    else:
        await ans("Команда не найдена, попробуйте еще раз или напишите \"Меню\"")


async def checker(user_id):
    while True:
        # try:
        min = 6 * 60
        await asyncio.sleep(5)
        u = await Users.get(user_id=user_id)

        if u.hunger - 1 >= 0:
            u.hunger = u.hunger - 1
            await u.save()

        if u.hunger > 10:
            if u.energy + 1 < 50:
                u.energy = u.energy + 1
                await u.save()

        if u.happiness - 1 >= 0:
            u.happiness = u.happiness - 1
            await u.save()

        if u.hunger == 0:
            if u.health - 0.1 >= 0:
                u.health = u.health - 0.1
                await u.save()

        if u.hunger == 10:
            await bot.api.messages.send(peer_id=user_id, message="Ваш питомец голоден", random_id=0)

        if u.health == 20:
            await bot.api.messages.send(peer_id=user_id, message="Ваш питомец дохнет", random_id=0)

        if u.energy == 49:
            await bot.api.messages.send(peer_id=user_id, message="Ваш питомец готов играть", random_id=0)

        if u.happiness == 20:
            await bot.api.messages.send(peer_id=user_id, message="Ваш питомец соскучился", random_id=0)
        # except:
        #     print("Проблема")
        #     continue

        if u.health == 0:
            await bot.api.messages.send(peer_id=user_id, message="Ваш питомец сдох:", random_id=0)
            await death(user_id=user_id)
            break

        print(1)


async def death(user_id=None):
    # if user_id is None:
    #     user_id == ans.peer_id
    #     print(user_id)
    b = await UsersBoolean.get(user_id=user_id)
    b.check_death = 1
    await b.save()
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Воскресить питомца", VkKeyboardColor.POSITIVE, payload={"button":"воскрешение"})
    keyboard.add_line()
    keyboard.add_button("Начать заново", VkKeyboardColor.NEGATIVE, {"button":"начать заново"})
    keyboard = keyboard.get_keyboard()
    if user_id is not None:
        await bot.api.messages.send(peer_id=user_id, message="Доступно:", random_id=0, keyboard=keyboard)
    # else:
    #     await ans("Ваш питомец сдох", keyboard=keyboard)

@bot.on.message(PayloadRule({"button":"начать заново нет"}))
async def pere(ans: Message):
    await death(ans.peer_id)


@bot.on.message(PayloadRule({"button":"воскрешение"}))
async def resurrection(ans: Message):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Нет", VkKeyboardColor.NEGATIVE, payload={"button":"начать заново нет"})
    keyboard.add_button("Да", VkKeyboardColor.POSITIVE, payload={"button":"воскрешение да"})
    keyboard = keyboard.get_keyboard()
    await ans("Воскрешение стоит 25 донат монет, хотите продолжить?", keyboard=keyboard)


@bot.on.message(PayloadRule({"button":"воскрешение да"}))
async def resurrection_continue(ans: Message):
    u = await Users.get(user_id=ans.peer_id)
    if u.donut >= 25:
        u.donut = u.donut - 25
        u.health = 50
        u.happiness = 25
        u.hunger = 25
        u.energy = 25
        await u.save()
        b = await UsersBoolean.get(user_id=ans.peer_id)
        b.check_death = 0
        await b.save()
        await ans("Вы успешно возродили своего питомца!")
        await menu(ans)
    else:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Вернуться", VkKeyboardColor.DEFAULT, payload={"button":"начать заново нет"})
        keyboard.add_button("Пополнить", VkKeyboardColor.POSITIVE, payload={"button": "воскрешение пополнить"})
        keyboard = keyboard.get_keyboard()
        await ans("На вашем балансе недостаточно средств, хотите пополнить?", keyboard=keyboard)

@bot.on.message(PayloadRule({"button": "воскрешение пополнить"}))
async def replenishment(ans: Message):
    pass


@bot.on.message(PayloadRule({"button":"начать заново"}))
async def start_over(ans: Message):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Нет", VkKeyboardColor.POSITIVE, payload={"button": "начать заново нет"})
    keyboard.add_button("Да", VkKeyboardColor.NEGATIVE, payload={"button":"начать заново да"})
    keyboard = keyboard.get_keyboard()
    await ans("Вы точно хотите начать игру заново? В таком случае весь ваш прогресс будет утерян",
              keyboard=keyboard)


host1='localhost'
host2='91.210.170.247'

def get_connection():
    connection = pymysql.connect(host=host2,
                                 user='maslinka',
                                 password='897555887Dan!',
                                 db='test',
                                 charset='utf8mb4'
                                 )
    return connection

@bot.on.message(PayloadRule({"button":"начать заново да"}))
async def start_anew(ans: Message):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM `user_boolean` WHERE user_id = %s", (ans.from_id,))
    c.execute("DELETE FROM `user_info` WHERE user_id = %s", (ans.from_id,))
    c.execute("DELETE FROM `user_stat` WHERE user_id = %s", (ans.from_id,))
    c.execute("DELETE FROM `user_values` WHERE user_id = %s", (ans.from_id,))
    conn.commit()
    conn.close()
    await ans("Вы успешно начали игру заново!"
              "\nЧтобы продолжить напишите \"Начать\"")




bot.run_polling(skip_updates=True, on_startup=init_db)