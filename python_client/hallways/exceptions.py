class HallwaysException(Exception):
    '''Parent for other hallways Exceptions, only used to except any hallways exception, never raised'''
    pass

class HallwaysServerException(HallwaysException):
    '''Exception while talking to the server (above the application layer)'''
    pass

class WiFiScannerException(HallwaysException):
    '''Exception in scanning for WiFi signal strengths'''
    pass

__all__ = ['HallwaysException', 'HallwaysServerException', 'WiFiScannerException']
