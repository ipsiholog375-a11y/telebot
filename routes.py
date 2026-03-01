from __future__ import annotations

from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.types import ErrorEvent, InlineKeyboardButton, InlineKeyboardMarkup

from .config import ADMIN_ID, CONTACT_LINK, PAYMENT_LINK
from .loader import bot, logger
from .stats import (
    active_users_last_days,
    add_order_event,
    new_users_today,
    top_services,
    total_users,
    touch_user,
)

router = Router(name="main")

MAIN_MENU_TEXT = "🌙 *ГОЛОВНЕ МЕНЮ*\n\n✨ Обери напрямок, який тебе кличе 👇"
TAROT_MENU_TEXT = (
    "🔮 *РОЗКЛАДИ НА ТАРО*\n\n"
    "✨ Вітаю в світі Таро - місці, де карти говорять душею.\n"
    "Обери напрямок, який тебе цікавить 👇"
)
RITUALS_MENU_TEXT = "🕯️ *РИТУАЛИ*\n\nМагія діє, коли серце вірить. Обери свій напрямок 👇"
STUDY_MENU_TEXT = "📚 *НАВЧАННЯ*\n\n🔮 Відчуй поклик магії - навчись керувати енергіями!"
HELP_TEXT = (
    "🌟 *Довідка / Help*\n\n"
    "Ось що я можу для тебе зробити:\n"
    "🔮 */start* - показати головне меню\n"
    "📋 */menu* - повернутись у головне меню\n"
    "💬 *Онлайн-консультація* - отримати індивідуальну пораду\n"
    "🕯️ *Ритуали* - обрати магічний напрямок\n"
    "📚 *Навчання* - дізнатись про курси\n"
    "💌 *Зв'язок із BellaTaro* - написати напряму\n"
    "💰 *Оплата* - усі послуги оплачуються через безпечне посилання"
)

TAROT_ORDERS = {
    "order_tarot_love": ("Розклад 'Кохання та стосунки'", "1500 грн"),
    "order_tarot_finance": ("Розклад 'Фінанси та кар'єра'", "1500 грн"),
    "order_tarot_self": ("Розклад 'Самопізнання'", "1500 грн"),
    "order_tarot_karma": ("Розклад 'Кармічні уроки'", "1000 грн"),
    "order_tarot_all": ("Розклад 'На всі сфери життя'", "1500 грн"),
}

RITUAL_ORDERS = {
    "order_ritual_love": ("Ритуал 'На кохання / примирення'", "від 500 грн"),
    "order_ritual_finance": ("Ритуал 'На фінансовий потік'", "від 1000 грн"),
    "order_ritual_clean": ("Ритуал 'Очищення від негативу'", "від 550 грн"),
    "order_ritual_harmony": ("Ритуал 'Гармонізація енергій'", "500 грн"),
    "order_ritual_individual": ("Індивідуальний ритуал", "ціна за домовленістю"),
}

STUDY_ORDERS = {
    "order_study_tarot": ("Курс 'Таро для початківців'", "3000 грн"),
    "order_study_rituals": ("Курс 'Сила Ритуалів'", "4000 грн"),
    "order_study_individual": ("Індивідуальне навчання", "ціна за домовленістю"),
}


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔮 Розклади на Таро", callback_data="menu_tarot")],
            [InlineKeyboardButton(text="🕯️ Ритуали", callback_data="menu_rituals")],
            [InlineKeyboardButton(text="💬 Онлайн-консультація", callback_data="menu_consult")],
            [InlineKeyboardButton(text="📚 Навчання", callback_data="menu_study")],
            [InlineKeyboardButton(text="💌 Зв'язок із BellaTaro", url=CONTACT_LINK)],
        ]
    )


def tarot_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❤️ Кохання та стосунки (1500 грн)", callback_data="order_tarot_love")],
            [InlineKeyboardButton(text="💰 Фінанси та кар'єра (1500 грн)", callback_data="order_tarot_finance")],
            [InlineKeyboardButton(text="🌿 Самопізнання (1500 грн)", callback_data="order_tarot_self")],
            [InlineKeyboardButton(text="⚖️ Кармічні уроки (1000 грн)", callback_data="order_tarot_karma")],
            [InlineKeyboardButton(text="🌟 На всі сфери життя (1500 грн)", callback_data="order_tarot_all")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_main")],
        ]
    )


def rituals_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💞 На кохання / примирення (від 500 грн)", callback_data="order_ritual_love")],
            [InlineKeyboardButton(text="💸 На фінансовий потік (від 1000 грн)", callback_data="order_ritual_finance")],
            [InlineKeyboardButton(text="🔥 На очищення від негативу (від 550 грн)", callback_data="order_ritual_clean")],
            [InlineKeyboardButton(text="🌕 Гармонізація енергій (500 грн)", callback_data="order_ritual_harmony")],
            [InlineKeyboardButton(text="🌺 Індивідуальний ритуал", callback_data="order_ritual_individual")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_main")],
        ]
    )


def study_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🃏 Курс 'Таро для початківців' (3000 грн)", callback_data="order_study_tarot")],
            [InlineKeyboardButton(text="🕯️ Курс 'Сила Ритуалів' (4000 грн)", callback_data="order_study_rituals")],
            [InlineKeyboardButton(text="🌙 Індивідуальне навчання", callback_data="order_study_individual")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_main")],
        ]
    )


def payment_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Перейти до оплати", url=PAYMENT_LINK)],
            [InlineKeyboardButton(text="❌ Скасувати", callback_data="menu_main")],
        ]
    )


def _touch_from_user(user: types.User | None) -> None:
    if not user:
        return
    touch_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )


