import telebot
import config
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telebot import types

# Подсоединение к Google Таблицам
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
client = gspread.authorize(credentials)
# открытие таблицы
# перед этим необходимо было создать таблицу в гугл диске
# и дать сервисному аккаунту права на редактирование
sheet = client.open("ilka").sheet1

try:
    if states:
        pass
except:
    states = dict()

bot = telebot.TeleBot(config.TOKEN)


def sheet_finder(sheet, value):
    array = sheet.get_values()
    for i in range(1, len(array)):
        if array[i][0] == value:
            return array[i][1]
    return -1


@bot.message_handler(commands=['start'])
def welcome(message):
    global states
    states[message.chat.id] = 0
    # клава
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Сделать заказ 📲")
    item2 = types.KeyboardButton("Срок доставки 🚚")
    item3 = types.KeyboardButton("Рассчитать стоимость 🧮")
    item4 = types.KeyboardButton("Ответы на вопросы 🙏")
    item5 = types.KeyboardButton("Актуальный курс 💹")
    item6 = types.KeyboardButton("Техподдержка 👨‍🎤")
    item7 = types.KeyboardButton("Отзывы 💁‍♂️💁‍♀")
    item8 = types.KeyboardButton("Товары в наличии 🛍")
    item9 = types.KeyboardButton("Акции 🔥")
    markup.row(item1, item5)
    markup.row(item3, item7)
    markup.row(item4, item8)
    markup.row(item2, item6)
    markup.row(item9)
    bot.send_message(message.chat.id, "Приветствуем вас!\n\nВыберете нужный пункт для продолжения:", parse_mode='html',
                     reply_markup=markup)


def value_order(personal_id, state):
    global states
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Актуальный курс 💹")
    item2 = types.KeyboardButton("В главное меню")
    markup.add(item1, item2)
    bot.send_message(personal_id, "Статус вашего заказа:{}".format(state), reply_markup=markup)

def search_order(personal_id):
    global states, ban_word
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("В главное меню")
    markup.add(item1)
    bot.send_message(personal_id, "Среднее время доставки товара от момента покупки до его получения на нашем складе: 2-4 недели.\n\n"
                                  "Срок доставки складывается из:\n\n1. Доставка от Poizon до склада в Китае (2-6 дней)\n\n"
                                  "Точный срок доставки написан на кнопках в приложении.\n\n"
                                  "2. Доставка со склада в Китае до Москвы (14-18 дней)\n\n"
                                  "Все полученные товары с Poizon на нашем складе в Китае мы отправляем в Россию каждые 1-2 дня.\n\n"
                                  "3. Доставка из Москвы до вашего города.\n\n"
                                  "Все заказы по России мы отправляем через СДЭК на следующий день как получили товар в магазине.\n\n"
                                  "Самостоятельно вы можете узнать сроки доставки на сайте СДЭК (https://www.cdek.ru/ru/calculate), выбрав коробку размера М.", reply_markup=markup)
    bot.send_message(personal_id,"**Готов оформить заказ или остались вопросы?**\n\n"
                                 "Пиши сюда @logisticsxstore\n\n"
                                 "Это чат с нашими менеджерами.",reply_markup=markup)


def position_order(personal_id):
    global states
    markups = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Товары в наличии",
                                         url="https://vk.com/market-217938774")
    button2 = types.InlineKeyboardButton("В главное меню", callback_data='welcome')
    markups.add(button1)
    markups.add(button2)
    bot.send_message(personal_id, "Актуальный каталог по ссылке ниже ⤵️.", reply_markup=markups)
    states[personal_id] = 0


def nothing_value(personal_id):
    global states
    markups = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Техническая поддержка", url="https://vk.com/kkklementev")
    button2 = types.InlineKeyboardButton("Ввести заказ заново", callback_data='again')
    markups.add(button1, button2)
    bot.send_message(personal_id, "Похоже, Вы неправильно ввели номер вашего заказа.", reply_markup=markups)
    states[personal_id] = 0


def new_order(personal_id):
    markups = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        "Заказать",
        url="https://vk.com/im?media=&sel=-214425199")
    button2 = types.InlineKeyboardButton("В главное меню", callback_data='welcome')
    markups.add(button1)
    markups.add(button2)
    bot.send_message(personal_id,
                     "Для того, чтобы сделать заказ - напишите нашему менеджеру. Контакты ниже ⬇️",
                     reply_markup=markups)
    states[personal_id] = 0


def tech(personal_id):
    markups = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Техническая поддержка", url="https://vk.com/im?media=&sel=-214425199")
    button2 = types.InlineKeyboardButton("В главное меню", callback_data='welcome')
    markups.add(button1)
    markups.add(button2)
    bot.send_message(personal_id,
                     "Возник вопрос? Мы обязательно поможем!",
                     reply_markup=markups)


