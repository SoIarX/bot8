from aiogram import Bot, types, asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()


from Config import TOKEN
from db import Database
import Config as cfg
import Keyboard
import check_sub as csc


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database('database.db')

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )
 
 
class vuvod(StatesGroup):
    amount = State()
    addres = State()
    
class dialog(StatesGroup):
  spam = State()
  blacklist = State()
  whitelist = State()
  setbln = State()
  newbln = State()

      
@dp.message_handler(content_types=['text'], text='🗣️ Рассылка')
async def spam(message: types.Message):
    ###
    user_id = message.from_user.id
    adm = db.adm_or_no(user_id)
    if adm == 1:
        ###
        await dialog.spam.set()
        await message.answer("Напиши текст рассылки", reply_markup=Keyboard.back)

@dp.message_handler(state=dialog.spam)
async def start_spam(message: types.Message, state: FSMContext):
  if message.text == 'Назад':
    await message.answer("Админ-панель", reply_markup=Keyboard.admin)
    await state.finish()
  else:
    users = db.get_users()
    for row in users:
      try:
        await bot.send_message(row[0], message.text)
        await state.finish()
        if int(row[1]) != 1:
          db.set_active(row[0], 1)
          await asyncio.sleep(0.4)
      except:
        db.set_active(row[0], 0)
        await state.finish()
        await asyncio.sleep(0.4)
        
      await bot.send_message(message.from_user.id, "Рассылка завершена", reply_markup=Keyboard.admin)


                    
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
  user_id = message.from_user.id
  if not db.exists_user(user_id):
            start_command = message.text
            referrer_id = str(start_command[7:])
            if str(referrer_id) != "":
                  if str(referrer_id) != str(user_id):
                      db.add_user(user_id, referrer_id)
                      await message.answer("Добро пожаловать", reply_markup=Keyboard.start, parse_mode='Markdown')
                      try:
                          await bot.send_message(referrer_id, "У Вас новый реферал!\nВы получили 0.50₽")
                          balance = c.execute("SELECT balance FROM users WHERE user_id=?", (referrer_id,)).fetchone()[0]
                          addnewam = balance + 0.5
                          c.execute("UPDATE users SET balance=? WHERE user_id=?", (addnewam, referrer_id,))
                          conn.commit()
                      except:
                          pass
                  else:
                      db.add_user(user_id)
                      await bot.send_message(message.from_user.id, 'Нельзя регистрироваться по своей ссылке!')
            else:
                db.add_user(user_id)
                await message.answer("Добро пожаловать", reply_markup=Keyboard.start, parse_mode='Markdown')
  else:
        await message.answer("Добро пожаловать", reply_markup=Keyboard.start, parse_mode='Markdown') 
    
    
    
@dp.message_handler(commands=['adminp'])
async def process_admin_command(message: types.Message):
  ###
  user_id = message.from_user.id
  adm = db.adm_or_no(user_id)
  if adm == 1:
    ###
    await message.answer("Добро пожаловать в админ-панель\nЧтобы выйти пропишите /start", reply_markup=Keyboard.admin)
  else:
    pass




