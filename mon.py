from telebot import types
from sc_client import client
from stalcraft import LocalItem, Order, Sort
from main import bot

def create_armor_keyboard(chat_id, call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_hveteranarmor = types.InlineKeyboardButton(text="Ветеран🟣", callback_data="hveteran_armor")
    button_hmasterarmor = types.InlineKeyboardButton(text="Мастер🔴", callback_data="hmaster_armor")
    button_hlegendarmor = types.InlineKeyboardButton(text="Легенда🟡", callback_data="hlegend_armor")
    markup.add(button_hveteranarmor, button_hmasterarmor, button_hlegendarmor)
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Хорошо! Теперь выберете ранг интересующей Вас брони:", reply_markup=markup)

def create_weapon_keyboard(chat_id, call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_hveteran = types.InlineKeyboardButton(text="Ветеран🟣", callback_data="hveteran_weapon")
    button_hmaster = types.InlineKeyboardButton(text="Мастер🔴", callback_data="hmaster_weapon")
    button_hlegend = types.InlineKeyboardButton(text="Легенда🟡", callback_data="hlegend_weapon")
    markup.add(button_hveteran, button_hmaster, button_hlegend)
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Хорошо! Теперь выберете ранг интересующего Вас оружия:", reply_markup=markup)

def send_lot_info(chat_id, ITEM_ID, description, is_recommended=True):
    lots = client.auction(ITEM_ID).lots(limit=10, sort=Sort.BUYOUT_PRICE, order=Order.ASC, additional=True)

    message_text = f"Описание лота:\n{description}\nСовет: к перепродаже { 'советую✅' if is_recommended else 'не советую❌' }\n\n"

    for lot in lots:
        start_time_str = lot.start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = lot.end_time.strftime('%Y-%m-%d %H:%M:%S')
        formatted_start_price = "{:,.0f}".format(lot.start_price).replace(",", ".")
        formatted_buyout_price = "{:,.0f}".format(lot.buyout_price).replace(",", ".")
        seller_name = lot.additional.get('buyer', 'Неизвестно')

        message_text += f"Стартовая цена💰: {formatted_start_price}\nЦена выкупа💸:{formatted_buyout_price}\nВремя создания лота⌚️:{start_time_str}\nВремя завершения лота⏱:{end_time_str}\nПродавец: {seller_name}\n\n"

    markup = types.InlineKeyboardMarkup(row_width=1)
    button_history = types.InlineKeyboardButton(text="История продаж", callback_data=f"{ITEM_ID.name}HISTORY")
    markup.add(button_history)

    bot.send_message(chat_id, message_text, reply_markup=markup)

def send_price_history(chat_id, ITEM_ID):
    try:
        price_history = client.auction(ITEM_ID).price_history(limit=50)

        message_text = f"История продаж {ITEM_ID.name}:\n\n"

        for price_entry in price_history:
            amount = price_entry.amount
            price = price_entry.price
            time_str = price_entry.time.strftime('%Y-%m-%d %H:%M:%S')
            formatted_price = "{:,}".format(price).replace(",", ".")

            message_text += f"Количество: {amount}, Цена: {formatted_price}, Время: {time_str}\n\n"
    except AttributeError:
        message_text = "Ошибка: История продаж недоступна."

    bot.send_message(chat_id, message_text)

@bot.callback_query_handler(func=lambda call: call.data == "harmor")
def handle_callback_query_harmor(call):
    chat_id = call.message.chat.id
    from auc import user_threads
    if chat_id in user_threads:
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                         text="Вы уже мониторите лот❗\nОстановите мониторинг текущего лота, чтобы начать отслеживать новый.\nЧтобы остановить пропишите команду /stop")
        return
    create_armor_keyboard(chat_id, call)  # Передаем call

@bot.callback_query_handler(func=lambda call: call.data == "hweapon")
def handle_callback_query_hweapon(call):
    chat_id = call.message.chat.id
    from auc import user_threads
    if chat_id in user_threads:
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                         text="Вы уже мониторите лот❗\nОстановите мониторинг текущего лота, чтобы начать отслеживать новый.\nЧтобы остановить пропишите команду /stop")
        return
    create_weapon_keyboard(chat_id, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("hveteran_weapon"))
