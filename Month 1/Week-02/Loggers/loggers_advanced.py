#In this code I am trying to implement the loggers using python in a more advanced example more of a production kind of example

import logging
from logging.handlers import RotatingFileHandler

#Create logger 
logger = logging.getLogger("MyAppLogger")
logger.setLevel(logging.DEBUG)

#implementing Formatter
formatter = logging.Formatter('%(asctime)s | %(name)s | %levelname)s | %(message)s')

#implementing the Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Implementing File Handler with Rotation
file_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024, backupCount=3)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


#Adding handlers to the logger

logger.addHandler(console_handler)
logger.addHandler(file_handler)

#Implementing some Example functions to demonstrate the logging

def divide(a,b):
    try:
        logger.info(f"Dividing {a} by {b}")
        result = a / b
        logger.debug(f"Result of Division: {result}")
        return result
    except ZeroDivisionError:
        logger.exception("Attempted to divide by zero!")

# Testing the logger with some function calls

logger.info("Application Started")

divide(10, 2)
divide(10,0)

logger.info("Application Finished")

