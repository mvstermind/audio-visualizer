class InvalidFileFormatError(Exception):
    """Error raised when invalid file extension is provided"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
