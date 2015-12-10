import logging
from pprint import pprint, pformat

from dynhelper import DynHelper
from .. import DynRestResource


class Delete(DynHelper):
    
    #inherit DynectRest init
    def __init__(self, user, password, account, logger=None):
        super(Delete, self).__init__(user, password, account, logger)
        
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

        log.debug('Delete request started')
        
        #Sort out fqdn, zone, and hostname provided
        arg_dict = self._get_zone_from_fqdn(arg_dict)
        
        self._log_request_info(resource, arg_dict)
        
        log.debug("Finding records that match fqdn {0}".format(arg_dict['fqdn']))
        dyn = DynRestResource(self.user, self.password, self.account, self.logger)
        result_list = dyn.do(resource, 'list', arg_dict, auto_publish)
        
        if 'delete_all' in arg_dict.keys():
            log.info('delete_all flag detected')
            update_all = arg_dict['delete_all']
        else:
            update_all = False
            
        if len(result_list['data']) > 1 and delete_all is False:
            log.warning('Multiple records found, please specify the ID with the -i flag or use the --update_all flag cautiously')
            output = result_list
        
        elif len(result_list['data']) == 1 or delete_all is True:
            output = []
            log.debug('Either one record was found, or delete_all flag was used')

            for record in result_list['data']:
                
                arg_dict['record_id'] = record.rsplit('/')[-1]
                log.debug('Deleting record {0}'.format(arg_dict['record_id']))
                result_delete = dyn.do(resource, 'delete', arg_dict, auto_publish)
        
                output.append({
                    'result': result_delete,
                })
        
        log.info("Request completed")
        log.debug(pformat(output))
        
        return output