#импорт нужных библиотек
from PIL import Image, ImageDraw, ImageFont
import time
import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="")
# Диспетчер
dp = Dispatcher(bot)

# Хэндлер на команду /start
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Вы управляете виртуальной матрицей!")
    await message.reply("Команда /map показывает состояние всей матрицы. (обновляется каждые 12 часов)")
    await message.reply("Чтобы поменять состояние пикселя , нужно написать команду в таком формате:")
    await message.reply("состояние пикселя (0 - черный, 1 - белый, 2 - красный, 3 - оранжевый, 4 - желтый, 5 - зеленый, 6 - голубой, 7 - фиолетовый, 8 - серый), координата по x (0 - 10240), координата по y (0 - 10240)")
    await message.reply("вам будет виден косочек матрицы размером 256x256")
    await message.reply("пример: '5 160 90'")
    await message.reply("Чтобы просто просмотреть матрицу , введите /view и координаты , выведется кусочек матрицы размером 1024x1024")
    await message.reply("пример: '/view 160 70'")






@dp.message_handler(commands=['map'])
async def map(message):
    photo = open('map.png', 'rb')
    await message.reply_document(photo)

@dp.message_handler(commands=['view'])
async def view(message):
    m = str(message.text).replace("/view ", "")
    ax = []
    ay = []
    x = ''
    y = ''
    c = 0
    for i in m:
        if str(i) == ' ':
            c = c + 1
        if c == 0:
            ax.append(str(i))
        else:
            ay.append(str(i))


    for i in range(len(ax)):
        x = x + ax[i]

    for i in range(len(ay)):
        y = y + ay[i]


    cx = int(int(x) / 2048)
    cy = int(int(y) / 2048)

    if cx < 1:
        cx = 1

    if cy < 1:
        cy = 1

    img_01 = Image.open("/matrix/"+str(cx)+"/"+str(cy)+".png")
    img_02 = Image.open("/matrix/"+str(cx + 1)+"/"+str(cy)+".png")
    img_03 = Image.open("/matrix/"+str(cx)+"/"+str(cy + 1)+".png")
    img_04 = Image.open("/matrix/"+str(cx + 1)+"/"+str(cy + 1)+".png")

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
    c_end = croped.resize((2561, 2561))
    c_end.save('view.png', 'PNG')
    photo = open('view.png', 'rb')
    await message.reply_document(photo)
