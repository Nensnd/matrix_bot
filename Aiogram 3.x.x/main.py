import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile as file
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from PIL import Image, ImageDraw, ImageFont
color = ''
work = 0


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token="6233306362:AAGa3XQ10aESz5vYoJV9lR-r22qBX6AQd9g")

# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Здесь вы управляете матрицей!\nВот команды, которые вы можете использолвать:\n/add - команда для добавление пикселя\n/map - команда для вывода всей карты (карта обновляется каждый час)\n/view - команда для вывода кусочка матрицы с размером 1024x1024\nпример: '/view 160 70'")

# Хэндлер на команду /map
@dp.message(Command("map"))
async def cmd_start(message: types.Message):
    await message.reply_document(file("map.png"))

# Хэндлер на команду /view
@dp.message(Command('view'))
async def view(message: types.Message):
    m = str(message.text).replace("/view ", "")
    m = str(message.text).replace("/view", "")
    m.split()

    x = int(m.split()[0])
    y = int(m.split()[1])

    cx = int(int(x) / 2048)
    cy = int(int(y) / 2048)

    if cx < 1:
        cx = 1

    if cy < 1:
        cy = 1

    img_01 = Image.open("matrix/"+str(cx)+"/"+str(cy)+".png")
    img_02 = Image.open("matrix/"+str(cx + 1)+"/"+str(cy)+".png")
    img_03 = Image.open("matrix/"+str(cx)+"/"+str(cy + 1)+".png")
    img_04 = Image.open("matrix/"+str(cx + 1)+"/"+str(cy + 1)+".png")

    img_01_size = img_01.size
    new_im = Image.new('RGB', (2 * img_01_size[0], 2 * img_01_size[1]), (250, 250, 250))

    new_im.paste(img_01, (0, 0))
    new_im.paste(img_02, (img_01_size[0], 0))
    new_im.paste(img_03, (0, img_01_size[1]))
    new_im.paste(img_04, (img_01_size[0], img_01_size[1]))
    new_im.save("view.png", "PNG")
    new_im.close()
    new_im = Image.open('view.png')
    cx = cx - 1
    cy = cy - 1
    croped = new_im.crop(((int(x) - cx * 2048) - 512, (int(y) - cy * 2048) - 512, (int(x) - cx * 2048) + 513,(int(y) - cy * 2048) + 513))
    croped.save('view.png', 'PNG')

    await message.reply_document(file("view.png"))