@dp.message_handler(text='👻 Заработать')
async def process_zarabotat_btn(message: types.Message):
    user_id = message.from_user.id
    block = c.execute("SELECT block FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if block == 0:
      if await csc.check_sub_channels(cfg.CHANNELS, message.from_user.id):
          await bot.send_message(message.from_user.id, f'💸 Партнёрская программа - самый эффективный способ заработать!\n\n🍇 Приглашай друзей и зарабатывай, за каждого друга 0.50₽\n\n🔗 Твоя ссылка для приглашений: https://t.me/{cfg.BOT_NICKNAME}?start={message.from_user.id}')
      else:
          await bot.send_message(message.from_user.id, cfg.NOT_SUB_MSG, reply_markup=Keyboard.keyboard)
    else:
        await message.answer("Ты был заблокирован в боте")

    
    
  
@dp.message_handler(text='💚 Профиль')
async def process_profile_btn(message: types.Message):
  user_id = message.from_user.id
  block = c.execute("SELECT block FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
  if block == 0:
      if await csc.check_sub_channels(cfg.CHANNELS, message.from_user.id):
         user_id = message.from_user.id
         count_referals = c.execute("SELECT COUNT('id') as count FROM users WHERE referrer_id=?", (user_id,)).fetchone()[0]
         balance = c.execute("SELECT balance FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
         await message.answer(f"🆔 ID: {message.from_user.id}\n==========================\n📭 Доступно для вывода: {balance}₽\n👔 Всего рефералов: {count_referals} человек\n==========================", reply_markup=Keyboard.vivod, parse_mode='Markdown')
      else:
         await bot.send_message(message.from_user.id, cfg.NOT_SUB_MSG, reply_markup=Keyboard.keyboard)
  else:
        await message.answer("Ты был заблокирован в боте")
  
  
  
  
@dp.message_handler(text='💨 Информация')
async def process_profile_btn(message: types.Message):
  user_id = message.from_user.id
  block = c.execute("SELECT block FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
  if block == 0:
      if await csc.check_sub_channels(cfg.CHANNELS, message.from_user.id):
          usr_count = c.execute("SELECT COUNT (*) as count FROM users").fetchall()[0][0]
          await message.answer(f'💨 Информация проекта:\n👨‍💻 Пользователей в проекте: {usr_count}\n🕐 Старт бота произведен 20.11.2022', reply_markup=Keyboard.infoya, parse_mode='Markdown')
      else:
          await bot.send_message(message.from_user.id, cfg.NOT_SUB_MSG, reply_markup=Keyboard.keyboard)
  else:
        await message.answer("Ты был заблокирован в боте")
  
  
  
@dp.callback_query_handler(text_contains='vuvud')
async def test(call: types.CallbackQuery, state: FSMContext):
  user_id = call.from_user.id
  balance = c.execute("SELECT balance FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
  if balance >= 2.0:
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.from_user.id, f'Введите сумму для вывода\nУ Вас на балансе: {balance}')
        
    await vuvod.amount.set()
        
  else:
    await bot.send_message(call.from_user.id, 'Минимальная сумма выплаты 2₽')
    


@dp.message_handler(state=vuvod.amount)                                # Как только бот получит ответ, вот это выполнится
async def amount_q1(message: types.Message, state: FSMContext):
  aamm = message.text
  user_id = message.from_user.id
  balance = c.execute("SELECT balance FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
  if balance - (float(aamm)) >= 0:
                await state.update_data(aamount=aamm)
                await message.answer('Введите свой payeer кошелек в формате P123456789:')
                await vuvod.addres.set()
  else:
      await message.answer('Недостаточно средств!')
      await state.finish()


@dp.message_handler(state=vuvod.addres)
async def addres_q2(message: types.Message, state: FSMContext):
  aad = message.text
  await state.update_data(aaddres=aad)
  data = await state.get_data()
  aamount = data.get("aamount")
  aaddres = data.get("aaddres")
  user_id = message.from_user.id
  await bot.send_message(5639323398, f'Юзернейм: @{message.from_user.username}\nАйди: {user_id}\nСумма: {aamount}\nPayeer: {aaddres}', reply_markup=Keyboard.msg_del)
  balance = c.execute("SELECT balance FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
  newblnc = balance - (float(aamount))
  c.execute("UPDATE users SET balance=? WHERE user_id=?", (newblnc, user_id))
  conn.commit()
  await message.answer('Ожидайте, средства поступят на ваши реквезиты в течении 48 часов!')
  await state.finish()
  
  
  
@dp.callback_query_handler(text_contains='msg_d')
async def test_call(callback_query: types.CallbackQuery):
  await callback_query.message.delete()
  

@dp.message_handler(content_types=['text'],text='🔒 Заблокировать пользователя')
async def banusr(message: types.Message):
    user_id = message.from_user.id
    adm = db.adm_or_no(user_id)
    if adm == 1:
        await dialog.blacklist.set()
        await message.answer("Введите id пользователя", reply_markup=Keyboard.back)

@dp.message_handler(state=dialog.blacklist)
async def start_spam(message: types.Message, state: FSMContext):
  if message.text == 'Назад':
    await message.answer("Админ-панель", reply_markup=Keyboard.admin)
    await state.finish()
  else:
      user_id = message.text
      try:
          db.ban(user_id)
          await message.answer("Пользователь заблокирован", reply_markup=Keyboard.admin)
          await state.finish()
      except ValueError:
          await message.answer("Введите айди цифрами", reply_markup=Keyboard.admin)
          await state.finish()
         
@dp.message_handler(content_types=['text'],text='🔓 Разблокировать пользователя')
async def banusr(message: types.Message):
    user_id = message.from_user.id
    adm = db.adm_or_no(user_id)
    if adm == 1:
        await dialog.whitelist.set()
        await message.answer("Введите id пользователя", reply_markup=Keyboard.back)

@dp.message_handler(state=dialog.whitelist)
async def start_spam(message: types.Message, state: FSMContext):
  if message.text == 'Назад':
    await message.answer("Админ-панель", reply_markup=Keyboard.admin)
    await state.finish()
  else:
      user_id = message.text
      try:
          db.unban(user_id)
          await message.answer("Пользователь разблокирован", reply_markup=Keyboard.admin)
          await state.finish()
      except ValueError:
          await message.answer("Введите айди цифрами", reply_markup=Keyboard.admin)
          await state.finish()
          
@dp.message_handler(content_types=['text'],text='Изменить баланс пользователю')
async def setblnc(message: types.Message):
    user_id = message.from_user.id
    adm = db.adm_or_no(user_id)
    if adm == 1:
        await dialog.setbln.set()
        await message.answer("Введите id пользователя", reply_markup=Keyboard.back)
        
@dp.message_handler(state=dialog.setbln)
async def setbbb(message: types.Message, state: FSMContext):
   if message.text == 'Назад':
    await message.answer("Админ-панель", reply_markup=Keyboard.admin)
    await state.finish()
   else:
      answer = message.text
      await state.update_data(user_id=answer)
      await dialog.newbln.set()
      await message.answer("Введите новый баланс для пользователя", reply_markup=Keyboard.back)
        
@dp.message_handler(state=dialog.newbln)
async def nblnc(message: types.Message, state: FSMContext):
  answer = message.text
  await state.update_data(newbalance=answer)
  if message.text == 'Назад':
    await message.answer("Админ-панель", reply_markup=Keyboard.admin)
    await state.finish()
  else:
    data = await state.get_data()
    user_id = data.get("user_id")
    balance = data.get("newbalance")
    try:
        db.setb(balance, user_id)
        await state.finish()
        await message.answer("Выполнено", reply_markup=Keyboard.admin)
    except:
      await state.finish()
      await message.answer("Ошибка!")

#@dp.message_handler()
#async def echo_message(msg: types.Message):
#    await bot.send_message(msg.from_user.id, msg.text)
@dp.message_handler(commands=['gadm'])
async def process_guveadmin_command(message: types.Message):
  admin = message.text[17:]
  user_id = message.text[6:-2]
  c.execute("UPDATE users SET admin = ? WHERE user_id = ?", (admin, user_id,))
  conn.commit()
  await message.answer("Выполнено")
  
  
  
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
