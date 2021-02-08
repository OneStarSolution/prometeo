class CleanUtils:
    @staticmethod
    def clean_phone(raw_phone):
        phone = raw_phone.replace('\n', '').replace(
            '-', '').replace(' ', '').replace('(', '').replace(')', '').strip()

        if phone.isnumeric():
            return phone
        else:
            raise ValueError(f"{phone} have unvalid characters after cleaning")
