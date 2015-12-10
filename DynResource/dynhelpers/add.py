import logging
from pprint import pprint, pformat

from dynhelper import DynHelper
from .. import DynRestResource


class Add(DynHelper):
    
    #inherit DynectRest init
    def __init__(self, user, password, account, logger=None):
        super(Add, self).__init__(user, password, account, logger)
        
        #if logger name is specified, log commands will log to it
        if logger is not None:
            parent_logger = logger
            global log
            log = logging.getLogger('{0}.{1}'.format(parent_logger,__name__))
        #if not, set up a NullHandler so log commands don't error
        else:
            log = logging.getLogger('{0}'.format(__name__))
            null_handler = logging.NullHandler()
            self.log.addHandler(null_handler)

    def do(self, resource, arg_dict, auto_publish=True):

        log.debug('Add request started')
        
        #Sort out fqdn, zone, and hostname provided
        arg_dict = self._get_zone_from_fqdn(arg_dict)
        
        self._log_request_info(resource, arg_dict)
        
        dyn = DynRestResource(self.user, self.password, self.account, self.logger)
        result = dyn.do(resource, 'add', arg_dict, auto_publish)
        
        log.info("Request completed")
        output = result
        log.debug(pformat(output))
        
        return output