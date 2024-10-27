import asyncio
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController
from .actions import _BaseAction, _KeyAction, _MouseAction #import parent classes
from .actions import * #import all actions

class Sender:
    def __init__(self, tick_rate: float = 0.1):
        self.tick_rate = tick_rate  # The tick rate of the sender
        self._running = False  # The running state of the sender
        self._task = None  # The task object of the sender

        self.mouse_controller = MouseController()
        self.keyboard_controller = KeyboardController()

        self.single_actions = []  # Actions that are executed once
        self.persistent_actions = {}  # Actions that are executed every tick until removed

    async def _tick(self):
        while self._running:
            to_remove = []

            # Execute single actions
            for action in self.single_actions:
                await self._execute(action)
                if action.remove:
                    to_remove.append(action)
            
            # Remove marked single actions
            for action in to_remove:
                self.single_actions.remove(action)

            # Execute persistent actions
            for action in self.persistent_actions.values():
                await self._execute(action)

            await asyncio.sleep(self.tick_rate)

    async def _execute(self, action):
        if isinstance(action, _KeyAction):
            await action.execute(self.keyboard_controller)
        elif isinstance(action, _MouseAction):
            await action.execute(self.mouse_controller)
    
    def start(self):
        if not self._task:
            self._running = True
            self._task = asyncio.create_task(self._tick())

    async def stop(self):
        if self._task:
            self._running = False
            await self._task
    
    def start_action(self, action: _BaseAction = None):
        if hasattr(action, "remove"):
            self.single_actions.append(action)
        else:
            key = str(action.key)
            if key in self.persistent_actions:
                self.stop_action(key)
            self.persistent_actions[key] = action

    def stop_action(self, key):
        key = str(key)
        if key in self.persistent_actions:
            del self.persistent_actions[key]

#==================== KEYBOARD ====================#
class KeySender(Sender):
    def __init__(self, tick_rate: float = 0.1):
        super().__init__(tick_rate)

    # Predefined Actions
    def press(self, key): self.start_action(Key_SingleAction_Press(key))
    def hold(self, key): self.start_action(Key_PersistentAction_Hold(key))
    def release(self, key): self.stop_action(key)
    def spam(self, key): self.start_action(Key_PersistentAction_Spam(key))

#==================== MOUSE ====================#
class MouseSender(Sender):
    def __init__(self, tick_rate: float = 0.1):
        super().__init__(tick_rate)

    # Predefined Actions
    def click(self, key): self.start_action(Mouse_SingleAction_Click(key))
    def hold(self, key): self.start_action(Mouse_PersistentAction_Hold(key))
    def release(self, key): self.stop_action(key)
    def spam(self, key): self.start_action(Mouse_PersistentAction_Spam(key))