# Хэндлер на команду /add
@dp.message(Command("add"))
async def reply_builder(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text= 'Черный', callback_data='1'))
    builder.add(types.InlineKeyboardButton(text= 'Белый', callback_data='2'))
    builder.add(types.InlineKeyboardButton(text= 'Красный', callback_data='3'))
    builder.add(types.InlineKeyboardButton(text= 'Оранжевый', callback_data='4'))
    builder.add(types.InlineKeyboardButton(text= 'Желтый', callback_data='5'))
    builder.add(types.InlineKeyboardButton(text= 'Зеленый', callback_data='6'))
    builder.add(types.InlineKeyboardButton(text= 'Синий', callback_data='7'))
    builder.add(types.InlineKeyboardButton(text= 'Фиолетовый', callback_data='8'))
    builder.add(types.InlineKeyboardButton(text= 'Коричневый', callback_data='9'))
    builder.add(types.InlineKeyboardButton(text='Серый', callback_data='10'))
    builder.adjust(3)
    await message.answer(
        "Выберите цвет:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )



# Коллбэки для кнопок (цветов)
@dp.callback_query(F.data == "1")
async def black(callback: types.CallbackQuery):
    global work
    global color
    color = 'black'
    work = 1
    await bot.send_message(chat_id=callback.from_user.id, text='Теперь напишите координаты через пробел')


@dp.callback_query(F.data == "2")
async def white(callback: types.CallbackQuery):
    global work
    global color
    color = 'white'
    work = 1
    await bot.send_message(chat_id=callback.from_user.id, text='Теперь напишите координаты через пробел')


@dp.callback_query(F.data == "3")
async def red(callback: types.CallbackQuery):
    global work
    global color
    color = 'red'
    work = 1
    await bot.send_message(chat_id=callback.from_user.id, text='Теперь напишите координаты через пробел')

@dp.callback_query(F.data == "4")
async def orange(callback: types.CallbackQuery):
    global work
    global color
    color = 'orange'
    work = 1
    await bot.send_message(chat_id=callback.from_user.id, text='Теперь напишите координаты через пробел')

@dp.callback_query(F.data == "5")
async def orange(callback: types.CallbackQuery):
    global work
    global color
    color = 'yellow'
    work = 1
    await bot.send_message(chat_id=callback.from_user.id, text='Теперь напишите координаты через пробел')

@dp.callback_query(F.data == "6")
async def orange(callback: types.CallbackQuery):
    global work
    global color
    color = 'green'
    work = 1
    await bot.send_message(chat_id=callback.from_user.id, text='Теперь напишите координаты через пробел')

@dp.callback_query(F.data == "7")
async def orange(callback: types.CallbackQuery):
    global work
    global color
    color = 'blue'
    work = 1
    await bot.send_message(chat_id=callback.from_user.id, text='Теперь напишите координаты через пробел')

@dp.callback_query(F.data == "8")
async def orange(callback: types.CallbackQuery):
    global work
    global color
    color = 'purple'
    work = 1
    await bot.send_message(chat_id=callback.from_user.id, text='Теперь напишите координаты через пробел')

@dp.callback_query(F.data == "9")
async def orange(callback: types.CallbackQuery):
    global work
    global color
    color = 'brown'
    work = 1
    await bot.send_message(chat_id=callback.from_user.id, text='Теперь напишите координаты через пробел')

@dp.callback_query(F.data == "10")
async def black(callback: types.CallbackQuery):
    global work
    global color
    color = 'grey'
    work = 1
    await bot.send_message(chat_id=callback.from_user.id, text='Теперь напишите координаты через пробел')

@dp.message()
async def mainloop(message):
    global work
    if work == 1:
        global color
        work = 0
        a = str(message.text)
        a = a.split()
        x = int(a[0])
        y = int(a[1])

        cx = int(int(x) / 2048)
        cy = int(int(y) / 2048)

        if cx < 1:
            cx = 1

        if cy < 1:
            cy = 1

        img_01 = Image.open("matrix/"+str(cx)+"/"+str(cy)+".png")
        img_02 = Image.open("matrix/"+str(cx + 1)+"/"+str(cy)+".png")
        img_03 = Image.open("matrix/"+str(cx)+"/"+str(cy + 1)+".png")
        img_04 = Image.open("matrix/"+str(cx + 1)+"/"+str(cy + 1)+".png")

        img_01_size = img_01.size

        new_im = Image.new('RGB', (2 * img_01_size[0], 2 * img_01_size[1]), (250, 250, 250))

        new_im.paste(img_01, (0, 0))
        new_im.paste(img_02, (img_01_size[0], 0))
        new_im.paste(img_03, (0, img_01_size[1]))
        new_im.paste(img_04, (img_01_size[0], img_01_size[1]))
        new_im.save("merged_matrix.png", "PNG")

        new_im.close()
        new_im = Image.open('merged_matrix.png')
        cx = cx - 1
        cy = cy - 1

        draw = ImageDraw.Draw(new_im)
        draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill=color)

        croped = new_im.crop(((int(x) - cx * 2048)-128, (int(y) - cy * 2048)-128, (int(x) - cx * 2048) + 129, (int(y) - cy * 2048) + 129))
        '''c_end = croped.resize((2561, 2561))'''
        croped.save('croped.png', 'PNG')
        await message.reply("Ваш запрос обработан!\nМатрица изменена!")
        await message.reply_document(file("croped.png"))

        #img_01
        if int(x) < 2049 and int(y) < 2049:
            img = img_01
            draw = ImageDraw.Draw(img_01)
            draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill=color)

        #img_02
        elif int(x) > 2048 and int(y) < 2049:
            img = img_02
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x)- 2048 - cx * 2048, int(y) - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - cy * 2048), fill=color)


        #img_03
        elif int(x) < 2049 and int(y) > 2048:
            img = img_03
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - cx * 2048, int(y) - 2048 - cy * 2048), fill=color)


        # img_04
        elif int(x) > 2048 and int(y) > 2048:
            img = img_04
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048), fill=color)

        cx = int(int(x) / 2048)
        cy = int(int(y) / 2048)

        if cx < 1:
            cx = 1

        if cy < 1:
            cy = 1
        if cx < 1:
            cx = 1


        img_01.save("matrix/"+str(cx)+"/"+str(cy)+".png")
        img_02.save("matrix/" + str(cx + 1) + "/" + str(cy) + ".png")
        img_03.save("matrix/" + str(cx) + "/" + str(cy + 1) + ".png")
        img_04.save("matrix/" + str(cx + 1) + "/" + str(cy + 1) + ".png")


async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())