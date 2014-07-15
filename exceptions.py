__author__ = 'stefano'

import endpoints
import httplib

class StazioneNotFoundException(endpoints.ServiceException):
   http_status = httplib.CONFLICT