def sum_order(personal_id):
    global states
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Одежда")
    item2 = types.KeyboardButton("Кроссовки")
    markup.add(item1, item2)
    bot.send_message(personal_id,
                     "Выберите один из предложенных вариантов:",
                     reply_markup=markup)
    states[personal_id] = 2



def review(personal_id):
    markups = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Отзывы", url="https://vk.com/topic-214425199_48948017")
    button2 = types.InlineKeyboardButton("В главное меню", callback_data='welcome')
    markups.add(button1)
    markups.add(button2)
    image = open('Frame_2211.png', 'rb')
    bot.send_photo(personal_id, image)
    bot.send_message(personal_id,
                     "С полным списком отзывов Вы можете ознакомиться, перейдя по кнопке ниже ⬇️",
                     reply_markup=markups)


def the_end(personal_id):
    global states
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("В главное меню")
    markup.add(item1)
    bot.send_message(personal_id, "Спасибо за твой чудесный отзыв", reply_markup=markup)
    states[personal_id] = 0


def fix_price(value, message):
    global states
    global sheet
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Посчитать еще")
    item2 = types.KeyboardButton("В главное меню")
    markup.add(item1, item2)
    cost = sheet.get_values()[0][1]
    answer = value * float(cost) + 1000
    bot.send_message(message.chat.id,
                     "{0} ₽ - это цена товаров + доставка до нашего склада в Китае со склада POIZON + легит-чек от основной группы + страховка товара + наша комиссия за работу\n\nК этой стоимости нужно будет приплюсовать доставку с Китая в Москву, когда товар будет выкуплен и доставлен на наш склад. Её стоимость рассчитывается 500₽/500гр\n\nОптовые заказы - @kkklementev".format(
                         answer), reply_markup=markup)
    states[message.chat.id] = 0


def price(message, personal_id):
    global states, ban_word
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("В главное меню")
    markup.add(item1)
    image = open('Frame_2210.png', 'rb')
    bot.send_photo(personal_id, image)
    bot.send_message(personal_id, "Какая сумма на бирюзовой кнопке?", reply_markup=markup)

    states[personal_id] = 3


def faq(personal_id, message):
    global states
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item0 = types.KeyboardButton('Что такое POIZON?')
    item1 = types.KeyboardButton('Оригинал?')
    item2 = types.KeyboardButton('Сколько стоит доставка?')
    item3 = types.KeyboardButton('Как забрать свой заказ?')
    item4 = types.KeyboardButton('Можете ли вы доставить посылку в другой город?')
    item5 = types.KeyboardButton('Главное меню')
    for i in [item0, item1, item2, item3, item4, item5]:
        markup.add(i)
    bot.send_message(personal_id, 'Часто задаваемые вопросы:', reply_markup=markup)
    states[personal_id] = 4


def answer(message, personal_id):
    global states
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item0 = types.KeyboardButton('Задать еще один вопрос')
    item1 = types.KeyboardButton('Главное меню')
    for i in [item0, item1]:
        markup.add(i)
    states[personal_id] = 0
    if message.text == 'Оригинал?':
        img = open('how.jpg', 'rb')
        bot.send_photo(personal_id, img)
        bot.send_message(personal_id,
                         'POIZON пошли на очень серьезное улучшение сервиса и внедрили несколько степеней проверки. Согласно последним данным, платформа подтверждает в среднем 4851 пару за один день.\n\n'
                         '«Стремясь к 100-процентной точности аутентификации, мы приложим все возможные усилия, чтобы положить конец всем подделкам на нашей платформе».\n\n'
                         'Компания приняла решение, что кроссовки с POIZON будут проходить максимально полную проверку, а только затем отправляться покупателю. Если же покупателю все-таки каким-то образом попадет фейк или реплика, то платформа гарантирует возврат суммы заказа в трехкратном размере.\n\n'
                         'Это позволило POIZON обеспечить легитимность поставок, выступая в качестве беспристрастного и авторитетного стороннего аутентификатора в своей торговой сделке. Таким образом платформа не продают обувь напрямую, а выступает в качестве посредника, взимая плату исключительно в первую очередь за точнейшую аутентификацию, доставку и обслуживание.',
                         reply_markup=markup)
    if message.text == 'Что такое POIZON?':
        img = open('what_is.png', 'rb')
        bot.send_photo(personal_id, img)
        bot.send_message(personal_id,
                         'POIZON — китайская торговая площадка, специализирующаяся на продаже оригинальных кроссовок, предметов одежды, коллекционных вещей и так далее. Это не совсем интернет-магазин в стандартном понимании этого слова. Пойзон является больше посредником с комплексом услуг аналогично американским платформам, таким как StockX и Goats, которые уже долгое время популярны на рынке.\n\n'
                         'Сайт POIZON в настоящее время собирает порядка 90 млн активных пользователей в месяц, а стоимость проекта в марте 2022 года превысила 1 миллиард долларов США. Это привлекло на китайский рынок совершенно новый класс розничных продавцов.',
                         reply_markup=markup)
    if message.text == 'Сколько стоит доставка?':
        bot.send_message(personal_id, 'Стоимость доставки рассчитывается после взвешивания вашего заказа.\n\n'
                                      'Расчет идет 500₽/500гр.\n\n'
                                      'Оплачивается при получении.', reply_markup=markup)
    if message.text == 'Как забрать свой заказ?':
        bot.send_message(personal_id,
                         'Адрес самовывоза в Москве: Смольная 24А, Бизнес-центр\nГлавный вход, 11 этаж  Метро Беломорская\n\n'
                         'График работы: 10:00-22:00\n\n'
                         '— Вещи в регионы отправляются СДЕКом на следующий день после поступления на наш склад в Москве , мы имеем контракт со СДЕКом , который уменьшает стоимость доставки на 70%',
                         reply_markup=markup)
    if message.text == 'Можете ли вы доставить посылку в другой город?':
        bot.send_message(personal_id,
                         'В данных получателя строго ПРАВИЛЬНО указывайте свои данные. После успешного создания накладной не забудьте скинуть её номер в службу поддержки. Не забудьте оплатить за доставку до Москвы!',
                         reply_markup=markup)