def handle_callback_query_weapon_veteran_weapon(call):
    chat_id = call.message.chat.id

    markup = types.InlineKeyboardMarkup(row_width=1)
    button_hPSG = types.InlineKeyboardButton(text="HK PSG1", callback_data="hPSG")
    button_h94CB = types.InlineKeyboardButton(text="СВ-98", callback_data="h94CB")
    button_haug9m = types.InlineKeyboardButton(text="AUG 9mm", callback_data="haug9m")
    button_hauga1 = types.InlineKeyboardButton(text="AUG A1", callback_data="hauga1")
    button_hauga2 = types.InlineKeyboardButton(text="AUG A2", callback_data="hauga2")
    button_hauga3 = types.InlineKeyboardButton(text="AUG A3", callback_data="hauga3")
    button_hmc116 = types.InlineKeyboardButton(text="МЦ-116М", callback_data="hmc116")
    button_hm1014 = types.InlineKeyboardButton(text="M1014 Breacher", callback_data="hBreacher")
    button_hshtorm = types.InlineKeyboardButton(text="ОЦ-14М Шторм", callback_data="hshtorm")
    button_hrmo = types.InlineKeyboardButton(text="РМО-93", callback_data="hrmo")
    button_hrpk16 = types.InlineKeyboardButton(text="РПК-16", callback_data="hrpk16")
    button_hsix = types.InlineKeyboardButton(text="Crye Precision SIX12", callback_data="hsix12")
    button_hak12 = types.InlineKeyboardButton(text="АК-12", callback_data="hak12")
    button_helb = types.InlineKeyboardButton(text="Эльбрус", callback_data="helb")

    markup.add(button_hPSG, button_h94CB, button_haug9m, button_hauga1, button_hauga2, button_hauga3,
               button_hmc116, button_hm1014, button_hshtorm, button_hrmo, button_hrpk16,
               button_hsix, button_hak12, button_helb)
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Хорошо! Выбери оружие:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "hPSG")
def handle_callback_query_hPSG(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("HK PSG1"), "PSG- одна из самых часто покупаемых начинающими игроками на юз. Имеет очень хорошие характеристики и в бою на ветеранских серверах очень хорошо себя показывает.")

@bot.callback_query_handler(func=lambda call: call.data == "h94CB")
def handle_callback_query_h94CB(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("SV-98"), "СВ-98- одна из самых часто покупаемых начинающими игроками на юз. Имеет очень хорошие характеристики и в бою на ветеранских серверах очень хорошо себя показывает.")

