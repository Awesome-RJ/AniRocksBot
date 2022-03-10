from bot import bot
from pyrogram import types, filters


@bot.on_message(filters.text & ~filters.edited)
async def search_handler(client:bot, message: types.Message):
    if (
        message.text.startswith('/')
        or not message.text.startswith('/')
        and message.chat.type != 'private'
    ):
        return None
    buttons = []
    data = await bot.search_anime(message.text)
    if len(data) == 0:
        return await message.reply(f'**Cannot find any results for:** {message.text}')
    buttons.extend([
                types.InlineKeyboardButton(
                    anime.title,
                    callback_data=f'ani_{anime.id}'
                )
            ] for anime in data if len(anime.id) <= 58)
    await message.reply(
        f'**Search Results for:** {message.text}',
        reply_markup=types.InlineKeyboardMarkup(buttons)
    )


@bot.on_callback_query(filters.regex('^s_'))
async def search_handler(_, query):
    anime_id = query.data.split('_')[1]
    buttons = []
    data = await bot.search_anime(anime_id)
    if len(data) == 0:
        return await query.message.edit(f'**Cannot find any results for:** {anime_id}')
    buttons.extend([
                types.InlineKeyboardButton(
                    anime.title,
                    callback_data=f'ani_{anime.id}'
                )
            ] for anime in data if len(anime.id) <= 56)
    await query.message.edit(
        f'**Search Results for:** {anime_id}',
        reply_markup=types.InlineKeyboardMarkup(buttons)
    )