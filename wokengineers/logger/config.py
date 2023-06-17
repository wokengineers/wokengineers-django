from kuantam.logger.consts import FMT
logger_config = {
    'version': 1,

    'disable_existing_loggers': False,

    'formatters': {
        'colored_verbose': {
            '()': 'colorlog.ColoredFormatter',
            'format': FMT,
            'datefmt': "%d-%b-%Y %H:%M:%S",
            'log_colors': {
                'DEBUG':    'yellow',
                'INFO':     'green',
                'WARNING':  'orange',
                'ERROR':    'red',
                'CRITICAL': 'bold_red',
            },
        },
    },


    'handlers': {
        'colored_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored_verbose',
        }
    },

    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['colored_console', ],

        },

        'loggers': {
            '': {
                'level': 'DEBUG',
                'handlers': ['colored_console', ],
            },
        }
    }
}
