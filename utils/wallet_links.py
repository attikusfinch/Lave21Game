from settings import WALLET, LAVE

def send_ton(user_id):
    return f"ton://transfer/{WALLET}?text={user_id}"

def send_lave(user_id):
    return f"ton://transfer/{WALLET}?jetton={LAVE}&text={user_id}"