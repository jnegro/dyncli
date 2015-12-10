import logging
import re

from dynhelpermap import DYN_HELPERS, SUPPORTED_RECORD_TYPES

class DynHelper(object):

    def __init__(self,user,password,account,logger=None):
        
        self.user = user
        self.password = password
        self.account = account
        self.logger = logger
    
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
            
    def _get_zone_from_fqdn(self,arg_dict):
        
        log.debug('Getting Zone from FQDN')
        
        if 'zone' not in arg_dict.keys():
            log.debug('No zone provided, getting zone from FQDN')
            arg_dict['zone'] = "{0}.{1}".format(arg_dict['fqdn'].rsplit('.')[-2],arg_dict['fqdn'].rsplit('.')[-1])
            log.info('Zone {0} assumed from FQDN {1}'.format(arg_dict['zone'], arg_dict['fqdn']))
                
        return arg_dict
        
    def _get_zone_from_zonelink(self, zonelinks, arg_dict):
        
        output = []
        log.debug('Getting zone name from zonelinks list')
        for zonelink in zonelinks:
            zone = "{0}".format(zonelink.rsplit('/')[-2])
            output.append(zone)
            log.debug('Zone {0} found in zonelink {1}'.format(zone, zonelink))
            
        return output
        
    def _redact_password(self, arg_dict):
        
        log.debug('Redacting password from arg_dict for logging')
        new_arg_dict = arg_dict
        
        if 'password' in arg_dict.keys():
            new_arg_dict['password'] = "********"
            log.debug('Password redacted')
        
        return new_arg_dict
        
    def _log_request_info(self, request, arg_dict):
        
        log.debug("Get request info")
        arg_list = arg_dict.keys()
        log_data = 'New {0} Request: '.format(request)
        
        for arg_item in arg_list:
            if arg_item not in ['user', 'password', 'account', 'helper_action', 'logger_name' ]:
                log_data = "{0}{1}={2}, ".format(log_data, arg_item, arg_dict[arg_item])
                
        log.info(log_data)
        
    def get_record_type(self, original, new_format):
        
        log.debug('Getting record type')
        format_choices = ['short', 'dataset', 'resource', ]
        if new_format not in format_choices:
            log.critical("Invalid new_format choice.  Must be 'short', 'dataset', or 'resource'")
        
        # long record_type for datasets
        long_name_dataset = ("{0}_record".format(x.lower()) for x in SUPPORTED_RECORD_TYPES)
        # long resource_type for resource calls
        long_name_resource = ("{0}Record".format(x.upper()) for x in SUPPORTED_RECORD_TYPES)
        
        if original in SUPPORTED_RECORD_TYPES:
            original_format = 'short'
            log.info('Short record type detected')
        elif original in long_name_dataset:
            log.info('Long record type detected type')
            original_format = 'dataset'
        elif original in long_name_resource:
            log.info('converted to short long range type')
            original_format = 'resource'
        
        if original_format == new_format:
            log.debug('Requested record_type is already in desired format')
            return original
        
        else:
            if new_format == 'short':
                if original_format == 'dataset':
                    output = original.split('_')[0].upper()
                    log.debug("Converted to short format, {0}".format(output))
                elif original_format == 'resource':
                    output = re.search('^[A-Z]*', original).group(0)
                    output = re.sub('R$','$', output)
                    log.debug("Converted to short format, {0}".format(output))
            elif new_format == 'dataset':
                if original_format =='short':
                    output = "{0}_records".format(original.lower())
                    log.debug("Converted to dataset format, {0}".format(output))
                elif original_format == 'resource':
                    short = re.sub('Record','_records', original)
                    output = short.lower()
                    log.debug("Converted to dataset format, {0}".format(output))
            elif new_format == 'resource':
                if original_format == 'short':
                    output = '{0}Record'.format(original)
                    log.debug("Converted to resource format, {0}".format(output))
                elif output_format == 'dataset':
                    short = re.match('^[A-Z]*_', original).group(0).upper()
                    output = '{0}Record'.format(original)
                    log.debug("Converted to resource format, {0}".format(output))
        
            return output
