import sys

from manager.core_manager import CommandManager

if __name__ == '__main__':
    command = CommandManager(sys.argv)
    command.execute()