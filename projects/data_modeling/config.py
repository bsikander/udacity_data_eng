from logging.config import dictConfig
import logging
import os
import sys
import structlog


def add_logger_lineno(logger, method_name, event_dict):
    """Add the log record line number to the event dict."""
    record = event_dict.get("_record")
    if record is None:
        event_dict["lineno"] = logger.lineno
    else:
        event_dict["lineno"] = record.lineno
    return event_dict


def logging_setup():
    """Set up logging."""
    default_formatter = "colored"
    log_level = os.environ.get("LOG_LEVEL", logging.INFO)

    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=log_level)

    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")

    pre_chain = [
        # Add the log level and a timestamp to the event_dict if the log entry
        # is not from structlog.
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        add_logger_lineno,
        timestamper,
    ]

    log_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {},
        "handlers": {},
        "loggers": {},
    }

    log_dict["formatters"]["plain"] = {
        "()": structlog.stdlib.ProcessorFormatter,
        "processor": structlog.processors.JSONRenderer(),
        "foreign_pre_chain": pre_chain,
    }

    log_dict["formatters"]["colored"] = {
        "()": structlog.stdlib.ProcessorFormatter,
        "processor": structlog.dev.ConsoleRenderer(colors=True),
        "foreign_pre_chain": pre_chain,
    }

    log_dict["handlers"]["default"] = {
        "level": log_level,
        "class": "logging.StreamHandler",
        "formatter": default_formatter,
    }
    log_dict["loggers"][""] = {
        "handlers": ["default"],
        "level": log_level,
        "propagate": True,
    }

    dictConfig(log_dict)

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            timestamper,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def instrument():
    """Set up all observability configurations."""
    logging_setup()