@bot.callback_query_handler(func=lambda call: call.data == "haug9m")
def handle_callback_query_haug9m(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Steyr AUG 9mm"), "AUG 9mm - автомат,который для меня является ошибкой новичка. Его хоть и часто покупают начинающие, которые еще не разбираются в игре, но больше 10 штук я бы не брал сразу. Сам на этом ауге сделал около 10 миллонов, скупая дешево оптом.")

@bot.callback_query_handler(func=lambda call: call.data == "hauga1")
def handle_callback_query_hauga1(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Steyr AUG A1"), "AUG A1- пожалуй как M4LB, является одним из лучших вариантов для начинающего игрока, пользуется спросом, но лучше подомные лоты покупать оптом.")

@bot.callback_query_handler(func=lambda call: call.data == "hauga2")
def handle_callback_query_hauga2(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Steyr AUG A2"), "AUG A2- пожалуй как Aug A1, является одним из лучших вариантов для начинающего игрока, пользуется спросом, но лучше подомные лоты покупать оптом.")

@bot.callback_query_handler(func=lambda call: call.data == "hauga3")
def handle_callback_query_hauga3(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Steyr AUG A3"), "AUG A3- никогда не понимал зачем люди покупают его, очень редко его перепродавал, на 1000 сделок максимум 2-3 были ауг А3.", is_recommended=False)

@bot.callback_query_handler(func=lambda call: call.data == "hmc116")
def handle_callback_query_hmc116(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("MTs-116M"), "МЦ-116М - скорострельнее, чем св98 из-за чего и стоит дороже. Она хороша как для перепродаже, так и на юз.")

@bot.callback_query_handler(func=lambda call: call.data == "hBreacher")
def handle_callback_query_hBreacher(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("M1014"), "Не перепродавал его и не интересуюсь, но это очень хорошая замена вторичному дробовику Оц-62, поэтому спрос на нее есть.")

@bot.callback_query_handler(func=lambda call: call.data == "hshtorm")
def handle_callback_query_hshtorm(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("OTs-14M Shtorm"), "Шторм всегда пользовался и будет пользоваться спросом у начинающих игроков. Обладает хорошим скорострелом и уроном, но пока нет анимаций. Думаю будет чуть дороже, когда сделают анимации.")

@bot.callback_query_handler(func=lambda call: call.data == "hrmo")
def handle_callback_query_hrmo(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("RMB-93"), "Этот дробовик набирает сейчас популярность, ибо является очень хорошей заменой протекте и АА-12.")

@bot.callback_query_handler(func=lambda call: call.data == "hrpk16")
def handle_callback_query_hrpk16(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("RPK-16"), "РПК-16 хороший пулемет, хорошо продается.")

@bot.callback_query_handler(func=lambda call: call.data == "hsix12")
def handle_callback_query_hsix12(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Crye Precision SIX12"), "Вторичка,которая многим нравится, но я никогда ее не брал на перекуп и на юз, ибо как по мне есть лучше варианты.", is_recommended=False)

@bot.callback_query_handler(func=lambda call: call.data == "hak12")
def handle_callback_query_hak12(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("AK-12"), "AK-12 очень хороший автомат и пользуется спросом.")

@bot.callback_query_handler(func=lambda call: call.data == "helb")
def handle_callback_query_helb(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Elbrus Short Range Detector"), "Тот самый предмет, на котором можно на перепродаже сделать немалые суммы.")

@bot.callback_query_handler(func=lambda call: call.data.endswith("HISTORY"))
def handle_callback_query_history(call):
    chat_id = call.message.chat.id
    item_name = call.data[:-7]
    send_price_history(chat_id, LocalItem(item_name))


@bot.callback_query_handler(func=lambda call: call.data == "hmaster_weapon")
def handle_callback_query_weapon_master_weapon(call):
    chat_id = call.message.chat.id

    markup = types.InlineKeyboardMarkup(row_width=1)
    button_jag = types.InlineKeyboardButton(text="Jagdkommando", callback_data="jag")
    button_xms = types.InlineKeyboardButton(text="HK XM8S", callback_data="xms")
    button_a308 = types.InlineKeyboardButton(text="АК-308", callback_data="a308")
    button_a12 = types.InlineKeyboardButton(text="AA-12", callback_data="aa12")
    button_vsk = types.InlineKeyboardButton(text="ВСК-94", callback_data="vsk")
    button_fal = types.InlineKeyboardButton(text="FN FAL", callback_data="fal")
    button_parash = types.InlineKeyboardButton(text="Scar-H", callback_data="parash")
    button_ptrd = types.InlineKeyboardButton(text="ПТРД-М", callback_data="ptrd")

    markup.add(button_jag, button_xms, button_a308, button_a12, button_vsk, button_fal, button_parash, button_ptrd)
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Хорошо! Выбери оружие:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "jag")
def handle_callback_query_jag(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Jagdkommando"), "Один из самых лучших ножей, плюс отличная анимация.")

@bot.callback_query_handler(func=lambda call: call.data == "xms")
def handle_callback_query_xms(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("HK XM8S"), "Пока является одной из самых бесполезный пушек, но я думаю скоро она заиграет.")

@bot.callback_query_handler(func=lambda call: call.data == "a308")
def handle_callback_query_a308(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("AK-308"), "Редко перепродавал АК-308, ибо тяжко перепродавался, сейчас, когда ему повысили статы, думаю хорошо будет продаваться.")

@bot.callback_query_handler(func=lambda call: call.data == "aa12")
def handle_callback_query_aa12(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("AA-12"), "Хороший дробовик, пользуется спросом.")

@bot.callback_query_handler(func=lambda call: call.data == "vsk")
def handle_callback_query_vsk(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("ВСК-94"), "Сейчас очень хорошо перепродается, ибо выпадает из элитного кейса, а некоторые начинающие игроки не знают цены и с этого можно сделать пару миллионов на одной сделке, например я недавно купил его за 10кк, а продал за 13кк.")

@bot.callback_query_handler(func=lambda call: call.data == "fal")
def handle_callback_query_fal(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("FN FAL"), "Хороший автомат, на котором я сделал  несколько десятков миллионов.")

@bot.callback_query_handler(func=lambda call: call.data == "parash")
def handle_callback_query_parash(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("FN SCAR-H"), "Хороший автомат, на котором я сделал  несколько десятков миллионов.")

@bot.callback_query_handler(func=lambda call: call.data == "ptrd")
def handle_callback_query_ptrd(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("PTRD-M"), "Никогда не брал на юз, только перепродавал, хорошо продается.")

@bot.callback_query_handler(func=lambda call: call.data == "jagHISTORY")
def handle_callback_query_jagHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("Jagdkommando"))

@bot.callback_query_handler(func=lambda call: call.data == "xmsHISTORY")
def handle_callback_query_xmsHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("HK XM8S"))

@bot.callback_query_handler(func=lambda call: call.data == "a308HISTORY")
def handle_callback_query_a308HISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("AK-308"))

@bot.callback_query_handler(func=lambda call: call.data == "a12HISTORY")
def handle_callback_query_a12HISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("AA-12"))

@bot.callback_query_handler(func=lambda call: call.data == "vskHISTORY")
def handle_callback_query_vskHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("ВСК-94"))

@bot.callback_query_handler(func=lambda call: call.data == "falHISTORY")
def handle_callback_query_falHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("FN FAL"))

