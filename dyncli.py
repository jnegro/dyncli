#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from pprint import pprint, pformat
import getpass
import logging
from logging import handlers

from settings import *
from DynResource import DYN_API_MAP, DynRestResource, dynhelpers, Formatter


def set_credentials():

    # decide whether to use credentials from in this order:
    #   1. the command line arguments
    #   2. the settings.py file
    #   3. DYN_USER,DYN_PASSWORD,DYN_ACCOUNT from Environment

    if args.user is not None:
        log.debug('No User specified at command prompt, trying settings.py'
                  )
        user = args.user
        log.debug('User specified at prompt, prompting for password')
        password = getpass.getpass(prompt='DynAPI Password:')
    else:
        try:
            user = USER
            log.debug('User {0} found in settings.py'.format(user))
        except:
            try:
                log.debug('settings.py did not contain username, trying environment'
                          )
                user = os.environ['DYN_USER']
                log.debug('User {0} found in environment'.format(user))
            except:
                log.error('User name not specified at prompt, settings.py, or environment'
                          )
                raise
        try:
            password = PASSWORD
            log.debug('Password found in settings.py')
        except:
            try:
                log.debug('settings.py did not contain a password, trying environment'
                          )
                password = os.environ['DYN_PASSWORD']
                log.debug('Password found in environment')
            except:
                log.error('Password not found in settings.py or environment'
                          )
                raise

    if args.account is not None:
        account = args.account
        log.debug('Account name {0} specified in command'.format(account))
    else:
        try:
            account = ACCOUNT
            log.debug('Account name {0} found in settings.py'.format(account))
        except:
            try:
                log.debug('Account name not found in settings.py.  Checking environment'
                          )
                account = os.environ['DYN_ACCOUNT']
                log.debug('Account name {0} found in environment'.format(account))
            except:
                log.error('Account name not specified in command, settings.py, or environment'
                          )
                raise
    log.info('executed as user {0}'.format(user))

    return [user, password, account]


def convert_args_to_dict():

    # argparse keeps the arguments as attributes of an object.
    # The library accepts a dictionary of keyword args
    #   in order to preserve its independence

    log.debug('Converting args to dictionary')
    arg_dict = {}

    attr_list = args.__dict__.keys()
    for attribute in attr_list:

        # important to filter out Boolean flags that were not set

        if getattr(args, attribute) is not None:
            if attribute != 'password':
                log.debug('Attribute {0} found, value {1}'.format(attribute,
                          getattr(args, attribute)))
            if attribute == 'helper_action':
                arg_dict['resource'] = getattr(args, attribute)
            arg_dict[attribute] = getattr(args,attribute)
        else:
            log.debug('Attribute {0} was not set'.format(attribute))

    return arg_dict


def _get_option_item_parser(option_name,option_item):

    option_item_parser = []
    option_item_kwargs = {}
    
    #order of the argparse argument args matters
    #short flag
    if 'flag' not in option_item.keys():
        option_item['flag'] = False
        
    if option_item['flag'] is False:
        # if the option flag is set to False, set the default to false and
        #  store true if it appears
        #  These are for Boolean flags that don't require input
        option_item_kwargs['action'] = 'store_true'
        option_item_kwargs['default'] = 'store_false'
        option_item_parser.append("--{0}".format(option_name))
    elif isinstance(option_item['flag'], str):
        option_item_parser.append("-{0}".format(option_item['flag']))
        option_item_parser.append("--{0}".format(option_name))
        
    #if the flag was not False and not a string, it is positional and dest will take care of it.
    
    #build kwargs
    if 'nargs' in option_item.keys():
        option_item_kwargs['nargs'] = option_item['nargs']
    if 'help' in option_item.keys():
        option_item_kwargs['help'] = option_item['help']
    option_item_kwargs['dest'] = option_name
    
    output = {
        'args': option_item_parser,
        'kwargs': option_item_kwargs,
    }
    
    return output
    

def main():

    log.info('Begin dyncli script execution')

    # set credentials

    try:
        [args.user, args.password, args.account] = set_credentials()
        log.debug('Credentials set successfully')
    except Exception, e:
        log.exception('Script failed to set credentials, exiting')
        log.debug(e)
        sys.exit(1)

    # convert args to dictionary

    try:
        arg_dict = convert_args_to_dict()
        log.debug('Successfully converted args to dictionary for consumption'
                  )
    except Exception, e:
        log.exception("""Script failed to convert arguments provided
            into a dictionary for consumption, exiting"""
                      )
        log.debug(e)
        sys.exit(1)

    # create the api object and provide the argument dictionary

    try:
        if args.helper == 'resource':
            resource_obj = DynRestResource(args.user, args.password, args.account, logger='dyncli')
            log.debug('Successfully created Dynect resource object')
            result = resource_obj.do(args.resource,args.action,arg_dict)
            log.debug('Successfully retrieved result set')
            pprint(result)
        else:
            
            #for helpers, action and resource args are reversed.  May fix later
            if args.helper == 'add':
                helper_obj = dynhelpers.Add(args.user, args.password, args.account, logger='dyncli')
            elif args.helper == 'update':
                helper_obj = dynhelpers.Update(args.user, args.password, args.account, logger='dyncli')
            elif args.helper == 'delete':
                helper_obj = dynhelpers.Delete(args.user, args.password, args.account, logger='dyncli')
            elif args.helper == 'search':
                helper_obj = dynhelpers.Search(args.user, args.password, args.account, logger='dyncli')
                
            log.debug('Successfully created Dyn Helper object')
            result = helper_obj.do(args.helper_action, arg_dict)
            log.debug('Successfully retrieved result set')
            
            output = Formatter(logger='dyncli')
            
            try:
                if arg_dict['csv'] is True:
                    for line in output.csv(result, arg_dict):
                        print line
                else:
                    raise KeyError
            except KeyError:
                try:
                    if arg_dict['as_list'] is True:
                        if arg_dict['helper_action'] == 'zones':
                            for line in output.zones_as_list(result,arg_dict):
                                print line
                        else:
                            for line in output.as_list(result, arg_dict):
                                print line
                    else:
                        raise KeyError
                except KeyError:
                    for line in output.standard(result):
                        print line
            
    except Exception:

        log.exception('Error while retrieving data from API, exiting')
        sys.exit(1)

    log.info('Dyncli script run completed successfully')


