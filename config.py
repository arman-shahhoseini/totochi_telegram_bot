import datetime
import pytz
from googletrans import Translator
import urllib.request
from telebot import types

TOKEN = 'input your telegram bot token' 
id_Admin = "input Numerical ID admin in telegram (get your Numerical ID from thats bot https://t.me/userinfobot)"


first_key = types.KeyboardButton('🟢تهیه اشتراک و ثبت برگه شرطبندی🟢')
second_key = types.KeyboardButton('📑دریافت برگه شرط بندی امروز📑')
third_key = types.KeyboardButton('📌قوانین📌')
fourth_key = types.KeyboardButton('👤پشتیبانی👤')
fifth_key = types.KeyboardButton('👨🏻‍💻پنل مدیریت👨🏻‍💻')
markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup.add(first_key)
markup.row(second_key, third_key)
markup.row(fourth_key, fifth_key)

def get_persian_date():
    tz = pytz.timezone('Asia/Tehran')
    now = datetime.datetime.now(tz)
    persian_date = now.strftime('%A %Y/%m/%d')
    return persian_date

def translate_text(text, dest_lang):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    return translation.text

translated_text = translate_text(get_persian_date(), "fa")

key1 = types.KeyboardButton('📁اپلود برگه شرطبندی امروز📁')
key2 = types.KeyboardButton('❇️دریافت لیست برنده ها❇️')
key3 = types.KeyboardButton('بازگشت به صفحه اصلی🔙')
markup_admin = types.ReplyKeyboardMarkup(resize_keyboard=True , row_width=1)
markup_admin.add(key1 , key2 , key3)


key_1 = types.KeyboardButton('💰تهیه اشتراک برای ثبت برگه شرطبندی💰')
key_2 = types.KeyboardButton('📝ثبت برگه پیش بینی شما📝')
key_3 = types.KeyboardButton('بازگشت به صفحه اصلی🔙')
markup_bet = types.ReplyKeyboardMarkup(resize_keyboard=True , row_width=1)
markup_bet.add(key_1, key_2 , key_3)



voucher = types.InlineKeyboardButton('ووچر پرفکت مانی', callback_data="voucher")
pay_markup = types.InlineKeyboardMarkup(row_width=1)
pay_markup.add( voucher)


proccesed_key = types.InlineKeyboardButton('تایید تراکنش 🟢' , callback_data="processed")
unproccesed_key = types.InlineKeyboardButton('رد تراکنش 🔴' , callback_data="unprocessed")
proccesed_markup = types.InlineKeyboardMarkup(row_width=1)
proccesed_markup.add(proccesed_key , unproccesed_key)
