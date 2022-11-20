from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

######################################################
start = types.ReplyKeyboardMarkup(resize_keyboard=True)

zarabotat = types.KeyboardButton("👻 Заработать")
profile = types.KeyboardButton("💚 Профиль")
info = types.KeyboardButton("💨 Информация")

start.add(zarabotat)
start.add(profile, info)



infoya = InlineKeyboardMarkup()
infoya.add(InlineKeyboardButton('👨 Владелец', url='https://t.me/F_O_L_Z'),InlineKeyboardButton('👨‍💻 Кодер', url='https://t.me/Paulfermer'))
infoya.add(InlineKeyboardButton('🤑 Выплаты', url='https://t.me/+HSpiToaawG43YWFi'), InlineKeyboardButton('💬 Чатик', url='https://t.me/+sQpzohNren43ODky'))




keyboard = InlineKeyboardMarkup()
keyboard.add(InlineKeyboardButton('Выплаты', url='https://t.me/viplatunoairdrop'))
keyboard.add(InlineKeyboardButton('Чат', url='https://t.me/noairdroprubchat'))
keyboard.add(InlineKeyboardButton('Спонсор', url='https://t.me/BearMoneyi'))
keyboard.add(InlineKeyboardButton('Спонсор', url='https://t.me/hirtioej'))
keyboard.add(InlineKeyboardButton('5₽ за реферала!', url='https://t.me/BearDropBot?start=ref-1758108751'))




vivod = InlineKeyboardMarkup()
vivod.add(InlineKeyboardButton('📤 Вывести', callback_data='vuvud'))

msg_del = InlineKeyboardMarkup()
msg_del.add(InlineKeyboardButton('❌ Закрыть', callback_data='msg_d'))


admin = types.ReplyKeyboardMarkup(resize_keyboard=True)

rassilka = types.KeyboardButton("🗣️ Рассылка")
ban = types.KeyboardButton("🔒 Заблокировать пользователя")
noban = types.KeyboardButton("🔓 Разблокировать пользователя")
balnc = types.KeyboardButton("Изменить баланс пользователю")
gmen = types.KeyboardButton("/start")

admin.add(rassilka)
admin.add(ban)
admin.add(noban)
admin.add(balnc)
admin.add(gmen)

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
nazad = types.KeyboardButton("Назад")
back.add(nazad)