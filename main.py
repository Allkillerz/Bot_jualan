import telebot  # pastikan sudah install: pip install pyTelegramBotAPI

# Token dari BotFather
BOT_TOKEN = "8431204846:AAF0JscZ7a0m0z_sT_zKiPqBzDX_x5NEzq0"
bot = telebot.TeleBot(BOT_TOKEN)

# Auto reply pesan masuk
@bot.message_handler(func=lambda message: True)
def reply_all(message):
    chat_id = message.chat.id
    text = message.text.lower()

    # Auto-reply berdasarkan keyword
    if "harga" in text:
        reply = "Harga produk kami mulai dari Rp50.000, kak 😊"
    elif "beli" in text:
        reply = "Untuk pembelian, silakan kunjungi link berikut: https://toko-online.com"
    else:
        reply = "Terima kasih sudah menghubungi, kak! Admin akan balas secepatnya ya 🙏"

    bot.send_message(chat_id, reply)

bot.infinity_polling()
