from constants.field_mappings import SERVER_FIELDS

class InputHelpers:
    """Helper methods for admin input prompts."""

    @staticmethod
    def gather_external_server_update_input() -> dict:
        """Prompt for external server update fields and return a dict of non-empty values."""
        name = input("New Name (leave blank to keep unchanged): ").strip()
        base_url = input("New Base URL (leave blank to keep unchanged): ").strip()
        api_key = input("New API Key (leave blank to keep unchanged): ").strip()
        is_active_input = input("Set Active? (yes/no/leave blank to keep unchanged): ").strip().lower()

        data = {}
        if name:
            data[SERVER_FIELDS["name"]] = name
        if base_url:
            data[SERVER_FIELDS["base_url"]] = base_url
        if api_key:
            data[SERVER_FIELDS["api_key"]] = api_key
        if is_active_input == "yes":
            data[SERVER_FIELDS["is_active"]] = True
        elif is_active_input == "no":
            data[SERVER_FIELDS["is_active"]] = False

        return data

    @staticmethod
    def get_blocked_keyword_input(prompt: str = "Enter keyword to block: ") -> str:
        """Prompt the user to enter a keyword to block and return it."""
        return InputHelpers.get_non_empty_input(prompt)

    @staticmethod
    def get_non_empty_input(prompt: str) -> str:
        """Prompt until a non-empty input is received."""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Input cannot be empty.")

    @staticmethod
    def get_valid_number_input(prompt: str) -> int:
        """Prompt until a valid integer is entered. Returns the integer value."""
        while True:
            value = input(prompt).strip()
            if value.isdigit():
                return int(value)
            print("Please enter a valid number.")