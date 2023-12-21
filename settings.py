control_discount = 30
brands_pl = ['Apple', 'Huawei', 'Realme', 'Samsung', 'Xiaomi', 'Honor']
brands_kof = ['DeLonghi', 'Philips', 'Smeg', 'Polaris', 'Nivona', 'Jura', 'Bosh']


def filter_product(name):
    flag = False
    if any(brand in name for brand in brands_pl):
        flag = True
    elif any(brand in name for brand in brands_kof):
        flag = True
    return flag