@bot.callback_query_handler(func=lambda call: call.data == "parashHISTORY")
def handle_callback_query_parashHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("FN SCAR-H"))

@bot.callback_query_handler(func=lambda call: call.data == "ptrdHISTORY")
def handle_callback_query_ptrdHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("PTRD-M"))


@bot.callback_query_handler(func=lambda call: call.data == "hlegend_weapon")
def handle_callback_query_weapon_legend_weapon(call):
    chat_id = call.message.chat.id
    # Create an inline keyboard with weapon options
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_gays = types.InlineKeyboardButton(text="Гаусс-Пушка", callback_data="gays")
    markup.add(button_gays)
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Хорошо! Выбери оружие:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "gays")
def handle_callback_query_gays(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Gauss Rifle"), "Сейчас уже думаю нет смысла искать его на рынке,но возможно какой-то игрок держит ее и выставит на аукцион.")

@bot.callback_query_handler(func=lambda call: call.data == "gaysHISTORY")
def handle_callback_query_gaysHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("Gauss Rifle"))

@bot.callback_query_handler(func=lambda call: call.data == "hveteran_armor")
def handle_callback_query_veteran_armor(call):
    chat_id = call.message.chat.id
    # Create an inline keyboard with weapon options
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_hmag = types.InlineKeyboardButton(text="Магнит", callback_data="hmag")
    button_htum = types.InlineKeyboardButton(text="Туманка", callback_data="htum")
    button_htong = types.InlineKeyboardButton(text="Тонга", callback_data="htong")
    button_hirh = types.InlineKeyboardButton(text="Йорш", callback_data="hirh")
    button_hspan = types.InlineKeyboardButton(text="Спаннер", callback_data="hspan")
    button_ham = types.InlineKeyboardButton(text="Аметист", callback_data="ham")
    button_hlaz = types.InlineKeyboardButton(text="Лазутчик", callback_data="hlaz")
    button_hraz = types.InlineKeyboardButton(text="Разведка", callback_data="hraz")
    markup.add(button_hmag, button_htum, button_htong, button_hirh, button_hspan, button_ham, button_hlaz, button_hraz)
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Хорошо! Выбери броню:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "hmag")
def handle_callback_query_hmag(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Magnet Jumpsuit"), "Магнит-один из самых покупаемых научных костюмов. Он обладает хорошей защитой от заражений и легко перепродается.")

@bot.callback_query_handler(func=lambda call: call.data == "hmagHISTORY")
def handle_callback_query_hmagHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("Magnet Jumpsuit"))

@bot.callback_query_handler(func=lambda call: call.data == "htum")
def handle_callback_query_htum(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Fog Hunter Heavy Armored Suit"), "Туманный охотник-пользуется спросом, Но не так как раньше.")

@bot.callback_query_handler(func=lambda call: call.data == "htumHISTORY")
def handle_callback_query_htumHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("Fog Hunter Heavy Armored Suit"))

