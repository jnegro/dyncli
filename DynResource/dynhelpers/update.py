import logging
from pprint import pprint, pformat

from dynhelper import DynHelper
from .. import DynRestResource


class Update(DynHelper):

    
    #inherit DynectRest init
    def __init__(self, user, password, account, logger=None):
        super(Update, self).__init__(user, password, account, logger)
        
        #if logger name is specified, log commands will log to it
        if logger is not None:
            parent_logger = logger
            global log
            log = logging.getLogger('{0}.{1}'.format(parent_logger,__name__))
        #if not, set up a NullHandler so log commands don't error
        else:
            log = logging.getLogger('{0}'.format(__name__))
            null_handler = logging.NullHandler()
            log.addHandler(null_handler)

    def do(self, resource, arg_dict, auto_publish=True):

        log.debug('Update request started')
        
        #Sort out fqdn, zone, and hostname provided
        arg_dict = self._get_zone_from_fqdn(arg_dict)
        
        self._log_request_info(resource, arg_dict)
        
        log.debug("Finding records that match fqdn {0}".format(arg_dict['fqdn']))
        dyn = DynRestResource(self.user, self.password, self.account, self.logger)
        result_list = dyn.do(resource, 'list', arg_dict, auto_publish)
        
        if 'update_all' in arg_dict.keys():
            log.info('update_all flag detected')
            update_all = arg_dict['update_all']
        else:
            update_all = False
            
        if len(result_list['data']) > 1 and update_all is False:
            log.warning('Multiple records found, please specify the ID with the -i flag or use the --update_all flag cautiously')
            output = result_list
        
        elif len(result_list['data']) == 1 or update_all is True:
            log.debug('Either one record was found, or update_all flag was used')

            output = {}

            for record in result_list['data']:
                output[record] = {}
                
                get_arg_dict = arg_dict.copy()
                
                get_arg_dict['record_id'] = record.rsplit('/')[-1]
                log.debug('Requesting detailed data for existing record')
                result_get = dyn.do(resource, 'get', get_arg_dict, auto_publish)
                orig_dict = result_get['data'].copy()
                
                update_arg_dict = get_arg_dict.copy()
                update_arg_dict['resource'] = resource
                
                log.debug('Sending update now')
                result_update = dyn.do(resource, 'update', update_arg_dict, auto_publish)
                
                output[record]['status'] = result_update['status']
                output[record]['data'] = {
                    'original_record': orig_dict,
                    'result': result_update,
                }
        
        log.info("Request completed")
        log.info(pformat(output))
        
        return output
