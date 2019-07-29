class NoAnswer(Exception):
    def __init__(self, message='Не получен ответ от пользователя'):
        """
        :param message:
        """
        super().__init__(message)
