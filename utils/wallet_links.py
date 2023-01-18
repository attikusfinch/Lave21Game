from settings import WALLET, LAVE

def send_ton(user_id):
    return f"ton://transfer/{WALLET}?text={user_id}"

def send_lave(user_id):
    # hard coded lave address, cuz it has tonkeeper bag
    return f"ton://transfer/{WALLET}?jetton=EQBl3gg6AAdjgjO2ZoNU5Q5EzUIl8XMNZrix8Z5dJmkHUfxI&text={user_id}"

def send_tonkeeper_ton(user_id):
    return f"https://app.tonkeeper.com/transfer/{WALLET}?text={user_id}"

def send_tonkeeper_lave(user_id):
    # hard coded lave address, cuz it has tonkeeper bag
    return f"https://app.tonkeeper.com/transfer/{WALLET}?jetton=EQBl3gg6AAdjgjO2ZoNU5Q5EzUIl8XMNZrix8Z5dJmkHUfxI&text={user_id}"