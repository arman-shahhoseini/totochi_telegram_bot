import telebot
from telebot import TeleBot, types
from config import *
import urllib.request

class TotochiBotManager:
    def __init__(self, token, admin_id):
        self.bot = TeleBot(token=token)
        self.admin_id = admin_id
        self.photo_day = None
        self.pay = ''
        self.file_winner = None
        self.setup_handlers()

    def setup_handlers(self):
        self.bot.message_handler(commands=['start'])(self.welcome)
        self.bot.message_handler(func=lambda m: True)(self.bot_pannel)
        self.bot.message_handler(content_types=['photo'])(self.handle_photo)
        self.bot.message_handler(content_types=['document'])(self.handle_document)
        self.bot.callback_query_handler(func=lambda call: True)(self.handle_payment)

    def welcome(self, message):
        self.bot.send_message(message.chat.id, 'با سلام به ربات توتوچی خوش اومدید ❤️ \n\n 💚قبل از انجام هرگونه فعالیتی حتما با استفاده از دکمه (📌قوانین📌) ثبت برگه شرطبندی رو مطالعه کنید تا تجربه دلنشینی داشته باشید', reply_markup=markup)

    def bot_pannel(self, message):
        if message.text == '🟢تهیه اشتراک و ثبت برگه شرطبندی🟢':
            self.bot.send_message(message.chat.id, 'به قسمت ثبت شرطبندی خوش اومدید 🤑\n لطفا قبل هرکاری از قسمت دریافت برگه شرطبندی امروز برگه جدید دریافت کنید و بعد نسبت به ثبت شرطبندی کوشا باشید 🛑\n\n از دستورات زیر استفاده کنید و اول اشتراک تهیه کنید و بعد شرط خود را ثبت نمایید👇🏻', reply_markup=markup_bet)

        elif message.text == '💰تهیه اشتراک برای ثبت برگه شرطبندی💰':
            self.payment_message = self.bot.send_message(message.chat.id, f'برای دریافت اشتراک شما باید مبلغ 200 هزار تومن پرداخت کنید \nمیتونید از روش های زیر استفاده کنید 👇🏻', reply_markup=pay_markup)

        elif message.text == '📝ثبت برگه پیش بینی شما📝':
            if self.pay:
                self.bot.send_message(message.chat.id, 'می توانید عکس برگه شرط بندی خود را ارسال کنید 💯')
            else:
                self.bot.send_message(message.chat.id, '🚫شما هنوز اشتراک خود را تهیه نکردین و نمیتوانید برگه خود را ارسال کنید 🚫\n  ⚠️ اول اشتراک خود را از قسمت (تهیه اشتراک برای ثبت برگه شرطبندی ) تهیه کنید و بعد اقدام به ثبت برگه کنید ⚠️ \n\n (اگر درخواست پرداخت دادین و هنوز تایید نشده صبر کنید لطفا)')

        elif message.text == '📑دریافت برگه شرط بندی امروز📑':
            if self.photo_day is not None:
                self.bot.send_chat_action(message.chat.id, action='upload_photo')
                self.bot.send_photo(message.chat.id, photo=self.photo_day, caption=f'📊برگه {translated_text} \nتا قبل از شروع اولین بازی میتوانید برگه ها را ارسال کنید')
            if self.photo_day is None:
                self.bot.send_message(message.chat.id, 'برگه ای برای ارسال وجود ندارد لطفا صبر کنید تا ادمین بارگزاری کند')

        elif message.text == '📌قوانین📌':
            self.send_rules(message)

        elif message.text == '👤پشتیبانی👤':
            self.bot.send_message(message.chat.id, f'هرگونه سوال یا مشکلی دارید میتونید از راه ارتباطی زیر استفاده کنید \n 👨🏻‍💻{'input id admin'}')

        elif message.text == '👨🏻‍💻پنل مدیریت👨🏻‍💻':
            if message.chat.id == self.admin_id:
                self.bot.send_message(chat_id=self.admin_id, text='به پنل مدیریت خوش اومدی ادمین محترم✅', reply_markup=markup_admin)
            else:
                self.bot.send_message(chat_id=message.chat.id, text='شما قابلیت استفاده از این بخش را ندارید❌')

        elif message.text == '📁اپلود برگه شرطبندی امروز📁':
            self.bot.send_message(message.chat.id, 'عکس برگه شرطبندی امروز را ارسال کنید♻️')

        elif message.text == '❇️دریافت لیست برنده ها❇️':
            if self.file_winner is None:
                self.bot.send_message(chat_id=self.admin_id, text='فایلی برای ارسال وجود ندارد \n برنده ها هنوز مشخص نشده لطفا تا پایان صبر کنید ')
            elif self.file_winner is not None:
                self.bot.send_document(chat_id=self.admin_id, document=self.file_winner, caption=f"لیست برندگان تاریخ : {translated_text}")

        elif message.text == 'بازگشت به صفحه اصلی🔙':
            self.welcome(message)

    def handle_photo(self, message):
        if message.chat.id == self.admin_id:
            self.photo_day = message.photo[-1].file_id
            self.bot.send_message(message.chat.id, text='✅عکس جدید با موفقیت ذخیره شد✅')
        else:
            photo_bet = message.photo[-1].file_id
            if message.from_user.username is not None:
                self.bot.send_photo(chat_id='-1002111705538', photo=photo_bet, caption=f' تاریخ : {translated_text} \nبرگه شرطبندی کاربر : {message.from_user.username}')
                self.bot.send_message(message.chat.id, '✅شرط شما با موفقیت ثبت شد ✅')
            elif message.from_user.username is None:
                self.bot.send_photo(chat_id='-1002111705538', photo=photo_bet, caption=f' تاریخ : {translated_text} \nبرگه شرطبندی کاربر : {message.chat.id} - {message.from_user}')
                self.bot.send_message(message.chat.id, '✅شرط شما با موفقیت ثبت شد ✅')

    def handle_document(self, message):
        if message.chat.id == self.admin_id:
            self.file_winner = message.document.file_id
            self.bot.send_message(chat_id=self.admin_id, text="ثبت شد ")

    def handle_payment(self, call):
        if call.data == 'voucher':
            self.bot.delete_message(chat_id=call.message.chat.id, message_id=self.payment_message.message_id)
            question = self.bot.send_message(call.message.chat.id, text='روش ووچر پرفکت مانی 📮\nشماره ووچر و شماره فعال سازی را بفرستید')
            self.bot.register_next_step_handler(question, self.processed_voucher)

        elif call.data == "processed":
            self.pay = True
            self.bot.send_message(chat_id=self.informatin_user, text=f"کاربر {self.informatin_user} تراکنش تهیه اشتراک شما تایید شد ✅")
            self.bot.edit_message_text(chat_id=self.admin_id, message_id=self.message_v.message_id, text='تراکنش کاربر تایید شد ')

        elif call.data == "unprocessed":
            self.pay = False
            self.bot.send_message(chat_id=self.informatin_user, text=f"کاربر {self.informatin_user} تراکنش تهیه اشتراک شما رد شد ❌")
            self.bot.edit_message_text(chat_id=self.admin_id, message_id=self.message_v.message_id, text='تراکنش کاربر رد شد ')

    def processed_voucher(self, message):
        voucher_code = message.text
        self.informatin_user = message.chat.id
        self.message_v = self.bot.send_message(chat_id=self.admin_id, text=f'کاربر با ایدی عددی : {message.chat.id} \n\n شماره ووچر و کد فعال سازی پرفکت مانی : \n{voucher_code}', reply_markup=proccesed_markup)
        self.bot.delete_message(chat_id=message.chat.id, message_id=question.message_id)
        self.bot.send_message(chat_id=message.chat.id, text='کد ووچر شما با موفقیت به ادمین ارسال شد منتظر تایید باشید⏳💚')

    def send_rules(self, message):
        try:
            image_url = 'https://i.ibb.co/Snbf7wW/photo-2024-04-03-22-48-27.jpg'
            file_path = "image.jpg"
            urllib.request.urlretrieve(image_url, file_path)

            with open(file_path, 'rb') as photo:
                self.bot.send_chat_action(message.chat.id, action='upload_photo')
                self.bot.send_photo(message.chat.id, photo=photo, caption='نمونه برگه ثبت شده لطفا عین این برگه ارسال کنید \n\n 📌 قوانین برگه totochi:\n1️⃣مبلغ ثبت برگه توتوچی ۲۰۰ هزار تومان میباشد\n2️⃣برای ثبت برگه میبایست همه بازی ها را پیشبینی کنید\n3️⃣برای هر بازی فقط یک آپشن را میتوانید انتخاب کنید\n4️⃣بیشترین پیشبینی درست برنده توتوچی ما میباشد\n5️⃣در صورتی که پیشبینی های درست مساوی شود مبلغ بین برندگان تقسیم میشود')
        except Exception as e:
            print(f"Error sending photo: {e}")

    def start_bot(self):
        self.bot.infinity_polling()

# Usage
bot_manager = TotochiBotManager(TOKEN, id_Admin)
bot_manager.start_bot()