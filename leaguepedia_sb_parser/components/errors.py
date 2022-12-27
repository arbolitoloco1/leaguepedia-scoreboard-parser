class EventCannotBeLocated(KeyError):
    def __str__(self):
        return "The event page for this game cannot be located!"


class InvalidGameSource(ValueError):
    def __init__(self, source):
        self.source = source

    def __str__(self):
        return f"{self.source} is not a valid source!"


class InvalidInput(ValueError):
    def __str__(self):
        return "The input format is invalid!"
