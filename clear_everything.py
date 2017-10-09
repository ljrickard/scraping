#!/usr/bin/env python3
import logging
from components.data_access.data_access import DataAccess

logging.basicConfig(level=logging.INFO, format='%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s') 
logger = logging.getLogger(__name__)

dataAccess = DataAccess(False)
dataAccess.clear_all_data()
