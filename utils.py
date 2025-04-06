import html
from telegram import InlineKeyboardMarkup

async def safe_replace_message(query, context, text, reply_markup=None, parse_mode="HTML"):
    try:
        await query.edit_message_text(
            text=html.escape(text),
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    except Exception as e:
        try:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=html.escape(text),
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        except Exception as inner_e:
            print(f"❌ safe_replace_message failed: {inner_e}")
