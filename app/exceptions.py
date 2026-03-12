class HueClientError(Exception):
    pass


class HueBridgeNotConfiguredError(HueClientError):
    pass


class HueBridgeConnectionError(HueClientError):
    pass


class HueBridgeAuthenticationError(HueClientError):
    pass


class HueResourceNotFoundError(HueClientError):
    pass
