import datetime
import psycopg2
from db import connect_db

def check_daily_limit(user_id: int) -> bool:
    today = datetime.date.today()
    conn = connect_db()
    if not conn:
        print("❌ DB connection failed.")
        return False

    try:
        cur = conn.cursor()
        cur.execute("SELECT is_premium, usage_count, last_used_date FROM users WHERE user_id = %s", (user_id,))
        result = cur.fetchone()

        if not result:
            print("❌ User not found in DB.")
            return False

        is_premium, usage_count, last_used = result

        if is_premium:
            return True  # Unlimited for premium

        if last_used == today:
            if usage_count >= 10:
                return False
            else:
                cur.execute("""
                    UPDATE users 
                    SET usage_count = usage_count + 1 
                    WHERE user_id = %s
                """, (user_id,))
        else:
            cur.execute("""
                UPDATE users 
                SET usage_count = 1, last_used_date = %s 
                WHERE user_id = %s
            """, (today, user_id))

        conn.commit()
        return True

    except Exception as e:
        print(f"❌ Error checking daily limit: {e}")
        return False

    finally:
        conn.close()




async def safe_replace_message(query, context, text, reply_markup=None, parse_mode="Markdown"):
    try:
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    except Exception as e:
        try:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        except Exception as inner_e:
            print(f"❌ safe_replace_message failed: {inner_e}")
