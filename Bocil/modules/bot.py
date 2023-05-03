import asyncio
import importlib
from datetime import datetime, timedelta

import pytz
from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Bocil import CMD_HELP, app, bot
from Bocil.config import HANDLER as cmd
from Bocil.config import *
from Bocil.helpers.SQL.ubot_sql import *
from Bocil.modules import ALL_MODULES
from Bocil.utils.inline import paginate_help
from Bocil.utils.misc import extract_user

msg = "**Help Menu Open\nPrefix : **" f"`. ^ + - , ; ! ?`"


@app.on_inline_query(filters.regex("help"))
async def _(client, inline_query):
    bttn = paginate_help(0, CMD_HELP, "helpme")
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    thumb_url="https://telegra.ph//file/deaf5d4f775190f8ce461.jpg",
                    title="Help Menu!",
                    reply_markup=InlineKeyboardMarkup(bttn),
                    input_message_content=InputTextMessageContent(msg),
                )
            )
        ],
    )


@app.on_callback_query(filters.regex("helpme_prev\((.+?)\)"))
async def on_plug_prev_in_cb(_, callback_query: CallbackQuery):
    current_page_number = int(callback_query.matches[0].group(1))
    buttons = paginate_help(current_page_number - 1, CMD_HELP, "helpme")
    await callback_query.edit_message_text(
        msg,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("helpme_next\((.+?)\)"))
async def on_plug_next_in_cb(_, callback_query: CallbackQuery):
    current_page_number = int(callback_query.matches[0].group(1))
    buttons = paginate_help(current_page_number + 1, CMD_HELP, "helpme")
    await callback_query.edit_message_text(
        msg,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("ub_modul_(.*)"))
async def on_plug_in_cb(_, callback_query: CallbackQuery):
    modul_name = callback_query.matches[0].group(1)
    commands: dict = CMD_HELP[modul_name]
    this_command = f"──「 **Help For {str(modul_name).upper()}** 」──\n\n"
    for x in commands:
        this_command += (
            f"  •  **Command:** `.{str(x)}`\n  •  **Function:** {str(commands[x])}\n\n"
        )
    this_command += "© Bocil-Userbot"
    bttn = [
        [InlineKeyboardButton(text="• Kembali •", callback_data="reopen")],
    ]
    await callback_query.edit_message_text(
        this_command,
        reply_markup=InlineKeyboardMarkup(bttn),
    )


@app.on_callback_query(filters.regex("reopen"))
async def reopen_in_cb(_, callback_query: CallbackQuery):
    buttons = paginate_help(0, CMD_HELP, "helpme")
    await callback_query.edit_message_text(
        msg,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("add_ubot"))