@bot.callback_query_handler(func=lambda call: call.data == "htong")
def handle_callback_query_htong(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Tonga Jumpsuit"), "Тонга-один из самых покупаемых научных костюмов. Он обладает хорошей защитой от заражений и легко перепродается.")

@bot.callback_query_handler(func=lambda call: call.data == "htongHISTORY")
def handle_callback_query_htongHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("Tonga Jumpsuit"))

@bot.callback_query_handler(func=lambda call: call.data == "hirh")
def handle_callback_query_hirh(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Yorsh Protective Armored Suit"), "Йорш пока не пользуется особым спромо, но скоро добавят данжи и он будет дороже. Например в начале своего пути я постоянно закупался перед средой схемы йорша.")

@bot.callback_query_handler(func=lambda call: call.data == "hirhHISTORY")
def handle_callback_query_hirhHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("Yorsh Protective Armored Suit"))

@bot.callback_query_handler(func=lambda call: call.data == "hspan")
def handle_callback_query_hspan(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("RAPS Spanner"), "Редко вижу игроков в спаннера, Но продавались они у меня быстро.")

@bot.callback_query_handler(func=lambda call: call.data == "hspanHISTORY")
def handle_callback_query_hspanHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("RAPS Spanner"))

@bot.callback_query_handler(func=lambda call: call.data == "ham")
def handle_callback_query_ham(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("MIS-122 Amethyst"), "Ранее стоил менее 2 миллионов и можно было с него легко делать 300-500к, сейчас дорогой и не понимаю зачем люди его покупают, ибо он есть в бартере.")

@bot.callback_query_handler(func=lambda call: call.data == "hamHISTORY")
def handle_callback_query_hamHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("MIS-122 Amethyst"))

@bot.callback_query_handler(func=lambda call: call.data == "hlaz")
def handle_callback_query_hlaz(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Albatross Infiltrator Armored Exoskeleton"), "Пользуется спросом у начинающих игроков, которые не хотят идти дальше ветеранок.")

@bot.callback_query_handler(func=lambda call: call.data == "hlazHISTORY")
def handle_callback_query_hlazHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("Albatross Infiltrator Armored Exoskeleton"))

@bot.callback_query_handler(func=lambda call: call.data == "hraz")
def handle_callback_query_hraz(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Albatross Scout Armored Exoskeleton"), "Пользуется спросом у начинающих игроков, которые не хотят идти дальше ветеранок.")

@bot.callback_query_handler(func=lambda call: call.data == "hrazHISTORY")
def handle_callback_query_hrazHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("Albatross Scout Armored Exoskeleton"))

@bot.callback_query_handler(func=lambda call: call.data == "hmaster_armor")
def handle_callback_query_master_armor(call):
    chat_id = call.message.chat.id
    # Create an inline keyboard with weapon options
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_hzivk = types.InlineKeyboardButton(text="Зивкас", callback_data="hzivk")
    button_hrig = types.InlineKeyboardButton(text="Ригель", callback_data="hrig")
    button_hkz = types.InlineKeyboardButton(text="КЗ-4", callback_data="hkz")
    button_htank = types.InlineKeyboardButton(text="Танк", callback_data="htank")
    button_hmod = types.InlineKeyboardButton(text="Модифицированный экзоскелет", callback_data="hmod")
    markup.add(button_hzivk, button_hrig, button_hkz, button_htank, button_hmod)
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Хорошо! Выбери броню:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "hzivk")
def handle_callback_query_hzivk(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("JD ZIVCAS 2A Exoarmor"), "ZIVCAS-обладает отличными статами и желающих купить его немало.")

