import logging
from pprint import pformat
import re
from time import sleep

from dynect import DynectRest
from dynresourcemap import DYN_API_MAP


class DynRestResource(DynectRest):
    
    request_uri = '/REST/'
    logged_in = False
    
    def __init__(self,user,password,account,logger=None):
        
        #inherit DynectRest init
        super(DynRestResource, self).__init__()
        
        self.user = user
        self.password = password
        self.account = account
        
        global log

        #if logger name is specified, log commands will log to it
        if logger is not None:
            parent_logger = logger
            log = logging.getLogger('{0}.{1}'.format(parent_logger,__name__))
        #if not, set up a NullHandler so log commands don't error
        else:
            log = logging.getLogger('{0}'.format(__name__))
            null_handler = logging.NullHandler()
            log.addHandler(null_handler)
    
    
    def login(self):
        try:
            log.debug('Connecting to Dynect API')
            login = self.execute(
                '/REST/Session/', 
                'POST',
                {
                    'customer_name': self.account,
                    'user_name': self.user, 'password': self.password
                }
            )

            if login['status'] != 'success':
                log.critical = 'Login Failed! \n'
            
            self.logged_in = True
            
            log.debug('Login Successful')
            return 0
        except Exception:

            log.exception('Connection to Dynect API failed')
            raise
        

    def _job_status(
        self, 
        job_id, 
        counter=0, 
        standoff=1, 
        max_attempts=10,
        standoff_multiplier=2
    ):

        log.debug('Checking job status')
        sleep(standoff)

        try:
            result = self.execute('/REST/Job/{0}/'.format(job_id), 'GET', {})

            if result['status'] not in ['success', 'failure']:
                log.info('Job status has not returned yet, retrying')
                if counter > max_attempts:
                    log.warning('Maximum attempts to check job status have failed')
                    response = raw_input("Do you wish to continue waiting?[Y/n]")
                    if response in ['n', 'N']:
                        log.critical(
                            'User terminated process after maximum attempts at checking job status were reached.'
                        )
                    else:
                        log.info('User chose to continue waiting on job status')
                        counter = 0
                else:
                    counter += 1

                standoff = standoff * multiplier
                _job_status(counter=counter, standoff=standoff)
                
            log.info('Job status check completed')
            return 0
            
        except Exception, e:
            log.exception('Failed to check job status\n{0}'.format(e))
            raise


    # publish the changes made by the CLI after call automatically
    def _auto_publish(self,zone):
        log.debug('Running Auto Publish')
        result = self.execute('/REST/Zone/{0}/'.format(zone),
                                  'PUT', {'publish': True})
        log.debug('Changes to {0} has been published'.format(zone))
        return 0
        
        
    def do(self, resource, action, arg_dict, auto_publish=True):
        
        log.debug("resource: {0}, action {1}".format(resource, action))
        log_arg_dict = arg_dict
        if 'password' in log_arg_dict.keys():
            log_arg_dict['password'] = "***********"
        log.debug("arg_dict: {0}".format(log_arg_dict))
        
        # get the resource map for the chosen resource
        log.debug("Retrieving resource action map")
        action_map = DYN_API_MAP[resource]['actions'][action]
        log.debug("Loaded action map for {0} resource {1} action".format(resource,action))
        log.debug(pformat(action_map))
        
        #build field lists for resource
        all_fields = []
        
        log.debug("Gathering URL variables")
        url_var_list = []
        if 'url_vars' in action_map.keys():
            for url_var in action_map['url_vars']:
                url_var_list.append(url_var)
                all_fields.append(url_var)
        log.debug("url_var_list: {0}".format(url_var_list))
        
        log.debug("Gathering Option variables")
        if 'options' in action_map.keys():
            option_list = action_map['options'].keys()
        else:
            option_list = []
        log.debug("option list: {0}".format(option_list))
        
        log.debug("Gathering rdata variables")
        if 'rdata' in action_map.keys():
            rdata_list = action_map['rdata'].keys()
        else:
            rdata_list = []
        log.debug("rdata list: {0}".format(rdata_list))
        
        log.debug("all_fields list: {0}".format(all_fields))
        # build out the URL/URI for the api call
        
        log.debug('Building URL for call')
        request_uri = self.request_uri
        for url_var in url_var_list:
            request_uri = "{0}{1}/".format(request_uri,arg_dict[url_var])

        # set the HTTP method used for the call
        method = action_map['method']

        # if the call is a GET method, options become GET params.
        #  Currently only used for 'detail' option
        if (method == 'GET'):
            log.debug('Request using GET method')
            if len(option_list) > 0:
                
                request_uri = "{0}?".format(request_uri)
                first_item = True

                for option_name in option_list:
                    
                    option = action_map['options'][option_name]
                    
                    if first_item is True:
                        first_item = False
                    else:
                        request_uri = "{0}&".format(request_uri)

                    # if constant value is set, use that
                    if 'constant' in option.keys():
                        if option_name in arg_dict.keys():
                            if arg_dict[option_name] is True:
                                request_uri = "{0}{1}={2}".format(request_uri,option_name,option['constant'])
                    elif option_name in arg_dict.keys():
                        request_uri = "{0}{1}={2}".format(request_uri,option_name,arg_dict[option_name])
                        
            log.info('Request URI: {0}'.format(request_uri))
            post_data = {}
            
            
        # for all other HTTP methods
        # if there is rdata, add it to the data dictionary for the api call
        else:
            log.debug('Request is not type GET')
            post_data = {}
            
            if resource != 'ZoneNoteReport':
                log.debug('Resource is not ZoneNoteReport')
                post_data['rdata'] = {} 
            
                log.debug("Adding rdata to postargs")
                if len(rdata_list) > 0:
                    for rdata_name in rdata_list:
                        
                        #see if rdata_name is in kwargs
                        if rdata_name in arg_dict.keys():
                            post_data['rdata'][rdata_name] = arg_dict[rdata_name]

            # if there are options, set them in the data dictionary as well

            log.debug("Adding options to postargs")
            if len(option_list) > 0:
                for option_name in option_list:
                    if option_name in arg_dict.keys():
                        
                        option = action_map['options'][option_name]

                        # if constant value is set, use that
                        if 'constant' in option.keys():
                            post_data[option_name] = option['constant']
                        elif option_name in arg_dict.keys():
                            post_data[option_name] = arg_dict[option_name]
                            
        if self.logged_in is False:
            self.login()
            
        #remove trailing ? from uri if it exists
        request_uri = re.sub('\?$','',request_uri)
        log.info('Request URL: {0}'.format(request_uri))
        log.debug('Postdata: {0}'.format(pformat(post_data)))
                            
        result = self.execute(request_uri, method, post_data)
        log.debug('Data received: \n{0}'.format(pformat(result)))
        
        if (method != 'GET') and (auto_publish is True) and (resource != 'ZoneNoteReport'):
            log.debug('Autopubish criteria met')
            self._job_status(result['job_id'])
            self._auto_publish(arg_dict['zone'])
            
        return result
