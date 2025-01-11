from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# توکن ربات
TOKEN = "7355451408:AAH2PWSDjP44NVmRtpppSauXvffEgqSmAyI"

# مسیر تصویر تعرفه‌ها
TARIFE_IMAGE_PATH = r"C:\Users\admin\Pictures\Screenshots\photo_2025-01-10_23-27-42.jpg"

# مسیر تصویر درباره ما
ABOUT_IMAGE_PATH = r"C:\Users\admin\Desktop\whalenet\photo_2025-01-10_23-29-34.jpg"

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    # لینک کانال تلگرام
    CHANNEL_USERNAME = "WhaleNetChannel"  # نام کاربری کانال بدون @

    user_id = update.effective_user.id

    try:
        # بررسی عضویت کاربر در کانال
        member = await context.bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
    except Exception as e:
        # در صورتی که خطایی پیش بیاید، به معنی این است که کاربر عضو نیست یا ربات دسترسی ندارد
        print(f"Error checking subscription: {e}")

    return False
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # بررسی عضویت کاربر
    is_subscribed = await check_subscription(update, context)
    if not is_subscribed:
        # پیام برای کاربرانی که عضو کانال نیستند
        await update.message.reply_text(
            f"سلام {update.effective_user.first_name} عزیز 🌹\n\n"
            "جهت استفاده از ربات ما باید عضو کانال زیر شوید. لطفا از عضویت خود اطمینان حاصل کنید و مجدداً دکمه /start را بزنید 🙏🏻",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("عضویت در کانال وال‌نت🐋", url="https://t.me/WhaleNetChannel")]]
            ),
        )
        return

    # کد اصلی منوی ربات
    keyboard = [
        [InlineKeyboardButton("خرید کانفیگ جدید 🛒", callback_data="buy_config")],
        [InlineKeyboardButton("تعرفه خرید 🛍", callback_data="pricing")],
        [InlineKeyboardButton("استعلام کانفینگ 🔍", callback_data="inquiry")],
        [InlineKeyboardButton("درخواست پشتیبانی 👨‍💻", callback_data="support")],
        [InlineKeyboardButton("درباره ما 👤", callback_data="about")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            f"سلام {update.effective_user.first_name} عزیز خوش اومدی 🐋\n\n"
            "برای استفاده از خدمات ربات ما، از دکمه‌های زیر استفاده کن 👤",
            reply_markup=reply_markup,
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            text=f"سلام {update.effective_user.first_name} عزیز خوش اومدی 🐋\n\n"
            "برای استفاده از خدمات ربات ما، از دکمه‌های زیر استفاده کن 👤",
            reply_markup=reply_markup,
        )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "buy_config":
        # انتخاب لوکیشن
        keyboard = [
            [InlineKeyboardButton("آلمان 🇩🇪", callback_data="location_germany")],
            [InlineKeyboardButton("برگشت به منوی اصلی↪️", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🌐 لوکیشن مورد نظر خود را انتخاب کنید:",
            reply_markup=reply_markup,
        )

    elif data == "location_germany":
        # انتخاب بازه زمانی
        keyboard = [
            [InlineKeyboardButton("یک ماهه", callback_data="duration_month")],
            [InlineKeyboardButton("برگشت به منوی اصلی↪️", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🔰برای نمایش لیست سرویس های وال‌نت یکی از گزینه های زیر را انتخاب کنید:",
            reply_markup=reply_markup,
        )

    elif data == "duration_month":
        # نمایش لیست قیمت
        keyboard = [
            [InlineKeyboardButton("یک ماهه - 10 گیگابایت - 40,000 تومان", callback_data="package_10gb")],
            [InlineKeyboardButton("یک ماهه - 20 گیگابایت - 57,000 تومان", callback_data="package_20gb")],
            [InlineKeyboardButton("یک ماهه - 30 گیگابایت - 72,000 تومان", callback_data="package_30gb")],
            [InlineKeyboardButton("یک ماهه - 50 گیگابایت - 106,000 تومان", callback_data="package_50gb")],
            [InlineKeyboardButton("یک ماهه - 100 گیگابایت - 182,000 تومان", callback_data="package_100gb")],
            [InlineKeyboardButton("یک ماهه - 250 گیگابایت - 398,000 تومان", callback_data="package_250gb")],
            [InlineKeyboardButton("برگشت به منوی اصلی↪️", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="حالا برای خرید کانفیگ جدید یکی از گزینه های زیر را انتخاب کنید تا جزئیات سرویس به شما داده شود 🐋",
            reply_markup=reply_markup,
        )

    elif data.startswith("package_"):
        # نمایش جزئیات بسته
        packages = {
            "package_10gb": ("10 گیگابایت", "40,000"),
            "package_20gb": ("20 گیگابایت", "57,000"),
            "package_30gb": ("30 گیگابایت", "72,000"),
            "package_50gb": ("50 گیگابایت", "106,000"),
            "package_100gb": ("100 گیگابایت", "182,000"),
            "package_250gb": ("250 گیگابایت", "398,000"),
        }
        package_name, price = packages[data]
        text = f"🔸یک ماهه {package_name}\n💰قیمت : {price} تومان \n🌐 سرور آلمان 🇩🇪\n📃 توضیحات :\n🔻این سرویس بدون محدودیت کاربر است."
        keyboard = [
            [InlineKeyboardButton("خرید و پرداخت 💳", callback_data=f"buy_{data}")],
            [InlineKeyboardButton("برگشت به منوی اصلی↪️", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
        )

    elif data == "pricing":
        # نمایش تعرفه خرید به همراه عکس
        text = (
            "🛍 تعرفه سرویس‌های وال‌نت به شرح زیر است:\n\n"
            "یک ماهه 10 گیگابایت - 40,000 تومان\n"
            "یک ماهه 20 گیگابایت - 57,000 تومان\n"
            "یک ماهه 30 گیگابایت - 72,000 تومان\n"
            "یک ماهه 50 گیگابایت - 106,000 تومان\n"
            "یک ماهه 100 گیگابایت - 182,000 تومان\n"
            "یک ماهه 250 گیگابایت - 398,000 تومان\n\n"
            "- تمامی سرویس‌های وال‌نت بدون محدودیت کاربر هستند و نیازی به پرداخت اضافه نیست!\n"
            "- سرویس‌های وال‌نت تا پایان مدت زمان سرور شما پشتیبانی می‌شوند.\n\n"
            "- @WhaleNet_Bot"
        )
        keyboard = [
            [InlineKeyboardButton("برگشت به منوی اصلی↪️", callback_data="remove_pricing_message")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        with open(TARIFE_IMAGE_PATH, "rb") as photo:
            sent_message = await query.message.reply_photo(photo=photo, caption=text, reply_markup=reply_markup)
            context.user_data["pricing_message_id"] = sent_message.message_id

    elif data == "about":
        # نمایش درباره ما به همراه عکس
        about_text = (
            "👨🏻‍💻ما در فروشگاه وال‌نت متعهد هستیم تا بهترین خدمات دسترسی به اینترنت جهانی را با قیمتی منصفانه و کیفیتی بی‌نظیر ارائه دهیم. "
            "هدف اصلی ما این است که کاربرانمان بتوانند بدون هیچ محدودیتی از اینترنت آزاد استفاده کنند و تجربه‌ای روان و مطمئن از ارتباطات دیجیتال داشته باشند. "
            "تیم وال‌نت همواره در تلاش است تا با بهره‌گیری از جدیدترین تکنولوژی‌ها، نیازهای کاربران را برآورده کند و دسترسی به اینترنت را برای همه آسان‌تر کند.\n\n"
            "امنیت و حریم خصوصی کاربران برای ما در اولویت است. تمامی خدمات ما با استفاده از پروتکل‌های پیشرفته رمزنگاری ارائه می‌شوند تا اطلاعات شما در برابر هرگونه خطر محافظت شود. "
            "شما می‌توانید با اطمینان خاطر به اینترنت متصل شوید و بدانید که تمامی داده‌های شما در امنیت کامل قرار دارند. "
            "تیم پشتیبانی ما نیز همیشه آماده است تا در صورت بروز هرگونه مشکل، در سریع‌ترین زمان ممکن به شما کمک کند.\n\n"
            "- @WhaleNet_Bot"
        )
        keyboard = [
            [InlineKeyboardButton("برگشت به منوی اصلی↪️", callback_data="remove_about_message")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        with open(ABOUT_IMAGE_PATH, "rb") as photo:
            sent_message = await query.message.reply_photo(photo=photo, caption=about_text, reply_markup=reply_markup)
            context.user_data["about_message_id"] = sent_message.message_id

    elif data == "support":
        # بخش درخواست پشتیبانی
        text = (
            "👨🏻‍💻جهت ارتباط با پشتیبانی وال‌نت می‌توانید به پیوی پشتیبانی که در زیر قرار داده شده است مراجعه کنید.\n\n"
            "‼️در صورت ریپورت بودن میتوانید از دکمه‌ی دوم استفاده کنید، پس از زدن این دکمه هر پیامی در ربات وارد کنید برای پشتیبانی ارسال خواهد شد.\n\n"
            "- لطفا از ارسال پیام های خالی و یا بی‌مورد خودداری فرمایید.\n"
            "- سرعت پاسخگویی پشتیبانی، بستگی به شلوغی ربات دارد.\n"
            "- جهت گزارش قطعی سرور و یا درخواست تعویض لینک کانفینگ، می‌توانید به پشتیبانی مراجعه کنید."
        )
        keyboard = [
            [InlineKeyboardButton("ارتباط مستقیم با پشتیبانی 👨🏻‍💻", url="https://t.me/whale_net")],
            [InlineKeyboardButton("ارسال پیام به پشتیبانی در ربات ☎️", url="https://t.me/whalenetmessengerbot")],
            [InlineKeyboardButton("برگشت به منوی اصلی↪️", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
        )

    elif data == "remove_about_message":
        # حذف پیام درباره ما به همراه عکس
        about_message_id = context.user_data.get("about_message_id")
        if about_message_id:
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=about_message_id)
            del context.user_data["about_message_id"]

    elif data == "remove_pricing_message":
        # حذف پیام تعرفه خرید به همراه عکس
        pricing_message_id = context.user_data.get("pricing_message_id")
        if pricing_message_id:
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=pricing_message_id)
            del context.user_data["pricing_message_id"]

    elif data == "inquiry":
        # پیام شیشه‌ای برای استعلام کانفینگ
        text = (
            "جهت استعلام کانفینگ، به آدرس زیر مراجعه کنید و لینک کانفینگ خود را قرار دهید 🔍\n\n"
            "🔗 https://chservice.info"
        )
        keyboard = [
            [InlineKeyboardButton("برگشت به منوی اصلی↪️", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
        )

    elif data.startswith("buy_package_"):
        # نمایش اطلاعات پرداخت
        price_map = {
            "buy_package_10gb": "40,000",
            "buy_package_20gb": "57,000",
            "buy_package_30gb": "72,000",
            "buy_package_50gb": "106,000",
            "buy_package_100gb": "182,000",
            "buy_package_250gb": "398,000",
        }
        price = price_map[data]
        text = f"جهت واریز {price} تومان و خرید این کانفینگ از طریق یکی از راه های زیر اقدام نموده و منتظر دریافت شماره کارت از سوی پشتیبانی وال‌نت باشید.👨🏻‍💻\n\n‼️ درصورتی که ریپورت بودید و امکان ارتباط مستقیم با پشتیبانی وجود نداشت از طریق ربات پیامرسان با پشتیبانی ارتباط برقرار کنید.\n- زمان پاسخگویی در دو حالت یکسان است و بستگی به میزان شلوغی دارد."
        keyboard = [
            [InlineKeyboardButton("پیوی پشتیبانی وال‌نت👥", url="https://t.me/whale_net")],
            [InlineKeyboardButton("ربات پیامرسان وال‌نت🤖", url="https://t.me/whalenetmessengerbot")],
            [InlineKeyboardButton("برگشت به منوی اصلی↪️", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
        )

    elif data == "main_menu":
        await start(update, context)

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.run_polling()

if __name__ == "__main__":
    main()