import win32api
import win32con


class KeyboardKeys(object):
    VK_CODE = {
        'enter': 0x0D,
        'ctrl': 0x11,
        'v': 0x56}

    @staticmethod
    def keyDown(keyName):
        win32api.keybd_event(KeyboardKeys.VK_CODE[keyName], 0, 0, 0)

    @staticmethod
    def keyUp(keyName):
        win32api.keybd_event(KeyboardKeys.VK_CODE[keyName], 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def oneKey(key):
        KeyboardKeys.keyDown(key)
        KeyboardKeys.keyUp(key)

    @staticmethod
    def twoKey(key1, key2):
        KeyboardKeys.keyDown(key1)
        KeyboardKeys.keyDown(key2)
        KeyboardKeys.keyUp(key1)
        KeyboardKeys.keyUp(key1) 