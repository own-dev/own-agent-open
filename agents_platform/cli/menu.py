"""
Modified version of https://pypi.org/project/Menu/3.1.0/
Beside original functionality it allows to pass data to callbacks
"""

import os
from typing import List, Tuple, Any, Callable


class Menu(object):
    """
    Basic functionality for menu-based command line interface (CLI)

    Looks like that:
    > Title
    > Message
    > list of indexed Options
    """

    def __init__(self,
                 options: List[Tuple] = None, title: str = None, message: str = None,
                 prompt: str = ">>>",
                 refresh: Callable = lambda: None):
        if options is None:
            options = []
        self.options = None
        self.title = None
        self.is_title_enabled = None
        self.message = None
        self.is_message_enabled = None
        self.refresh = None
        self.prompt = None
        self.is_open = None

        self.set_options(options)
        self.set_title(title)
        self.set_title_enabled(True)
        self.set_message(message)
        self.set_message_enabled(message is not None)
        self.set_prompt(prompt)
        self.set_refresh(refresh)

    def set_options(self, options: List[Tuple]):
        """Sets menu's items/options"""
        # Save previous options in case something goes wrong
        original = self.options

        # Generate new options
        self.options = []
        try:
            for option in options:
                if not isinstance(option, tuple):
                    raise TypeError(option, "option is not a tuple")
                if len(option) != 2 and len(option) != 3:
                    raise ValueError(option, "option is not of length 2 or 3")
                if len(option) == 3:
                    self.add_option(option[0], option[1], option[2])
                else:
                    self.add_option(option[0], option[1])
        except (TypeError, ValueError) as error:
            self.options = original
            raise error

    def set_title(self, title: str) -> None:
        """Sets the menu's title to be displayed (above the message and the list of items/options"""
        self.title = title

    def set_title_enabled(self, is_enabled: bool) -> None:
        """Enables menu's title"""
        self.is_title_enabled = is_enabled

    def set_message(self, message: str) -> None:
        """Sets the message to be displayed once menu appears (above the list of items/options)"""
        self.message = message

    def set_message_enabled(self, is_enabled: bool) -> None:
        """Enables menu's messages"""
        self.is_message_enabled = is_enabled

    def set_prompt(self, prompt: str) -> None:
        """Just sets the prompt for the input"""
        self.prompt = prompt

    def set_refresh(self, refresh):
        """Sets the callback to refresh the menu"""
        if not callable(refresh):
            raise TypeError(refresh, "refresh is not callable")
        self.refresh = refresh

    def add_option(self, name: str, handler: Callable, kwargs: Any = None) -> None:
        """
        Adds an item for the menu; it can have
        :param name: Option's name/title to display
        :param handler: Option's callback
        :param kwargs: # TODO: Refactor it to be real **kwargs
        :return: Nothing
        """
        if not callable(handler):
            raise TypeError(handler, "handler is not callable")
        self.options += [(name, handler, kwargs)]

    def open(self) -> None:
        """
        Opens the menu
        :return: Nothing
        """
        self.is_open = True
        while self.is_open:
            # Refresh the menu
            self.refresh()

            # Get the callback
            callback = self.input()

            if not isinstance(callback, tuple):
                print('It should not happen!..')
            if callback[0] == Menu.CLOSE:
                callback = self.close
            print()

            # If it's a plain funciton/callback, just call it
            if callable(callback):
                callback()
            # If callback has parameters, call the function with them
            elif callback[1] is not None:
                callback[0](callback[1])
            # Otherwise deep/down-grade until it's a regular callback tuple
            else:
                while isinstance(callback[0], tuple):
                    callback = callback[0]
                callback[0]()

    def close(self) -> None:
        """
        "Closes" the menu
        """
        self.is_open = False

    def show(self) -> None:
        """
        Clears the screen, lists the menu-items (options)
        :return:
        """
        # Clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Set title and message if needed
        if self.is_title_enabled:
            print(self.title)
            print()
        if self.is_message_enabled:
            print(self.message)
            print()

        # Show all the options
        for (index, option) in enumerate(self.options):
            print(str(index + 1) + ". " + option[0])
        print()

    def input(self) -> Tuple[Callable, Any]:
        """
        Shows the menu, gets a new index from input, and returns corresponding callback with data
        :return: tuple(callback, callback_data)
        """
        if not self.options:
            return (Menu.CLOSE, None)
        try:
            self.show()
            # Get user's input
            index = int(input(f'{self.prompt} ')) - 1

            # Get corresponding callback
            callback = self.options[index][1]
            callback_data = self.options[index][2]

            return (callback, callback_data)

        # Get input once more
        except (ValueError, IndexError):
            return (self.input(), None)

    def CLOSE(self) -> None:
        """
        Allows to recognize when to close the menu
        Think of it like a signal
        """
        pass
