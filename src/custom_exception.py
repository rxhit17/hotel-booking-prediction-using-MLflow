import traceback

class CustomException(Exception):
    def __init__(self, error_message, error_detail):
        super().__init__(error_message)
        self.error_message = self.get_detailed_message(error_message, error_detail)

    @staticmethod
    def get_detailed_message(error_message, error_detail):
        tb = traceback.extract_tb(error_detail.__traceback__)
        if tb:
            file_name = tb[-1].filename
            line_number = tb[-1].lineno
        else:
            file_name = "Unknown"
            line_number = "Unknown"

        return f"Error in {file_name}, line {line_number}: {error_message} | Cause: {str(error_detail)}"

    def __str__(self):
        return self.error_message