@bot.callback_query_handler(func=lambda call: call.data == "hrig")
def handle_callback_query_hrig(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Rigel Jumpsuit"), "Ригель-обладает отличными статами и желающих купить его немало.")

@bot.callback_query_handler(func=lambda call: call.data == "hkz")
def handle_callback_query_hkz(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("CD-4 Armored Suit"), "КЗ-4 очень хорошая броня, пользуются споросом у любителей пкашить или для клановых войн, с него легко можно сделать 1-3кк окупа.")

@bot.callback_query_handler(func=lambda call: call.data == "htank")
def handle_callback_query_htank(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("SBA TANK"), "SBA TANK очень хорошая броня, пользуются споросом у любителей пкашить или для клановых войн.")

@bot.callback_query_handler(func=lambda call: call.data == "hmod")
def handle_callback_query_hmod(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Modified Exoskeleton"), "Модка очень хорошая броня, пользуются споросом у любителей пкашить или для клановых войн, с него легко можно сделать 1-3кк окупа.")


@bot.callback_query_handler(func=lambda call: call.data == "hzivkHISTORY")
def handle_callback_query_hzivkHISTORY(call):
    chat_id = call.message.chat.id  # Исправлено: используем chat.id
    send_price_history(chat_id, LocalItem("JD ZIVCAS 2A Exoarmor"))

@bot.callback_query_handler(func=lambda call: call.data == "hrigHISTORY")
def handle_callback_query_hrigHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("Rigel Jumpsuit"))

@bot.callback_query_handler(func=lambda call: call.data == "hkzHISTORY")
def handle_callback_query_hkzHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("CD-4 Armored Suit"))

@bot.callback_query_handler(func=lambda call: call.data == "htankHISTORY")
def handle_callback_query_htankHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("SBA TANK"))

@bot.callback_query_handler(func=lambda call: call.data == "hmodHISTORY")
def handle_callback_query_hmodHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("Modified Exoskeleton"))


@bot.callback_query_handler(func=lambda call: call.data == "hlegend_armor")
def handle_callback_query_legend_armor(call):
    chat_id = call.message.chat.id
    # Create an inline keyboard with weapon options
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_hshrm = types.InlineKeyboardButton(text="Альбатрос-Штурмовик", callback_data="hshrm")
    markup.add(button_hshrm)
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Хорошо! Выбери броню:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "hshrm")
def handle_callback_query_hshrm(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Albatross Heavy Assault Armored Exoskeleton"), "")

@bot.callback_query_handler(func=lambda call: call.data == "a16HISTORY")
def handle_callback_query_a16HISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("Albatross Heavy Assault Armored Exoskeleton"))

@bot.callback_query_handler(func=lambda call: call.data == "hcont")
def handle_callback_query_cont(call):
    chat_id = call.message.chat.id
    from auc import user_threads
    if chat_id in user_threads:
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                         text="Вы уже мониторите лот❗\nОстановите мониторинг текущего лота, чтобы начать отслеживать новый.\nЧтобы остановить пропишите команду /stop")
        return
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_six = types.InlineKeyboardButton(text="Берлога 6у", callback_data="hsix")
    button_four = types.InlineKeyboardButton(text="Берлога 4у", callback_data="hfour")
    button_hksm = types.InlineKeyboardButton(text="КСМ", callback_data="hksm")
    markup.add(button_four, button_six, button_hksm)
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Хорошо! Выбери контейнер:", reply_markup=markup)

# Handler for "Берлога 6у"
@bot.callback_query_handler(func=lambda call: call.data == "hsix")
def handle_callback_query_hsix(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Berloga-6u Container"), "Берлога 6у - контейнер с большим количеством полезных вещей.")

# Handler for "Берлога 6у" history
@bot.callback_query_handler(func=lambda call: call.data == "hsixHISTORY")
def handle_callback_query_hsixHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("Berloga-6u Container"))

# Handler for "Берлога 4у"
@bot.callback_query_handler(func=lambda call: call.data == "hfour")
def handle_callback_query_hfour(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("Berloga-4u Container"), "Берлога 4у - контейнер с меньшим количеством вещей, но более дорогой.")

# Handler for "Берлога 4у" history
@bot.callback_query_handler(func=lambda call: call.data == "hfourHISTORY")
def handle_callback_query_hfourHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("Berloga-4u Container"))

# Handler for "КСМ"
@bot.callback_query_handler(func=lambda call: call.data == "hksm")
def handle_callback_query_hksm(call):
    chat_id = call.message.chat.id
    send_lot_info(chat_id, LocalItem("SMC Container"), "КСМ - контейнер с большим количеством дешевых вещей.")

# Handler for "КСМ" history
@bot.callback_query_handler(func=lambda call: call.data == "hksmHISTORY")
def handle_callback_query_hksmHISTORY(call):
    chat_id = call.message.chat.id
    send_price_history(chat_id, LocalItem("SMC Container"))