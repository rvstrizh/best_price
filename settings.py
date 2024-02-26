control_discount = 25
brands_pl = ['apple', 'huawei', 'realme', 'samsung', 'xiaomi', 'honor']
brands_kof = ['deLonghi', 'philips', 'smeg', 'polaris', 'nivona', 'jura', 'bosh']
brands_watch = ['apple', 'huawei', 'samsung']
brands_phone = ['huawei', 'realme', 'samsung', 'xiaomi', 'honor', 'asus', 'google', 'infinix', 'nothing', 'nubia', 'onePlus', 'oppo', 'oukitel', 'tecno']
BOT_TOKEN = '7095167593:AAHc3B7kiyUomCK8NNihSGj9enDvlYWvYxc'


def filter_product(name, category):
    flag = False
    if category == 'planshety' and any(brand in name.lower() for brand in brands_pl):
        flag = True
    elif category == 'kofemashiny' and any(brand in name.lower() for brand in brands_kof):
        flag = True
    elif category == 'umnye-chasy' and any(brand in name.lower() for brand in brands_watch):
        flag = True
    return flag


def filter_phone(name):
    # мне нужно найти name в спике
    for brand in brands_phone:
        if brand in name.lower():
            return brand


name = 'Смартфон Tecno CAMON 20 Pro 8/256GB Black'


