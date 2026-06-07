class AuthenticationError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class InvalidRefreshTokenError(Exception):
    pass