async def _(_, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in MEMBERS and user_id not in ADMIN:
        for X in ADMIN:
            await app.resolve_peer(X)
        buttons = InlineKeyboard(row_width=3)
        keyboard: List[InlineKeyboardButton] = []
        for i in range(min(len(ADMIN), len(ADMIN))):
            list_admin = f"👮🏼 Admin {i}"
            id_admin = ADMIN[i]
            keyboard.append(
                InlineKeyboardButton(
                    list_admin,
                    user_id=id_admin,
                )
            )
        buttons.add(*keyboard)
        return await app.send_message(
            user_id,
            f"**{callback_query.from_user.mention} silahkan hubungin salah satu admin untuk mendapat akses membuat userbot**",
            disable_web_page_preview=True,
            reply_markup=buttons,
        )
    buat = [
        [
            InlineKeyboardButton("🔥 Buat Userbot 🔥", callback_data="add_ubot"),
        ]
    ]
    await callback_query.message.delete()
    api_id_msg = await app.ask(
        user_id, "**Tolong berikan saya API_ID**", filters=filters.text
    )
    if await is_cancel(callback_query, api_id_msg.text):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "Bukan API_ID yang valid (yang harus bilangan bulat). Silakan ulang kembali",
            quote=True,
            reply_markup=InlineKeyboardMarkup(buat),
        )
        return
    api_hash_msg = await app.ask(
        user_id, "**Tolong berikan saya API_HASH**", filters=filters.text
    )
    if await is_cancel(callback_query, api_hash_msg.text):
        return
    api_hash = api_hash_msg.text
    try:
        phone = await app.ask(
            user_id,
            (
                "**Silahkan Masukkan Nomor Telepon Telegram Anda Dengan Format Kode Negara.\nContoh: +628xxxxxxx**\n"
                "\n**Gunakan /cancel untuk Membatalkan Proses Membuat Userbot**"
            ),
            timeout=300,
        )

    except asyncio.TimeoutError:
        return await message.reply_text(
            "Batas waktu tercapai 5 menit. Proses Dibatalkan.",
            reply_markup=InlineKeyboardMarkup(buat),
        )
    if await is_cancel(callback_query, phone.text):
        return
    phone_number = phone.text
    new_client = Ubot(
        name=str(callback_query.id),
        api_id=api_id,
        api_hash=api_hash,
        in_memory=True,
    )
    await new_client.connect()
    try:
        code = await new_client.send_code(phone_number.strip())
    except Exception:
        code = await new_client.resend_code(
            phone_number.strip(), SentCodeType.EMAIL_CODE
        )
    except PhoneNumberInvalid:
        return await app.send_message(
            user_id,
            "Nomor telepon tidak valid, silakan coba lagi",
            reply_markup=InlineKeyboardMarkup(buat),
        )
    except PhoneNumberBanned:
        return await app.send_message(
            user_id, "Nomor telepon diblokir", reply_markup=InlineKeyboardMarkup(buat)
        )
    except PhoneNumberFlood:
        return await app.send_message(
            user_id,
            "Nomor telepon terkena spam, harap menunggu",
            reply_markup=InlineKeyboardMarkup(buat),
        )
    except PhoneNumberUnoccupied:
        return await app.send_message(
            user_id, "Nomor tidak terdaftar", reply_markup=InlineKeyboardMarkup(buat)
        )
    except BadRequest as error:
        return await app.send_message(
            user_id,
            f"Terjadi kesalahan yang tidak diketahui: {error}",
            reply_markup=InlineKeyboardMarkup(buat),
        )

    try:
        otp = await app.ask(
            user_id,
            (
                "**Silakan Periksa Kode OTP dari <a href=tg://openmessage?user_id=777000>Akun Telegram</a> Resmi. Kirim Kode OTP ke sini setelah membaca Format di bawah ini.**\n"
                "\nJika Kode OTP adalah `12345` Tolong **[ TAMBAHKAN SPASI ]** kirimkan Seperti ini `1 2 3 4 5`\n"
                "\n__Jika code tidak muncul silahkan cek email kamu__"
                "\n**Gunakan /cancel untuk Membatalkan Proses Membuat Userbot**"
            ),
            timeout=300,
        )

    except asyncio.TimeoutError:
        return await app.send_message(
            user_id,
            "Batas waktu tercapai 5 menit. Proses Dibatalkan.",
            reply_markup=InlineKeyboardMarkup(buat),
        )
    if await is_cancel(callback_query, otp.text):
        return
    otp_code = otp.text
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except PhoneCodeInvalid:
        return await app.send_message(
            user_id,
            "Kode yang Anda kirim tampaknya Tidak Valid, Coba lagi.",
            reply_markup=InlineKeyboardMarkup(buat),
        )
    except PhoneCodeExpired:
        return await app.send_message(
            user_id,
            "Kode yang Anda kirim tampaknya Kedaluwarsa. Coba lagi.",
            reply_markup=InlineKeyboardMarkup(buat),
        )
    except BadRequest as error:
        return await app.send_message(
            user_id,
            f"Terjadi kesalahan yang tidak diketahui: {error}",
            reply_markup=InlineKeyboardMarkup(buat),
        )
    except SessionPasswordNeeded:
        try:
            two_step_code = await app.ask(
                user_id,
                "**Akun anda Telah mengaktifkan Verifikasi Dua Langkah. Silahkan Kirimkan Passwordnya.\n\nGunakan /cancel untuk Membatalkan Proses Membuat Userbot**",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await app.send_message(
                user_id,
                "Batas waktu tercapai 5 menit.",
                reply_markup=InlineKeyboardMarkup(buat),
            )
        if await is_cancel(callback_query, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
        except BadRequest:
            return await app.send_message(
                user_id,
                "Kata sandi salah, coba lagi",
                reply_markup=InlineKeyboardMarkup(buat),
            )
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False
    await new_client.start()
    add_ubot(
        user_id=int(new_client.me.id),
        api_id=api_id,
        api_hash=api_hash,
        session_string=session_string,
    )
    for mod in ALL_MODULES:
        importlib.reload(importlib.import_module(f"Bocil.modules.{mod}"))

    now = datetime.now(pytz.timezone("Asia/Jakarta"))
    waktu = now.strftime("%w %d %m %Y %H:%M:%S").split()
    text_done = f"**🔥 {app.me.mention} Berhasil Diaktifkan Di Akun: <a href=tg://openmessage?user_id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> > `{new_client.me.id}`**\nTanggal : {waktu[1]}/{waktu[2]}/{waktu[3]}\nJam : {waktu[4]}"
    await app.send_message(
        user_id,
        text_done
        + "\nSilahkan ketik .ping untuk cek userbot apakah sudah aktif apa belum",
        disable_web_page_preview=True,
    )
    ID_MAKER_UBOT = callback_query.from_user.id
    buttons = [
        [
            InlineKeyboardButton(
                "🧑‍💻 Pembuat Userbot 🧑‍💻",
                url=f"tg://openmessage?user_id={ID_MAKER_UBOT}",
            )
        ]
    ]
    await app.send_message(
        BOTLOG_CHATID,
        text_done,
        disable_web_page_preview=True,
    )


@app.on_callback_query(filters.regex("get_ubot"))
async def _(_, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in OWNER_ID:
        return
    await callback_query.message.delete()
    for ub in bot._ubot:
        list_ubot = f"🤖 ROBOT: {app.me.mention}\n\n"
        if ub.me.id == bot.me.id:
            list_ubot += f"**👤 USERBOT UTAMA: {ub.me.mention}**\n"
        else:
            habis = get_habis(ub.me.id)
            if habis is not None:
                for i in habis:
                    waktunya = i.habis
            list_ubot += f"**👤 USERBOT: {ub.me.mention}**\n\nHabis: {waktunya}"
        msg_list_ubot = await app.send_message(
            user_id,
            list_ubot,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📁 Hapus Dari Database 📁",
                            callback_data=f"del_ubot {ub.me.id}",
                        )
                    ]
                ]
            ),
            disable_web_page_preview=True,
        )
        await asyncio.sleep(1)


