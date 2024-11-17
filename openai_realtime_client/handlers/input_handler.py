import asyncio

class InputHandler:
    """
    Handles input for the chatbot in a headless environment.
    """
    def __init__(self, external_queue: asyncio.Queue):
        """
        Initializes the InputHandler.

        Args:
            external_queue (asyncio.Queue): Queue to receive external button press events.
        """
        self.text_input = ""
        self.text_ready = asyncio.Event()
        self.command_queue = asyncio.Queue()
        self.external_queue = external_queue
        self.loop = asyncio.get_event_loop()
        self.running = False

    async def process_commands(self):
        """
        Asynchronously processes incoming commands from both internal and external sources.
        """
        while self.running:
            # Wait for either internal commands or external button presses
            done, pending = await asyncio.wait(
                [
                    asyncio.create_task(self.command_queue.get()),
                    asyncio.create_task(self.external_queue.get())
                ],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                result = task.result()
                if isinstance(result, tuple):
                    # Internal command
                    command, data = result
                    await self.handle_command(command, data)
                else:
                    # External button press
                    button = result
                    await self.handle_button_press(button)

    async def handle_command(self, command, data):
        """
        Handles internal commands.

        Args:
            command (str): The command type.
            data (Any): Additional data associated with the command.
        """
        if command == 'space':
            self.text_input += ' '
        elif command == 'enter':
            self.text_ready.set()
            # You can process the entered text here
            print(f"User Input: {self.text_input}")
            self.text_input = ""
        elif command == 'r':
            # Handle 'r' command
            pass
        elif command == 'q':
            # Handle 'q' command (e.g., quit)
            self.running = False
        elif isinstance(command, str):
            self.text_input += command

    async def handle_button_press(self, button):
        """
        Handles external button press events.

        Args:
            button (str): The button identifier.
        """
        if button == 'space':
            await self.handle_command('space', None)
        elif button == 'enter':
            await self.handle_command('enter', None)
        elif button == 'r':
            await self.handle_command('r', None)
        elif button == 'q':
            await self.handle_command('q', None)
        else:
            # Handle other buttons or characters
            await self.handle_command(button, None)

    def start(self):
        """
        Starts the input processing loop.
        """
        self.running = True
        self.loop.create_task(self.process_commands())

    def stop(self):
        """
        Stops the input processing loop.
        """
        self.running = False