if __name__ == '__main__':
    parser = {}
    subparser = {}

    # main parser - these args are global and static.  Uppercase short flags,
    #  and represent global parameters

    parser['main'] = argparse.ArgumentParser()
    parser['main'].add_argument('-U', '--user', dest='user',
                                help="""The username to connect to the dyn api.
                Can also be set as DYN_USER in
                environment or in settings.py.""")
    parser['main'].add_argument('-A', '--account', dest='account',
                                help="""The account name used to make API requests. Can be set as
                DYN_ACCOUNT in environment or in settings.py."""
                                )
    parser['main'].add_argument('-L', '--loglevel', choices=['CRITICAL'
                                , 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
                                default='INFO',
                                help='Logging output level')
                                
    # Declare the HELPER subparser

    subparser['main'] = parser['main'].add_subparsers(dest='helper')
    helpers = dynhelpers.dynhelpermap.DYN_HELPERS

    for helper_key in helpers.keys():
        
        helper = helpers[helper_key]
        parser[helper_key] = subparser['main'].add_parser(helper_key, help=helper['help'])

        subparser[helper_key] = parser[helper_key].add_subparsers(dest='helper_action')

        for action_key in helper['actions'].keys():
            action = helpers[helper_key]['actions'][action_key]
            helper_action = '{0}_{1}'.format(helper_key, action_key)
            parser[action_key] = subparser[helper_key].add_parser(action_key, help=helper['help'])
                    
            # if options exist, decide what type of option they are, and build them out.
            if 'options' in action.keys():
                for option_name in action['options'].keys():
                    option_item = action['options'][option_name]
                    option_dict = _get_option_item_parser(option_name,option_item)
                    parser[action_key].add_argument(*option_dict['args'],**option_dict['kwargs'])

    # declare the RESOURCE subparser

    parser['resource'] = subparser['main'].add_parser('resource',
            help='Make direct API Calls')
    subparser['resource'] = parser['resource'
                                   ].add_subparsers(dest='resource',
            help='Dynect API Resource Name')

    # loop thru resources in the DynAPIMap dictionary and create a subparser for each

    for resource in DYN_API_MAP.keys():
        parser[resource] = subparser['resource'].add_parser(resource)
        subparser[resource] = parser[resource].add_subparsers(dest='action')

        action_map = DYN_API_MAP[resource]['actions']

        # for each resource, loop thru the actions and build a subparser for each
        for action in action_map.keys():
            resource_action = '{0}_{1}'.format(resource, action)
            url_vars = action_map[action]['url_vars']
            method = action_map[action]['method']
            parser[resource_action] = subparser[resource].add_parser(action, help=action_map[action]['help'])

            # URL_VARS are positional with no flags - they are not optional

            for url_var in url_vars:
                if url_var in ['resource']:
                    continue
                parser[resource_action].add_argument(url_var)

            # if rdata fields exist, build them out with long and short flags
            if 'rdata' in action_map[action].keys():
                for rdata_name in action_map[action]['rdata'].keys():
                    rdata_item = action_map[action]['rdata'][rdata_name]
                    rdata_option_dict = _get_option_item_parser(rdata_name,rdata_item)
                    parser[resource_action].add_argument(*rdata_option_dict['args'],**rdata_option_dict['kwargs'])

            # if options exist, decide what type of option they are, and build them out.
            if 'options' in action_map[action].keys():
                for option_name in action_map[action]['options'].keys():
                    option_item = action_map[action]['options'][option_name]
                    option_dict = _get_option_item_parser(option_name,option_item)
                    parser[resource_action].add_argument(*option_dict['args'],**option_dict['kwargs'])


    args = parser['main'].parse_args()

    # set up logging

    log_format = \
        '%(name)s:%(lineno)d[%(process)d]: %(levelname)s - %(message)s'
    log_level_numeric = getattr(logging, args.loglevel.upper())

    try:
        logging.captureWarnings(True)
    except:
        pass

    logger_name = 'dyncli'
    args.logger_name = logger_name
    log = logging.getLogger(logger_name)
    logformat = logging.Formatter(log_format)
    log.setLevel(log_level_numeric)

    # syslog handler

    if SYSLOG_ENABLED == 1:
        syslog_handler = \
            logging.handlers.SysLogHandler(address=SYSLOG_ADDRESS)
        syslog_handler.setFormatter(logformat)
        log.addHandler(syslog_handler)
    else:
        null_handler = logging.NullHandler()
        log.addHandler(null_handler)

    # console handler

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(logformat)
    if args.loglevel.upper() != 'DEBUG':
        console_handler.setLevel(log_level_numeric + 10)
    log.addHandler(console_handler)

    main()
