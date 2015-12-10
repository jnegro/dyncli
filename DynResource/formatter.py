import logging
import re
from pprint import pformat


#if logger name is specified, log commands will log to it
class Formatter(object):
    
    def __init__(self,logger=None):
        
        global log
        if logger is not None:
            parent_logger = logger
            log = logging.getLogger('{0}.{1}'.format(parent_logger,__name__))
        #if not, set up a NullHandler so log commands don't error
        else:
            log = logging.getLogger('{0}'.format(__name__))
            null_handler = logging.NullHandler()
            log.addHandler(null_handler)

    def _leading_spaces(self,level, step=4):
        space = ''
        level_counter = level * step
        while level_counter > 0:
            space = " {0}".format(space)
            level_counter = level_counter-1
            
        return space
    
    def standard(self,result, output=[], level=0, last_key=None, last_type=None):
        log.debug('Starting output_formatter loop')
        
        if isinstance(result, dict):
            log.debug('Dictionary instance detected')
            if result and (last_type == 'dict'):
                line = "{0}{1}:".format(self._leading_spaces(level),last_key)
                output.append(line)
                log.debug("Dictionary detected inside of Dictionary")
                log.debug('Current level: {0}'.format(level))
                level = level+1
    
            for key in result.keys():
                output = self.standard(result[key], output, level, key, 'dict')
                
        elif isinstance(result, list):
            log.debug('List instance detected')
            
            if result: 
                if last_type == 'dict':
                    line = "{0}{1}:".format(self._leading_spaces(level),last_key)
                    log.debug("Dictionary detected inside of List")
                    output.append(line)
                    level = level+1
    
                divider_line = "----------------"
                level_counter = level
                while level_counter > 0:
                    divider_line = "    {0}".format(divider_line)
                    level_counter = level_counter-1
        
                for item in result:
                    output.append(divider_line)
                    output = self.standard(item, output, level, None, 'list')
                    
                output.append(divider_line)
        
        else:
            log.debug('String detected')
            
            if last_type == 'dict':
                line = "{0}{1}: {2}".format(self._leading_spaces(level),last_key, result)
                output.append(line)
            elif last_type == 'list':
                line = "{0}{1}".format(self._leading_spaces(level),result)
                output.append(line)
            else:
                line = "{0}{1}".format(self._leading_spaces(level),result)
                output.append(line)
                
            #log.debug(pformat(output))
        
        return output
        

    def _flatten_headers(self, results, headers=[], parent=None):
        
        log.debug('Flattening headers')
        log.debug('Current data: {0}'.format(results))
        
        if parent is None:
            log.debug('Parent is None')
            if isinstance(results, dict):
                log.debug('Data is a dictionary')
                for key in results.keys():
                    log.debug('Recursing key {0}'.format(key))
                    log.debug('headers gathered: {0}'.format(headers))
                    headers = self._flatten_headers(results[key], headers, key)
            elif isinstance(results, list):
                log.debug('Data is a list')
                for item in results:
                    log.debug('Recusing List')
                    log.debug('headers gathered: {0}'.format(headers))
                    headers = self._flatten_headers(item, headers, None)
        else:
            log.debug('Parent is {0}'.format(parent))
            if isinstance(results, dict):
                log.debug('Data is a dictionary')
                for key in results.keys():
                    log.debug('Recursing key {0}'.format(key))
                    log.debug('headers gathered: {0}'.format(headers))
                    headers = self._flatten_headers(results[key], headers, key)
            elif isinstance(results, list):
                for item in results:
                    headers = self._flatten_headers(item, headers, None)
            else:
                log.debug('String detected: {0}'.format(parent))
                headers.append("{0}".format(parent))
        
        return headers
    
    def _collect_records(self, results, records=[], parent=None):
        
        log.debug('Collecting records from results')
        
        if parent is None:
            log.debug('Parent is None')
            if isinstance(results, dict):
                log.debug('Data is a dictionary')
                for key in results.keys():
                    log.debug('Recursing key {0}'.format(key))
                    log.debug('{0} records collected'.format(len(records)))
                    records = self._collect_records(results[key], records, key)
            elif isinstance(results, list):
                for item in results:
                    log.debug('{0} records collected'.format(len(records)))
                    records = self._collect_records(item, records, None)
        else:
            log.debug('Parent is {0}'.format(parent))
            if isinstance(results, dict):
                log.debug('Data is a dictionary')
                for key in results.keys():
                    log.debug('Recursing key {0}'.format(key))
                    log.debug('{0} records collected'.format(len(records)))
                    records = self._collect_records(results[key], records, key)
            elif isinstance(results, list):
                log.debug('List detected')
                for item in results:
                    log.debug('{0} records collected'.format(len(records)))
                    records.append(item)
                
        return records
        
    def _quote_data(self, value, delimiter):
        
        if isinstance(value, unicode):
            log.debug("String instance detected for value, testing for quoting")
            log.debug(value)
            quote = '\"'
            if re.search('\"', "{0}".format(value)):
                log.debug("double quotes found, switching to single quotes")
                quote = "\'"
            
            #quote spaces no matter what
            if re.search(' ', "{0}".format(value)):
                log.debug("Space detected in value, quoting")
                value = "{0}{1}{0}".format(quote,value)
            
            elif delimiter == ",":
                log.debug("Delimiter is a comma")
                if re.search(",", "{0}".format(value)):
                    log.debug("Comma detected in value, quoting")
                    value = """{0}{1}{0}""".format(quote,value)
        else:
            output = value
                    
        return value
    
    def csv(self, results, arg_dict, delimiter=','):
        log.debug('CSV printing format detected')
        
        if 'datafields' in arg_dict.keys():
            log.debug("datafields set at command prompt")
            header_set = set(arg_dict['datafields'])
        else:
            log.debug("datafields not specified")
            all_headers = []
            for zone in results.keys():
                headers = self._flatten_headers(results[zone]['data'])
                all_headers.extend(headers)
                
            header_set = set(all_headers)
            log.info('No datafields specified.  Using all')
        
        output = []
        
        if 'noheaders' in arg_dict.keys():
            if arg_dict['noheaders'] is not True:
                log.info('Noheaders option not detected')
                line = ''
                
                for header in header_set:
                    if line == '':
                        line = "{0}".format(header)
                    else:
                        line = "{0}{1}{2}".format(line, delimiter, header)
                output.append(line)
        
        records = []
        for zone in results.keys():
            log.debug('Collecting records for {0}'.format(zone))
            records.extend(self._collect_records(results[zone]['data']))
        
        for record in records:
            line = ''
            for header in header_set:
                value = ''
                for field in record.keys():
                    if isinstance(record[field], dict):
                        log.debug("Field is a dictionary")
                        for subfield in record[field].keys():
                            if header == subfield:
                                log.debug('Header {0} found in subfield {1}'.format(header, subfield))
                                value = self._quote_data(record[field][subfield], delimiter)
                            else:
                                log.debug('Header {0} not found in subfield {1}'.format(header, subfield))
                    else:
                        if header == field:
                            log.debug('Header {0} found in field {1}'.format(header, field))
                            value = self._quote_data(record[header], delimiter)
                        else:
                            log.debug('Header {0} not found in field {1}'.format(header, field))
                
                if line == '':
                    line = "{0}".format(value)
                else:
                    line = "{0}{1}{2}".format(line, delimiter, value)
                        
            output.append(line)
                
        return output
        
    def as_list(self, results, arg_dict):
        log.debug('as-list function has been activated')
        output = self.csv(results, arg_dict, ' ')
        
        return output
        
    def zones_as_list(self, results, arg_dict):
        
        log.debug('Getting list of zones')
        zones = []
        
        for zonelink in results['data']:
            zones.append(zonelink.rsplit('/')[-2])
            
        return zones
