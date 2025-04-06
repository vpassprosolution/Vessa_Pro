import html

async def safe_replace_message(query, *args, **kwargs):
    # Extract params
    context = None
    text = None
    reply_markup = None
    parse_mode = "HTML"

    if len(args) == 2:  # Old version: (query, context, text, reply_markup)
        context = args[0]
        text = args[1]
    elif len(args) == 1:  # New version: (query, text)
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
            # Use context if exists, else fallback to query.message.bot
            bot = context.bot if context else query.message.bot
            await bot.send_message(
                chat_id=query.message.chat_id,
                text=html.escape(text),
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        except Exception as inner_e:
            print(f"❌ safe_replace_message failed: {inner_e}")
