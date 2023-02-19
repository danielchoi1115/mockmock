from .error_dto import ErrorDto


class ErrorHandler():
    def send_error(self, dto: ErrorDto):
        for k, v in vars(dto).items():
            dto.__setattr__(k, str(v))
        with open('error.txt', 'a', encoding='utf8') as f:
            f.write(str(dto.json())+'\n')


errorHandler = ErrorHandler()