@app.on_callback_query(filters.regex("del_ubot"))
async def _(_, callback_query):
    user_id = callback_query.from_user.id
    del_id = callback_query.data.split()[1]
    if user_id not in OWNER_ID:
        return
    try:
        user = await app.get_users(del_id)
        await callback_query.message.delete()
        await app.send_message(
            user_id, f"** ✅ {user.mention} Berhasil Dihapus Dari Database**"
        )
        await app.send_message(
            user.id,
            "**Peringatan**‼️\n\nMasa aktif userbot anda telah habis silahkan hubungi admin untuk mengaktifkan kembali\nUntuk informasi lebih lanjut kontak kami di @Pantekyks",
        )
        remove_ubot(user.id)
    except BadRequest:
        await callback_query.message.delete()
        await app.send_message(
            user_id,
            f"** ✅ {del_id} Berhasil Dihapus Dari Database**",
        )
        await app.send_message(
            user.id,
            "**Peringatan**‼️\n\nMasa aktif userbot anda telah habis silahkan hubungi admin untuk mengaktifkan kembali\nUntuk informasi lebih lanjut kontak kami di @Pantekyks",
        )
        remove_ubot(int(del_id))


async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        await app.send_message(callback_query.from_user.id, "**Membatalkan Proses!**")
        return True
    return False


