class TransientHTTPError(Exception):
    pass

class PermanentHTTPError(Exception):
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body
        super().__init__("HTTP " + str(status_code) + ": " + body)