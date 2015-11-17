from scrapy import log


def info(message):
	log.msg(message, level=log.INFO)


def debug(message):
	log.msg(message, level=log.DEBUG)


def warn(message):
	log.msg(message, level=log.WARNING)


def error(message):
	log.msg(message, level=log.ERROR)


def critical(message):
	log.msg(message, level=log.CRITICAL)
