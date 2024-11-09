lockState = False

def setLockState(value: bool):
    global lockState
    lockState = value

def getLockState():
    return lockState