async def safe_edit_or_send(
    call: types.CallbackQuery,
    text: str,
    keyboard: InlineKeyboardMarkup | None = None,
) -> None:
    if not call.message:
        await call.answer("Не вдалося оновити повідомлення", show_alert=True)
        return

    try:
        await call.message.edit_text(text=text, reply_markup=keyboard)
    except TelegramBadRequest as exc:
        logger.warning("Cannot edit message: %s", exc)
        await call.message.answer(text=text, reply_markup=keyboard)
    finally:
        await call.answer()


def payment_text(service_name: str, price: str) -> str:
    return (
        f"Чудово! Ти обрав(ла) *{service_name}*.\n"
        f"💰 *Вартість: {price}*\n\n"
        "Для оплати, будь ласка, перейди за посиланням на кнопці нижче 👇\n\n"
        "‼️ *ВАЖЛИВО:* у коментарі до платежу вкажи своє ім'я в Telegram та бажаний час.\n"
        "Наприклад: Анастасія Велика, 18:00\n\n"
        "Після оплати просто напиши сюди у відповідь, що оплатив(ла).\n"
        "Можеш також прислати скріншот чека. Я передам замовлення BellaTaro 🌹"
    )


async def send_payment(call: types.CallbackQuery, service_key: str, service_name: str, price: str) -> None:
    if call.from_user:
        add_order_event(call.from_user.id, service_key)
    await safe_edit_or_send(call, payment_text(service_name, price), payment_menu())


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    _touch_from_user(message.from_user)
    await message.answer(MAIN_MENU_TEXT, reply_markup=main_menu())


@router.message(Command("menu"))
async def cmd_menu(message: types.Message) -> None:
    _touch_from_user(message.from_user)
    await message.answer(MAIN_MENU_TEXT, reply_markup=main_menu())


@router.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    _touch_from_user(message.from_user)
    await message.answer(HELP_TEXT)


@router.message(Command("stats"))
async def cmd_stats(message: types.Message) -> None:
    if not message.from_user or message.from_user.id != ADMIN_ID:
        await message.answer("❌ Ця команда доступна тільки адміну.")
        return

    lines = [
        "📊 *Статистика бота*",
        "",
        f"👥 Всього користувачів: *{total_users()}*",
        f"🆕 Нових сьогодні: *{new_users_today()}*",
        f"🕒 Активних за 24 години: *{active_users_last_days(1)}*",
        f"📅 Активних за 7 днів: *{active_users_last_days(7)}*",
        f"📆 Активних за 30 днів: *{active_users_last_days(30)}*",
    ]

    top = top_services(5)
    if top:
        lines.append("")
        lines.append("🔥 Топ послуг:")
        for service_key, count in top:
            lines.append(f"- `{service_key}`: *{count}*")

    await message.answer("\n".join(lines))


@router.callback_query(F.data == "menu_main")
async def cb_main(call: types.CallbackQuery) -> None:
    _touch_from_user(call.from_user)
    await safe_edit_or_send(call, MAIN_MENU_TEXT, main_menu())


@router.callback_query(F.data == "menu_tarot")
async def cb_tarot(call: types.CallbackQuery) -> None:
    await safe_edit_or_send(call, TAROT_MENU_TEXT, tarot_menu())


@router.callback_query(F.data == "menu_rituals")
async def cb_rituals(call: types.CallbackQuery) -> None:
    await safe_edit_or_send(call, RITUALS_MENU_TEXT, rituals_menu())


@router.callback_query(F.data == "menu_study")
async def cb_study(call: types.CallbackQuery) -> None:
    await safe_edit_or_send(call, STUDY_MENU_TEXT, study_menu())


@router.callback_query(F.data == "menu_consult")
async def cb_consult(call: types.CallbackQuery) -> None:
    await send_payment(call, "menu_consult", "Онлайн-консультація", "3000 грн")


@router.callback_query(F.data.startswith("order_tarot_"))
async def cb_tarot_order(call: types.CallbackQuery) -> None:
    service_name, price = TAROT_ORDERS.get(call.data, ("Послуга", "ціна уточнюється"))
    await send_payment(call, call.data or "order_tarot_unknown", service_name, price)


@router.callback_query(F.data.startswith("order_ritual_"))
async def cb_ritual_order(call: types.CallbackQuery) -> None:
    service_name, price = RITUAL_ORDERS.get(call.data, ("Ритуал", "ціна уточнюється"))
    await send_payment(call, call.data or "order_ritual_unknown", service_name, price)


@router.callback_query(F.data.startswith("order_study_"))
async def cb_study_order(call: types.CallbackQuery) -> None:
    service_name, price = STUDY_ORDERS.get(call.data, ("Навчання", "ціна уточнюється"))
    await send_payment(call, call.data or "order_study_unknown", service_name, price)


@router.callback_query()
async def cb_unknown(call: types.CallbackQuery) -> None:
    logger.warning("Unknown callback: %s", call.data)
    await call.answer("❌ Ця дія зараз недоступна", show_alert=True)


@router.message(F.text & ~F.command)
async def user_message_to_admin(message: types.Message) -> None:
    if not message.from_user:
        await message.answer("Щось пішло не так. Спробуй ще раз.")
        return

    _touch_from_user(message.from_user)
    user = message.from_user
    username = f"@{user.username}" if user.username else "немає username"
    user_info = f"Повідомлення від: {user.full_name} ({username}, ID: {user.id})"

    try:
        await bot.send_message(ADMIN_ID, user_info)
        await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        await message.answer("🌹 Дякую! BellaTaro скоро з тобою зв'яжеться.")
    except Exception:
        logger.exception("Failed to forward user message to admin")
        await message.answer("Щось пішло не так. Напиши напряму: @arinka90210")


@router.error()
async def on_error(event: ErrorEvent) -> None:
    logger.exception("Unhandled error: %s", event.exception)
