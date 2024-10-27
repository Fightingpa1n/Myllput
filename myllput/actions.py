import asyncio
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController

KEY_PRESS_DURATION = 0.01  # Duration of how long a key is pressed for


class _BaseAction:
    def __init__(self, key):
        self.key = key  # The key to press or mouse button to click
    async def execute(self, controller): pass  # Execute gets called each tick by the sender

#==================== KEYBOARD ====================#
class _KeyAction(_BaseAction):  # Base class for key actions
    async def execute(self, controller: KeyboardController): pass

class Key_SingleAction_Press(_KeyAction):  # Press a key once
    def __init__(self, key):
        super().__init__(key)
        self.remove = False

    async def execute(self, controller: KeyboardController):
        controller.press(self.key)
        await asyncio.sleep(KEY_PRESS_DURATION)
        controller.release(self.key)
        self.remove = True

class Key_PersistentAction_Hold(_KeyAction):  # Hold a key down
    async def execute(self, controller: KeyboardController):
        controller.press(self.key)

class Key_PersistentAction_Spam(_KeyAction):  # Spam a key
    async def execute(self, controller: KeyboardController):
        controller.press(self.key)
        await asyncio.sleep(KEY_PRESS_DURATION)
        controller.release(self.key)

#==================== MOUSE ====================#
class _MouseAction(_BaseAction):  # Base class for mouse actions
    async def execute(self, controller: MouseController): pass

class Mouse_SingleAction_Click(_MouseAction):  # Click a mouse button once
    def __init__(self, key):
        super().__init__(key)
        self.remove = False

    async def execute(self, controller: MouseController):
        controller.click(self.key)
        self.remove = True

class Mouse_PersistentAction_Hold(_MouseAction):  # Hold a mouse button down
    async def execute(self, controller: MouseController):
        controller.press(self.key)

class Mouse_PersistentAction_Spam(_MouseAction):  # Spam a mouse button
    async def execute(self, controller: MouseController):
        controller.click(self.key)