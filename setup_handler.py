from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# ⚙️ SETUP MENU
async def setup_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("🌐 Language", callback_data="language_menu"),
            InlineKeyboardButton("🎓 Tutorial", callback_data="coming_soon")
        ],
        [
            InlineKeyboardButton("💬 Live Chat", callback_data="live_chat"),
            InlineKeyboardButton("🛠️ Support", callback_data="support_info")  # ✅ Updated to callback
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]

    await query.message.edit_text(
        "⚙️  CHOOSE YOUR SETUP MENU  ⚙️",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 🚧 COMING SOON
async def coming_soon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.edit_text(
        "🚧 This feature is coming soon!",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="setup_menu")]])
    )


# ✅ SUPPORT INFO
async def support_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "🛠️ *VESSA PRO SUPPORT*\n\n"
        "If you’re facing any issue, we’re here to help you.\n\n"
        "📩 You can email us directly:\n"
        "*support@vessapro.com*\n\n"
        "🧠 Please describe your issue in detail so our team can assist you better."
    )

    keyboard = [
        [InlineKeyboardButton("✉️ Email Support", url="mailto:support@vessapro.com")],
        [InlineKeyboardButton("🔙 Back", callback_data="setup_menu")]
    ]

    await query.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
