async def safe_replace_message(query, context, text, reply_markup=None, parse_mode="Markdown"):
    try:
        if hasattr(query, "message") and query.message:
            await query.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        else:
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
    except Exception as e:
        print(f"❌ safe_replace_message failed: {e}")
