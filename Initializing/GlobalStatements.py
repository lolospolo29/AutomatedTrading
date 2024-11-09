lockState = False

def set_lock_state(value: bool):
    global lockState
    lockState = value

def get_lock_state():
    return lockState