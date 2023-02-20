import time
from PIL import Image
while True:
    img = []
    o = []
    for i in range(1, 6):
        for j in range(1, 6):
           img.append(Image.open("C:/Users/maxga/PycharmProjects/matrix_bot/matrix/"+str(i)+"/"+str(j)+".png"))
    img_01_size = [int(208), int(208)]

    new_im = Image.new('RGB', (5 * img_01_size[0], 5 * img_01_size[1]), (250, 250, 250))

    new_im.paste(img[0].resize((208, 208)), (0,0))
    new_im.paste(img[1].resize((208, 208)), (208,0))
    new_im.paste(img[2].resize((208, 208)), (416,0))
    new_im.paste(img[3].resize((208, 208)), (624,0))
    new_im.paste(img[4].resize((208, 208)), (832,0))
    new_im.paste(img[5].resize((208, 208)), (0,208))
    new_im.paste(img[6].resize((208, 208)), (208,208))
    new_im.paste(img[7].resize((208, 208)), (416,208))
    new_im.paste(img[8].resize((208, 208)), (624,208))
    new_im.paste(img[9].resize((208, 208)), (832,208))
    new_im.paste(img[10].resize((208, 208)), (0,416))
    new_im.paste(img[11].resize((208, 208)), (208,416))
    new_im.paste(img[12].resize((208, 208)), (416,416))
    new_im.paste(img[13].resize((208, 208)), (624,416))
    new_im.paste(img[14].resize((208, 208)), (832,416))
    new_im.paste(img[15].resize((208, 208)), (0,624))
    new_im.paste(img[16].resize((208, 208)), (208,624))
    new_im.paste(img[17].resize((208, 208)), (416,624))
    new_im.paste(img[18].resize((208, 208)), (624,624))
    new_im.paste(img[19].resize((208, 208)), (832,624))
    new_im.paste(img[20].resize((208, 208)), (0,832))
    new_im.paste(img[21].resize((208, 208)), (208,832))
    new_im.paste(img[22].resize((208, 208)), (416,832))
    new_im.paste(img[23].resize((208, 208)), (624,832))
    new_im.paste(img[24].resize((208, 208)), (832,832))



    new_im.save("map.png", "PNG")
    time.sleep(43200)
