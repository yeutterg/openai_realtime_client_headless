import asyncio
import logging

class InputHandler:
    """
    Handles input for the chatbot in a headless environment.
    """
    def __init__(self, external_queue: asyncio.Queue, loop: asyncio.AbstractEventLoop):
        """
        Initializes the InputHandler.

        Args:
            external_queue (asyncio.Queue): Queue to receive external button press events.
            loop (asyncio.AbstractEventLoop): Reference to the asyncio event loop.
        """
        self.text_input = ""
        self.text_ready = asyncio.Event()
        self.command_queue = asyncio.Queue()
        self.external_queue = external_queue
        self.loop = loop
        self.running = False

        # Configure logging for InputHandler
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] [InputHandler] %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )

    async def process_commands(self):
        """
        Asynchronously processes incoming commands from both internal and external sources.
        """
        logging.info("InputHandler started processing commands.")
        while self.running:
            try:
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
                        await self.handle_input('command', result)
                    else:
                        # External button press
                        await self.handle_input('button', result)
            except Exception as e:
                logging.error(f"Error processing commands: {e}")

        logging.info("InputHandler stopped processing commands.")

    async def handle_input(self, input_type, input_value):
        """
        Handles both internal commands and external button press events.

        Args:
            input_type (str): The type of input ('command' or 'button').
            input_value (Any): The value associated with the input (command or button).
        """
        logging.info(f"InputHandler: Handling {input_type}: {input_value}")
        
        if input_type == 'command':
            command, data = input_value
        else:  # input_type == 'button'
            command = input_value
            data = None

        if command == 'space':
            logging.info("InputHandler: Handling 'space' command.")
            self.text_input += ' '

        elif command == 'enter':
            logging.info("InputHandler: Handling 'enter' command.")
            self.loop.call_soon_threadsafe(
                self.command_queue.put_nowait, ('enter', self.text_input)
            )

        elif command == 'r':
            logging.info("InputHandler: Handling 'r' command.")
            self.loop.call_soon_threadsafe(
                self.command_queue.put_nowait, ('r', self.text_input)
            )

        elif command == 'q':
            logging.info("InputHandler: Handling 'q' command.")
            self.loop.call_soon_threadsafe(
                self.command_queue.put_nowait, ('q', None)
            )
            self.running = False

        elif isinstance(command, str):
            self.text_input += command
            logging.info(f"InputHandler: Text input updated to: '{self.text_input}'")

    def start(self):
        """
        Starts the input processing loop.
        """
        logging.info("Starting InputHandler.")
        self.running = True
        self.loop.create_task(self.process_commands())

    def stop(self):
        """
        Stops the input processing loop.
        """
        logging.info("Stopping InputHandler.")
        self.running = False