import logging
import re
import time
from pprint import pprint, pformat

from dynhelper import DynHelper
from .. import DynRestResource
from ..dynresourcemap import DYN_API_MAP

class Search(DynHelper):
    
    #inherit DynectRest init
    def __init__(self, user, password, account, logger=None):
        super(Search, self).__init__(user, password, account, logger)
        
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

        log.debug('Search request started')
        
        self._log_request_info(resource, arg_dict)
        
        if arg_dict['helper_action'] == 'records':
            log.debug('Searching Records')
            
            dyn = DynRestResource(self.user, self.password, self.account, self.logger)
            
            # get zone records
            zone_dict = {}
            ('Getting zone data')
            
            zone_query_dict = arg_dict
            zone_query_dict['detail'] = True
            zone_query_dict['resource'] = 'AllRecord'
            
            output = {}
            
            # Apply any specified filter args to output
            filter_args = ['record_types', 'datafields', 'ttl_min', 'ttl_max', ]
            
            for zone in arg_dict['zones']:
                output[zone] = {}
                zone_query_dict['zone'] = zone
                zone_data = dyn.do('AllRecord', 'list', zone_query_dict, auto_publish)
                output[zone]['status'] = zone_data['status']
                output[zone]['job_id'] = zone_data['job_id']
                output[zone]['msgs'] = zone_data['msgs']
                output[zone]['data'] = {}
            
                if any(x in arg_dict.keys() for x in filter_args):
                        
                    if 'record_types' in arg_dict.keys():
                        log.debug("record_types arg detected")
                        
                        record_types = []
                        for record_type_arg in arg_dict['record_types']:
                            record_type_arg = self.get_record_type(record_type_arg, 'dataset')
                            record_types.append(record_type_arg)
                            
                    else:
                        record_types = zone_data['data'].keys()
                        
                    for record_type in record_types:
                        
                        output[zone]['data'][record_type] = []
                        
                        try:
                        
                            for record in zone_data['data'][record_type]:
                                
                                if ('ttl_min' in arg_dict.keys()) and ('ttl_max' in arg_dict.keys()):
                                    if (int(record['ttl']) > int(arg_dict['ttl_min'])) and (int(record['ttl']) < int(arg_dict['ttl_max'])):
                                        output[zone]['data'][record_type].append(record)
                                    
                                elif 'ttl_min' in arg_dict.keys():
                                    if int(record['ttl']) > int(arg_dict['ttl_min']):
                                            log.debug("ttl for {0}, ttl:{1} is less than {2}, filtering".format(
                                                record['fqdn'], record['ttl'], arg_dict['ttl_min']))
                                            output[zone]['data'][record_type].append(record)
                                    else:
                                        log.debug("ttl for {0}, ttl:{1} is greater than {2}, keeping".format(
                                            record['fqdn'], record['ttl'], arg_dict['ttl_min']))
                                    
                                elif 'ttl_max' in arg_dict.keys():                    
                                    if int(record['ttl']) < int(arg_dict['ttl_max']):
                                            log.debug("ttl for {0}, ttl:{1} is greater than {2}, filtering".format(
                                                record['fqdn'], record['ttl'], arg_dict['ttl_max']))
                                            output[zone]['data'][record_type].append(record)
                                    else:
                                        log.debug("ttl for {0}, ttl:{1} is less than {2}, keeping".format(
                                            record['fqdn'], record['ttl'], arg_dict['ttl_max']))
                                            
                                else:
                                    output[zone]['data'][record_type].append(record)
                                    
                        except KeyError:
                            log.info('No {0} found'.format(record_type))
                        except:
                            raise
                                        
                else:
                    output[zone]['data'] = zone_data['data']
                                    
            return output
            
        elif arg_dict['helper_action'] == 'changelog':

            log.info('changelog action specified')
            dyn = DynRestResource(self.user, self.password, self.account, self.logger)
            
            if 'zones' not in arg_dict.keys():
                log.info('Zones not specified in command, using all zones')
                zones = dyn.do('Zone', 'list', arg_dict, auto_publish)
                zones_list = []
                for zone_link in zones['data']:
                    zones_list.append(zone_link.rsplit('/')[-2])
            else:
                log.debug('Zones specified in command')

            if 'age' not in arg_dict.keys():
                log.info('No log age defined')
                arg_dict['age'] = 0

            if 'limit' not in arg_dict.keys():
                log.info('No log entry limit defined, using last 50 entries')
                arg_dict['limit'] = 50
            else:
                log.debug('Limit of log entries specified at {0}'.format(arg_dict['limit']))

            log.debug('Getting zone notes')
            
            zone_notes = {}
            for zone in arg_dict['zones']:
                arg_dict['zone'] = zone
                arg_dict['resource'] = 'ZoneNoteReport'
                zone_notes[zone] = dyn.do('ZoneNoteReport', 'get', arg_dict, auto_publish)
            log.info('Zone notes retrieved successfully')

            if arg_dict['age'] == 0:
                cutoff = 0
                log.debug('Cutoff age is 0')
            else:
                epoch_age = int(arg_dict['age']) * 60 * 60
                cutoff = int(time.time()) - epoch_age
                log.debug('Cutoff age is {0}'.format(cutoff))
            
            output = {}
            for zone in arg_dict['zones']:
                
                output[zone] = {}
                output[zone]['data'] = []
                output[zone]['msgs'] = zone_notes[zone]['msgs']
                output[zone]['status'] = zone_notes[zone]['status']
                output[zone]['job_id'] = zone_notes[zone]['job_id']
                
                if zone_notes[zone]['data'] is not None:
                    log.debug('Data was found')
                    for note in zone_notes[zone]['data']:
                        log.debug("Analyzing zone note {0}".format(note['timestamp']))
                        if int(note['timestamp']) > int(cutoff):
                            log.debug("Note with timestamp {0} was newer than cutoff {1}, appending output".format(note['timestamp'], cutoff))
                            log.debug("log items for output: {0}".format(len(output[zone]['data'])))
                            output[zone]['data'].append(note)
                        else:
                            log.debug("Note with timestamp {0} older than cuttoff {1}, skipping".format(note['timestamp'], cutoff))

            return output
        
        elif arg_dict['helper_action'] == 'zones':
            log.info('Search zones request received')
            log.debug('Getting zone list')
            arg_dict['resource_action'] = 'Zone'
            arg_dict['resource'] = 'Zone'
            dyn = DynRestResource(self.user, self.password, self.account, self.logger)
            output = dyn.do('Zone', 'list', arg_dict, self.logger)

            log.debug('Zone list received')

            return output
        
        elif arg_dict['helper_action'] == 'services':

            log.info('Search services request received')
            arg_dict['resource'] = arg_dict['service_type']
            
            dyn = DynRestResource(self.user, self.password, self.account, self.logger)

            log.debug('Making query to dyn')
            output = dyn.do(arg_dict['service_type'], 'list', arg_dict, self.logger)
            log.info('Dyn Search Query result received')
            
            return output