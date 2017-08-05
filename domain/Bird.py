class Bird:
    def __init__(self, filename, name, order, difficulty):
        self.__filename = filename
        self.__name = name
        self.__order = order
        self.__difficulty = int(difficulty)

    def get_filename(self):
        return self.__filename

    def get_name(self):
        return self.__name

    def get_order(self):
        return self.__order

    def get_difficulty(self):
        return self.__difficulty

    def __str__(self) -> str:
        return '%s[%s]' % (type(self).__name__, ', '.join('%s=%s' % item for item in vars(self).items()))
