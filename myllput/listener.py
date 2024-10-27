import asyncio
from pynput import keyboard, mouse

class KeyListener:
    def __init__(self):
        self._running = False
        self._task = None
        self.key_bindings = {}  # keybindings storage
        
        self._listener = keyboard.Listener(  # Create a listener object
            on_press=lambda key: self.on_key(key, True),
            on_release=lambda key: self.on_key(key, False)
        )

    def on_key(self, key, pressed):
        """Handles key events, checking if a function is bound to the key."""
        if key in self.key_bindings and pressed:  # Only trigger on key press
            try:
                self.key_bindings[key]()  # Call the bound function
            except Exception as e:
                print(f"Error executing function for {key}: {e}")

    def bind_key(self, key, func):
        """Binds a function to a specific key."""
        self.key_bindings[key] = func
        print(f"Bound function {func.__name__} to key {key}")

    async def _listen(self):  # coroutine function
        self._listener.start()  # start listening
        while self._running:
            await asyncio.sleep(0.1)  # check every 0.1 seconds
        self._listener.stop()  # stop listening when running is set to False

    def start(self):
        """Starts the input listener coroutine."""
        if not self._task:  # Only start if no task is running
            self._running = True
            self._task = asyncio.create_task(self._listen())

    async def stop(self):
        """Stops the input listener coroutine."""
        self._running = False
        await self._task


class MouseListener:
    def __init__(self):
        self._running = False
        self._task = None
        self.button_bindings = {}  # mouse button bindings storage
        
        self._listener = mouse.Listener(  # Create a mouse listener
            on_click=self.on_click
        )

    def on_click(self, x, y, button, pressed):
        """Handles mouse click events, checking if a function is bound to the button."""
        if button in self.button_bindings and pressed:  # Only trigger on button press
            try:
                self.button_bindings[button]()  # Call the bound function
            except Exception as e:
                print(f"Error executing function for {button}: {e}")

    def bind_button(self, button, func):
        """Binds a function to a specific mouse button."""
        self.button_bindings[button] = func
        print(f"Bound function {func.__name__} to button {button}")

    async def _listen(self):  # coroutine function
        self._listener.start()  # start listening
        while self._running:
            await asyncio.sleep(0.1)  # check every 0.1 seconds
        self._listener.stop()  # stop listening when running is set to False

    def start(self):
        """Starts the mouse listener coroutine."""
        if not self._task:  # Only start if no task is running
            self._running = True
            self._task = asyncio.create_task(self._listen())

    async def stop(self):
        """Stops the mouse listener coroutine."""
        if self._task:
            self._running = False
            await self._task