def currency(personal_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    img = open('Frame_2208.png', 'rb')
    bot.send_photo(personal_id, img)
    item1 = types.KeyboardButton("Назад")
    markup.add(item1)
    cost = sheet.get_values()[0][0]
    bot.send_message(personal_id, f'Текущий курс {cost}₽  = 1 ¥', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    global service
    personal_id = message.chat.id
    try:
        pos = states[personal_id]
    except:
        states[personal_id] = 0
    if True:
        if message.text == '/sum':
            price(message, personal_id)
            return 0
        if message.text == '/currency':
            currency(personal_id)
            states[personal_id] = 0
            return 0
        if message.text == '/search':
            search_order(personal_id)
            states[personal_id] = 0
            return 0
        if message.text == '/faq':
            faq(personal_id, message)
            return 0
        if states[personal_id] == 3:
            try:
                value = int(message.text)
                fix_price(value, message)
                return 0
            except:
                if message.text in ["В главное меню", "Сделать заказ 📲", "Срок доставки 🚚",
                                    "Рассчитать стоимость 🧮", "Ответы на вопросы 🙏",
                                    "Актуальный курс 💹", "✅Техподдержка 👨‍🎤",
                                    "Отзывы 💁‍♂️💁‍♀", "Товары в наличии 🛍","Акции 🔥"]:
                    states[personal_id] = 0
                else:
                    bot.send_message(message.chat.id, "Неверный формат")
                    price(message, personal_id)
                    return 0
        if states[personal_id] == 4:
            if message.text in ['Оригинал?', 'Можете ли вы доставить посылку в другой город?',
                                'Как забрать свой заказ?', 'Сколько стоит доставка?', 'Что такое POIZON?']:
                answer(message, personal_id)
                return 0
            elif message.text == 'Главное меню':
                welcome(message)
                return 0
            else:
                states[personal_id] = 0
        if states[personal_id] == 0:
            if message.text == "Сделать заказ 📲":
                new_order(personal_id)
            elif message.text == "Акции 🔥":
                bot.send_message(personal_id, "Мы сразу же вас уведомим о начале новой акции 👌")
            elif message.text == "Срок доставки 🚚":
                search_order(personal_id)
            elif message.text == "Ответы на вопросы 🙏" or message.text == "Задать еще один вопрос":
                faq(personal_id, message)
            elif message.text == "Рассчитать стоимость 🧮":
                price(message, personal_id)
            elif message.text == "Посчитать еще":
                price(message, personal_id)
            elif message.text == 'Товары в наличии 🛍':
                position_order(personal_id)
            elif message.text == 'Актуальный курс 💹':
                currency(message.chat.id)
            elif message.text == 'В главное меню' or message.text == 'Назад' or message.text == 'Главное меню':
                welcome(message)
            elif message.text == "Техподдержка 👨‍🎤":
                tech(personal_id)
            elif message.text == "Отзывы 💁‍♂️💁‍♀":
                review(personal_id)
            else:
                bot.send_message(message.chat.id, "Введите корректные данные")
                welcome(message)
            return 0
        if states[personal_id] == 1:
            key = str(message.text)
            state = sheet_finder(sheet, key)
            if state != -1:
                value_order(personal_id, state)
            else:
                nothing_value(personal_id)
            states[personal_id] = 0
            return 0
        if states[personal_id] == 2:
            price(message, personal_id)
            return 0

        if states[personal_id] == 5:
            the_end(personal_id)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'welcome':
            welcome(call.message)
        if call.data == 'again':
            search(call.message.chat.id)


bot.infinity_polling()
