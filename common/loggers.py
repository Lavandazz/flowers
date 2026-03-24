LOGGERS_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
            "verbose": {
                "format": "{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}",
                'style': '{'
            },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'basket': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'user': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'order': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'pay': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}