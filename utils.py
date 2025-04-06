import html

async def safe_replace_message(query, *args, **kwargs):
    context = None
    text = None
    reply_markup = None
    parse_mode = "HTML"

    # Support both formats
    if len(args) == 2:  # (context, text)
        context = args[0]
        text = args[1]
    elif len(args) == 1:  # (text only)
        text = args[0]

    if "reply_markup" in kwargs:
        reply_markup = kwargs["reply_markup"]
    if "parse_mode" in kwargs:
        parse_mode = kwargs["parse_mode"]

    try:
        await query.edit_message_text(
            text=html.escape(text),
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    except Exception as e:
        try:
            # Fallback bot
            if context and hasattr(context, "bot"):
                bot = context.bot
            elif hasattr(query, "message") and hasattr(query.message, "chat_id"):
                bot = query._bot  # Safe fallback from telegram.ext
            else:
                raise Exception("Bot instance not found")

            await bot.send_message(
                chat_id=query.message.chat_id,
                text=html.escape(text),
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        except Exception as inner_e:
            print(f"❌ safe_replace_message failed: {inner_e}")
