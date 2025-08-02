import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8431204846:AAF0JscZ7a0m0z_sT_zKiPqBzDX_x5NEzq0"  # Ganti dengan token asli dari BotFather
ADMIN_USERNAME = "@RyuDigitall"  # Admin tujuan

bot = telebot.TeleBot(BOT_TOKEN)

# Produk list
produk = {
    "1": {"nama": "Xtra Combo S + XUTS (pulsa 25k)", "harga": "Rp 10.000"},
    "2": {"nama": "Xtra Combo S + XUTP (pulsa 25k)", "harga": "Rp 10.000"},
    "3": {"nama": "XC 1GB + XUTS (pulsa 12.5k)", "harga": "Rp 10.000"},
    "4": {"nama": "XC 1GB + XUTS (tanpa pulsa)", "harga": "Rp 23.000"},
    "5": {"nama": "Xtra Combo S + XUTS (tanpa pulsa)", "harga": "Rp 35.000"},
    "6": {"nama": "Xtra Combo S + XUTP (tanpa pulsa)", "harga": "Rp 35.000"},
    "7": {"nama": "Xtra Combo S + Full Add-on Combo", "harga": "Rp 40.000"},
    "8": {"nama": "XL Vidio (pulsa 25k)", "harga": "Rp 8.000"},
    "9": {"nama": "XL Vidio (tanpa pulsa)", "harga": "Rp 33.000"},
    "10": {"nama": "XL Iflix (pulsa 25k)", "harga": "Rp 8.000"},
    "11": {"nama": "XL Iflix (tanpa pulsa)", "harga": "Rp 33.000"},
}

# Simpan pesanan user sementara
pesanan_user = {}

# Start command
@bot.message_handler(commands=['start'])
def kirim_menu(message):
    markup = InlineKeyboardMarkup(row_width=1)
    for kode, item in produk.items():
        tombol = InlineKeyboardButton(f"{item['nama']} - {item['harga']}", callback_data=kode)
        markup.add(tombol)
    bot.send_message(message.chat.id, "📦 *Katalog Produk XL*\nPilih produk di bawah ini:", reply_markup=markup, parse_mode="Markdown")

# Saat user pilih produk
@bot.callback_query_handler(func=lambda call: True)
def proses_produk(call):
    user_id = call.message.chat.id
    kode = call.data
    item = produk.get(kode)
    if item:
        pesanan_user[user_id] = item  # Simpan sementara
        bot.send_message(user_id, f"📝 Kamu memilih:\n*{item['nama']}*\n💰 Harga: *{item['harga']}*\n\nSilakan ketik *Nomor XL Tujuan* kamu:", parse_mode="Markdown")
        bot.register_next_step_handler_by_chat_id(user_id, input_nomor)

# Input nomor HP
def input_nomor(message):
    user_id = message.chat.id
    nomor = message.text.strip()
    item = pesanan_user.get(user_id)

    if not item:
        bot.send_message(user_id, "❌ Tidak ada pesanan aktif. Ketik /start untuk ulang.")
        return

    # Kirim ringkasan
    teks = (
        f"🛒 *Pesanan Kamu:*\n"
        f"📦 Produk: *{item['nama']}*\n"
        f"💰 Harga: *{item['harga']}*\n"
        f"📱 Nomor XL: `{nomor}`\n\n"
        f"Silakan transfer ke:\n"
        "`1234567890 (BCA a.n. RyuStore)`\n"
        "_Setelah transfer, kirim bukti ke admin._\n\n"
        f"📩 Admin: {ADMIN_USERNAME}"
    )

    bot.send_message(user_id, teks, parse_mode="Markdown")

    # Forward ke admin
    forward = (
        f"📥 *Pesanan Baru*\n"
        f"👤 Dari: @{message.from_user.username or '-'}\n"
        f"📦 Produk: *{item['nama']}*\n"
        f"💰 Harga: *{item['harga']}*\n"
        f"📱 Nomor XL: `{nomor}`"
    )
    bot.send_message(user_id, "✅ Pesanan berhasil dicatat & dikirim ke admin.")
    bot.send_message(user_id, "Terima kasih telah order di RyuDigital Store 🙏")

    # Kirim ke admin
    bot.send_message(user_id=message.chat.id, text="📤 Forwarding ke admin...")
    bot.send_message(chat_id=user_id, text="🕒 Tunggu konfirmasi dari admin ya...")

    # Kirim ke admin real
    bot.send_message(chat_id=user_id, text=forward, parse_mode="Markdown")

# Run bot
print("Bot aktif...")
bot.polling(none_stop=True, interval=1, timeout=30)