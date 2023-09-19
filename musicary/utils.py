from django.conf import settings

def log_message(message):
    message_length = len(message)
    line = '-' * message_length
    
    print(line + '\n' + message + '\n' + line)
    
def log_message_debug(message):
    if settings.DEBUG:
        log_message(message)