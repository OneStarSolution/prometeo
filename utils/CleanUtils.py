class CleanUtils:
    @staticmethod
    def clean_phone(raw_phone):
        return ''.join([char for char in raw_phone if char.isdigit()])