@bot.on_message(filters.command("prem", cmd) & filters.me)
async def add_members(c, m):
    if m.from_user.id not in ADMIN:
        return
    args = await extract_user(m)
    reply = m.reply_to_message
    ex = await m.reply("Processing...")
    if args:
        try:
            user = await c.get_users(args)
        except Exception:
            await ex.edit(f"__User tidak ditemukan__")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await c.get_users(user_id)
    else:
        await ex.edit(f"User tidak di temukan")
        return

    try:
        if user.id in MEMBERS:
            return await ex.edit("__User sudah menjadi member__")
        MEMBERS.append(user.id)
        await ex.edit(f"{user.mention} ditambahkan ke members")

    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")
        return


@bot.on_message(filters.command("unprem", cmd) & filters.me)
async def del_members(c, m):
    if m.from_user.id not in ADMIN:
        return
    args = await extract_user(m)
    reply = m.reply_to_message
    ex = await m.reply_text("Processing...")
    if args:
        try:
            user = await c.get_users(args)
        except Exception:
            await ex.edit(f"User tidak di temukan")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await c.get_users(user_id)
    else:
        await ex.edit(f"User tidak di temukan")
        return
    try:
        if user.id not in MEMBERS:
            return await ex.edit("__User bukan bagian dari members**")
        MEMBERS.remove(user.id)
        await ex.edit(f"{user.mention} Sudah dihapus dari members")

    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")
        return


@app.on_message(filters.command("active"))
async def active_members(c, m):
    if m.from_user.id not in ADMIN and m.from_user.id not in OWNER_ID:
        return
    if len(m.command) < 3:
        return await m.reply("format ?active id hari\ncontoh ?active 165366 30")
    user_id = m.command[1]
    time = m.command[2]
    now = datetime.now(pytz.timezone("Asia/Jakarta"))
    hab = now + timedelta(int(time))
    waktu = now.strftime("%w %d %m %Y %H:%M:%S").split()
    habisx = hab.strftime("%w %d %m %Y %H:%M:%S").split()
    waktu_awal = f"{waktu[1]}-{waktu[2]}-{waktu[3]}"
    waktu_habis = f"{habisx[1]}-{habisx[2]}-{habisx[3]}"
    try:
        mem = await c.get_users(int(user_id))
        memb = f"{mem.mention} {mem.id}"
    except:
        memb = int(user_id)
    save_habis(int(user_id), waktu_habis)
    anu = await m.reply(
        f"**Waktu Userbot**\n\n**Waktu Mulai :**\n{waktu_awal}\n**Waktu Habis :**\n{waktu_habis}\n**Pembuat :**\n{m.from_user.mention}\n**Member :**\n{memb}"
    )


@app.on_message(filters.command("start") & filters.private)
async def start_bot(c, m):
    buat = [
        [
            InlineKeyboardButton("🔥 Buat Userbot 🔥", callback_data="add_ubot"),
        ]
    ]
    but = [
        [
            InlineKeyboardButton("🔥 Buat Userbot 🔥", callback_data="add_ubot"),
            InlineKeyboardButton("💡 Daftar Userbot 💡", callback_data="get_ubot"),
        ]
    ]

    if m.from_user.id not in OWNER_ID:
        await m.reply(
            "Selamat datang di Bocil Userbot\nGunakan tombol di bawah jika ingin membuat userbot",
            reply_markup=InlineKeyboardMarkup(buat),
        )
    else:
        await m.reply(
            "Selamat datang di Bocil Userbot\nGunakan tombol di bawah jika ingin membuat userbot",
            reply_markup=InlineKeyboardMarkup(but),
        )
