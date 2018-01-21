import logging.config

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'maxBytes': 1024 * 1024 * 10,  # 当达到10MB时分割日志
            'backupCount': 10,  # 最多保留10份文件
            'delay': True,  # If delay is true, file opening is deferred until the first call to emit
            'filename': '../log/sample-site.log',
            'formatter': 'verbose',
        },
        'file2': {
            'level': 'DEBUG',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'maxBytes': 1024 * 1024 * 10,  # 当达到10MB时分割日志
            'backupCount': 10,  # 最多保留10份文件
            'delay': True,  # If delay is true, file opening is deferred until the first call to emit
            'filename': 'sample-site2.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': 0,
        },
        'root2': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': 1,
        },
    },
})
logger = logging.getLogger("")
logger.info("==== Here is a very exciting log message")
logger = logging.getLogger("root")
logger.info("==== Here is a very exciting log message")

logger = logging.getLogger("root2")
logger.info("==== Here is a very exciting log message2")
