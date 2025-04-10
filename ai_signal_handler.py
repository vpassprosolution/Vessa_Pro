import httpx
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler
import asyncio
from language_handler import get_text
from utils import check_daily_limit

AI_API_URL = "https://aiagentinstantsignal-production.up.railway.app"

# Cooldown reset
async def reset_cooldown(context):
    await asyncio.sleep(1.5)
    context.user_data["cooldown"] = False

# ✅ Function to fetch trade signal from the AI API
async def fetch_ai_signal(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if context.user_data.get("cooldown"):
        return
    context.user_data["cooldown"] = True
    asyncio.create_task(reset_cooldown(context))

    user_id = query.from_user.id
    get = lambda key: get_text(user_id, key, context)

    # ✅ Check Daily Limit
    if not check_daily_limit(user_id):
        await query.message.edit_text(
            "🚫 You’ve reached your *daily limit* of 10 signals.\n\n💎 Upgrade to *Premium* for unlimited access.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get("btn_back"), callback_data="ai_agent_signal")]
            ])
        )
        return

    # ✅ Extract Instrument
    selected_instrument = query.data.replace("ai_signal_", "")
    if selected_instrument == "XAU":
        selected_instrument = "XAUUSD"

    # ✅ Fetch from Backend
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{AI_API_URL}/get_signal/{selected_instrument}")
            if response.status_code == 200:
                trade_signal = response.json().get("signal", get("signal_error"))
            else:
                trade_signal = get("signal_error")
    except Exception as e:
        print(f"❌ AI Signal Error: {e}")
        trade_signal = get("signal_error")

    formatted_message = f"Naomi Have *{selected_instrument}* Dicision\n{trade_signal}"
    keyboard = [[InlineKeyboardButton(get("btn_back"), callback_data="ai_agent_signal")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # ✅ Try to edit safely (avoid Message Not Modified)
    try:
        await query.message.edit_text(
            formatted_message,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        if "Message is not modified" not in str(e):
            print(f"❌ Failed to edit message: {e}")



# ✅ Function to show instrument selection buttons
async def show_instruments(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if context.user_data.get("cooldown"):
        return
    context.user_data["cooldown"] = True
    asyncio.create_task(reset_cooldown(context))

    user_id = query.from_user.id
    get = lambda key: get_text(user_id, key, context)

    keyboard = [
        [InlineKeyboardButton(get("instrument_gold"), callback_data="ai_signal_XAUUSD")],
        [
            InlineKeyboardButton(get("instrument_bitcoin"), callback_data="ai_signal_BTC"),
            InlineKeyboardButton(get("instrument_ethereum"), callback_data="ai_signal_ETH")
        ],
        [
            InlineKeyboardButton(get("instrument_dowjones"), callback_data="ai_signal_DJI"),
            InlineKeyboardButton(get("instrument_nasdaq"), callback_data="ai_signal_IXIC")
        ],
        [
            InlineKeyboardButton(get("instrument_eurusd"), callback_data="ai_signal_EURUSD"),
            InlineKeyboardButton(get("instrument_gbpusd"), callback_data="ai_signal_GBPUSD")
        ],
        [InlineKeyboardButton(get("btn_back"), callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(
        get("smart_signal_title"),
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ✅ Callback Query Handlers (if needed in bot.py)
ai_signal_handler = CallbackQueryHandler(fetch_ai_signal, pattern='^ai_signal_')
instrument_menu_handler = CallbackQueryHandler(show_instruments, pattern='^ai_agent_signal$')