#обработка команд
@dp.message_handler(content_types=['text'])
async def mainloop(message):
    t = 0
    xp = []
    yp = []
    c = 0
    x = ''
    y = ''
    for i in message.text:
        if i != ' ':
            if c == 0:
                t = int(i)
            elif c == 1:
                xp.append(str(i))
            elif c == 2:
                yp.append(str(i))
        else:
            c = c + 1

    for i in xp:
        x = x + i

    for i in yp:
        y = y + i

    cx = int(int(x) / 2048)
    cy = int(int(y) / 2048)

    if cx < 1:
        cx = 1

    if cy < 1:
        cy = 1

    img_01 = Image.open("/matrix/"+str(cx)+"/"+str(cy)+".png")
    img_02 = Image.open("/matrix/"+str(cx + 1)+"/"+str(cy)+".png")
    img_03 = Image.open("/matrix/"+str(cx)+"/"+str(cy + 1)+".png")
    img_04 = Image.open("/matrix/"+str(cx + 1)+"/"+str(cy + 1)+".png")

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
    if t == 1:
        draw = ImageDraw.Draw(new_im)
        draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='white')
    elif t == 0:
        draw = ImageDraw.Draw(new_im)
        draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='black')
    elif t == 2:
        draw = ImageDraw.Draw(new_im)
        draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='red')
    elif t == 3:
        draw = ImageDraw.Draw(new_im)
        draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='orange')
    elif t == 4:
        draw = ImageDraw.Draw(new_im)
        draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='yellow')
    elif t == 5:
        draw = ImageDraw.Draw(new_im)
        draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='green')
    elif t == 6:
        draw = ImageDraw.Draw(new_im)
        draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='blue')
    elif t == 7:
        draw = ImageDraw.Draw(new_im)
        draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='purple')
    elif t == 8:
        draw = ImageDraw.Draw(new_im)
        draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='darkgrey')
    croped = new_im.crop(((int(x) - cx * 2048)-128, (int(y) - cy * 2048)-128, (int(x) - cx * 2048) + 129, (int(y) - cy * 2048) + 129))
    '''c_end = croped.resize((2561, 2561))'''
    croped.save('croped.png', 'PNG')
    await message.reply("Ваш запрос обработан! матрица изменена !")
    photo = open('croped.png', 'rb')
    await message.reply_document(photo)

    #img_01
    if int(x) < 2049 and int(y) < 2049:
        img = img_01
        if t == 1:
            draw = ImageDraw.Draw(img_01)
            draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='white')
        elif t == 0:
            draw = ImageDraw.Draw(img_01)
            draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='black')
        elif t == 2:
            draw = ImageDraw.Draw(img_01)
            draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='red')
        elif t == 3:
            draw = ImageDraw.Draw(img_01)
            draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='orange')
        elif t == 4:
            draw = ImageDraw.Draw(img_01)
            draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='yellow')
        elif t == 5:
            draw = ImageDraw.Draw(img_01)
            draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='green')
        elif t == 6:
            draw = ImageDraw.Draw(img_01)
            draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='blue')
        elif t == 7:
            draw = ImageDraw.Draw(img_01)
            draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='purple')
        elif t == 8:
            draw = ImageDraw.Draw(img_01)
            draw.rectangle((int(x) - cx * 2048, int(y) - cy * 2048, int(x) - cx * 2048, int(y) - cy * 2048), fill='darkgrey')

    #img_02
    elif int(x) > 2048 and int(y) < 2049:
        img = img_02
        if t == 1:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x)- 2048 - cx * 2048, int(y) - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - cy * 2048), fill='white')
        elif t == 0:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - 2048 - cx * 2048, int(y) - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - cy * 2048), fill='black')
        elif t == 2:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - 2048 - cx * 2048, int(y) - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - cy * 2048), fill='red')
        elif t == 3:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x)- 2048 - cx * 2048, int(y) - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - cy * 2048), fill='orange')
        elif t == 4:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x)- 2048 - cx * 2048, int(y) - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - cy * 2048), fill='yellow')
        elif t == 5:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x)- 2048 - cx * 2048, int(y) - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - cy * 2048), fill='green')
        elif t == 6:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x)- 2048 - cx * 2048, int(y) - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - cy * 2048), fill='blue')
        elif t == 7:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x)- 2048 - cx * 2048, int(y) - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - cy * 2048), fill='purple')
        elif t == 8:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x)- 2048 - cx * 2048, int(y) - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - cy * 2048), fill='darkgrey')

    #img_03
    elif int(x) < 2049 and int(y) > 2048:
        img = img_03
        if t == 1:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - cx * 2048, int(y) - 2048 - cy * 2048), fill='white')
        elif t == 0:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - cx * 2048, int(y) - 2048 - cy * 2048), fill='black')
        elif t == 2:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - cx * 2048, int(y) - 2048 - cy * 2048), fill='red')
        elif t == 3:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - cx * 2048, int(y) - 2048 - cy * 2048), fill='orange')
        elif t == 4:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - cx * 2048, int(y) - 2048 - cy * 2048), fill='yellow')
        elif t == 5:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - cx * 2048, int(y) - 2048 - cy * 2048), fill='green')
        elif t == 6:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - cx * 2048, int(y) - 2048 - cy * 2048), fill='blue')
        elif t == 7:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - cx * 2048, int(y) - 2048 - cy * 2048), fill='purple')
        elif t == 8:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - cx * 2048, int(y) - 2048 - cy * 2048), fill='darkgrey')


    # img_04
    elif int(x) > 2048 and int(y) > 2048:
        img = img_04
        if t == 1:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048), fill='white')
        elif t == 0:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048),fill='black')
        elif t == 2:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048),fill='red')
        elif t == 3:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048),fill='orange')
        elif t == 4:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048),fill='yellow')
        elif t == 5:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048),fill='green')
        elif t == 6:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048),fill='blue')
        elif t == 7:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048),fill='purple')
        elif t == 8:
            draw = ImageDraw.Draw(img)
            draw.rectangle((int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048, int(x) - 2048 - cx * 2048, int(y) - 2048 - cy * 2048),fill='darkgrey')

    cx = int(int(x) / 2048)
    cy = int(int(y) / 2048)

    if cx < 1:
        cx = 1

    if cy < 1:
        cy = 1
    if cx < 1:
        cx = 1


    img_01.save("/matrix/"+str(cx)+"/"+str(cy)+".png")
    img_02.save("/matrix/" + str(cx + 1) + "/" + str(cy) + ".png")
    img_03.save("/matrix/" + str(cx) + "/" + str(cy + 1) + ".png")
    img_04.save("/matrix/" + str(cx + 1) + "/" + str(cy + 1) + ".png")



'''if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)'''
#цикл
if 1 == 1:
  while True:
    try:
      executor.start_polling(dp, skip_updates=True)
    except:
      time.sleep(0.3)
