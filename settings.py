control_discount = 32
brands_pl = ['Apple', 'Huawei', 'Realme', 'Samsung', 'Xiaomi', 'Honor']
brands_kof = ['DeLonghi', 'Philips', 'Smeg', 'Polaris', 'Nivona', 'Jura', 'Bosh']
brands_watch = ['Apple', 'Huawei', 'Samsung']


def filter_product(name, category):
    flag = False
    if category == 'planshety' and any(brand in name for brand in brands_pl):
        flag = True
    elif category == 'kofemashiny' and any(brand in name for brand in brands_kof):
        flag = True
    elif category == 'umnye-chasy' and any(brand in name for brand in brands_watch):
        flag = True
    return flag


