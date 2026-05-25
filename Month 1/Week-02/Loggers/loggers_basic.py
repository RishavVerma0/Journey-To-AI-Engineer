# This code is a basic example of using the logging module in Python.

import logging

#configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Log messages of Different Levels

logging.debug("This is a Debugging Information")
logging.info("Your started Successfully")
logging.warning("This is a warning message")
logging.error("An error Occured!")
logging.critical("Critical issue detected!, Immediate attention required!")