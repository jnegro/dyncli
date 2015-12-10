#This dictionary serves to map out DynectAPI resources as per their documentation https://help.dyn.com/rest-resources/
#  This map is meant to be used by the CLI and the library, so some dictionary items may pertain to the CLI only.
#  The win here is that we don't need to add a new function every time we want to wrap a new API resource.  Instead we just add a new dictionary item here,
#  and things shoudl just work.
#
#  The structure of the dictionary works as follows:
# [RESOURCE]
# --[vars]                  #vars are constants related to the Resource.  Common use cases are GET params like 'detail=y' or Booleans
# ----[<var>]               #the var and it's value.  one line for each var
# --[actions]               #Actions performed with this resource.
# ----[<action>]            #Action choice - one block of these per action
# ------[url_vars]          #URL vars for the resource.  These are mandatory values that are used in the URI part of the REST call
# ------[method]            #The method used for the REST API Call (GET,PUT,POST,DELETE)
# ------[rdata]             #Rdata is the DNS data to use in the call.  Set to False if there is no rdata for the resource to send
# --------[rdata_fields]    #Rdata field and value pairs, one per line
# ------[options]           #Options are optional items.  There are also some not-so-obvious things that go on here for the CLI
# --------[<option>]        #An option block, one per option
# ----------[name]          #For CLI - Name of the option.  NOTE there are some uses cases (Zone) where if the Action name matches this, an option by that name will be created with value set in vars.  Typically Boolean
# ----------[flag]          #For CLI - Short flag (one letter).  If this is set to false, only a long version is presented and
# ----[help]                #For CLI - Help string for the action
SUPPORTED_RECORD_TYPES = [
    'A',
    'CNAME',
    'NS',
    'PTR',
    'SOA',
    'TXT',
    'SPF',
    'SRV',
    'MX',
]


DYN_API_MAP = {}
DYN_API_MAP['AllRecord'] = {
    'actions': {
        'list': {
            'url_vars': ['resource', 'zone'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                }
            },
            'help': 'List all records in a zone',
        },
    },
}
DYN_API_MAP['NSRecord'] = {
    'actions': {
        'list': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
            'help': 'List NS records in a zone',
        },
        'get': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
            'help': 'Get a specific NS record in a zone',
        },
        'add': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'POST',
            'rdata': {
                'nsdname': {
                    'flag': 'd',
                    'help': 'Hostname of the authoritative Nameserver for the zone',
                }
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                }
            },
            'help': 'Add NSRecord to a zone',
        },
        'update': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'PUT',
            'rdata': {
                'nsdname': {
                    'flag': 'd',
                    'help': 'Hostname of the authoritative Nameserver for the zone',
                }
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                },
            },
            'help': 'Update an NS record',
        },
        'delete': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'DELETE',
            'help': 'Delete NSRecord from a zone',
        },
    },
    'help': 'Delete NSRecord from zone',
}
DYN_API_MAP['ARecord'] = {
    'actions': {
        'list': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'GET',
            'help': 'List ARecord that match in a zone',
        },
        'get': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'GET',
            'help': 'Get a specific ARecord from a zone',
        },
        'add': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'POST',
            'rdata': {
                'address': {
                    'flag': 'd',
                    'help': 'IPv4 Address',
                }
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                }
            },
            'help': 'Add ARecord to a zone',
        },
        'update': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'PUT',
            'rdata': {
                'address': {
                    'flag': 'd',
                    'help': 'IPv4 Address',
                }
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                }
            },
            'help': 'Update an A record',
        },
        'delete': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'DELETE',
            'help': 'Delete ARecord from a zone',
        },
    },
}
DYN_API_MAP['HTTPRedirect'] = {
    'actions': {
        'list': {
            'url_vars': ['resource', 'zone'],
            'method': 'GET',
            'help': 'HTTP Redirect Details',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
        },
        'add': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'POST',
            'options': {
                'code': {
                    'flag': 'C',
                    'help': 'HTTP response code to return for redirection',
                },
                'keep_uri': {
                    'flag': 'K',
                    'help': """A flag indicating whether the redirection
                             should include the originally requested URI""",
                },
                'url': {
                    'flag': 'd',
                    'help': 'The destination URL where the client is sent. Must begin with either http:// or https://',
                },
            },
            'help': 'Creating a new HTTP Redirect service',
        },
        'update': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'PUT',
            'options': {
                'code': {
                    'flag': 'C',
                    'help': 'HTTP response code to return for redirection',
                },
                'keep_uri': {
                    'flag': 'K',
                    'help': 'A flag indicating whether the redirection should include the originally requested URI',
                },
                'url': {
                    'flag': 'd',
                    'help': 'The target URL where the client is sent. Must begin with either http:// or https://',
                },
            },
            'help': 'Updates an existing HTTP Redirect service on the zone/node indicated.',
        },
        'delete': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'DELETE',
            'help': 'Deletes an existing HTTP Redirect service from the zone/node indicated.',
        },
    },
}
DYN_API_MAP['CNAMERecord'] = {
    'actions': {
        'list': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
            'help': 'List CNAME record details',
        },
        'get': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'GET',
            'help': 'Get a specific CNAMERecord from a zone',
        },
        'add': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'POST',
            'rdata': {
                'cname': {
                    'flag': 'd',
                    'help': 'Hostname',
                }
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                }
            },
            'help': 'Add a CNAME record to a zone',
        },
        'update': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'PUT',
            'rdata': {
                'cname': {
                    'flag': 'd',
                    'help': 'Hostname',
                }
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                }
            },
            'help': 'Update an CNAME record',
        },
        'delete': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'DELETE',
            'help': 'Delete a CNAME record from a zone',
        },
    },
}
DYN_API_MAP['PTRRecord'] = {
    'actions': {
        'list': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
            'help': 'List PTR records that match fqdn in zone',
        },
        'get': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
            'help': 'Get a specific PTR Record from zone',
        },
        'add': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'POST',
            'rdata': {
                'ptrdname': {
                    'flag': 'd',
                    'help': 'Hostname where the IP address should be directed. Example: mail.example.com',
                }
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                }
            },
            'help': 'Add an PTR record',
        },
        'update': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'PUT',
            'rdata':  {
                'ptrdname': {
                    'flag': 'd',
                    'help': 'Hostname where the IP address should be directed. Example: mail.example.com',
                }
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                }
            },
            'help': 'Update an PTR record',
        },
        'delete': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'DELETE',
            'help': 'Delete a PTR record from a zone',
        },
    },
}
DYN_API_MAP['TXTRecord'] = {
    'actions': {
        'list': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
            'help': 'List TXT records that match fqdn in zone',
        },
        'get': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
            'help': 'Get a specific TXT Record from zone',
        },
        'add': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'POST',
            'rdata': {
                'txtdata': {
                    'flag': 'd',
                    'help': 'Free form text',
                }
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                }
            },
            'help': 'Add a TXT record to a zone',
        },
        'update': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'PUT',
            'rdata': {
                'txtdata': {
                    'flag': 'd',
                    'help': 'Free form text',
                }
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                }
            },
            'help': 'Update an TXT record',
        },
        'delete': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'DELETE',
            'help': 'Delete a TXT record from a zone',
        },
    },
}
DYN_API_MAP['MXRecord'] = {
    'actions': {
        'list': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
            'help': 'List MX records that match fqdn in zone',
        },
        'get': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
            'help': 'Get a specific MX Record from zone',
        },
        'add': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'POST',
            'rdata': {
                'exchange': {
                    'flag': 'd',
                    'help': 'Hostname of the server responsible for accepting mail messages in the zone',
                },
                'preference': {
                    'flag': 'N',
                    'help': 'Numeric value for priority usage. Lower value takes precedence over higher value where two records of the same type exist on the zone/node. Default = 10',
                },
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                }
            },
            'help': 'Add an MX record to a zone',
        },
        'update': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'PUT',
            'rdata': {
                'exchange': {
                    'flag': 'd',
                    'help': 'Hostname of the server responsible for accepting mail messages in the zone',
                },
                'preference': {
                    'flag': 'N',
                    'help': 'Numeric value for priority usage. Lower value takes precedence over higher value where two records of the same type exist on the zone/node. Default = 10',
                },
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                }
            },
            'help': 'Update an TXT record',
        },
        'delete': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'DELETE',
            'help': 'Delete an MX record from a zone',
        },
    },
}
DYN_API_MAP['SPFRecord'] = {
    'actions': {
        'list': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
            'help': 'List SPF records that match fqdn in zone',
        },
        'get': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
            'help': 'Get a specific SPF Record from zone',
        },
        'add': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'POST',
            'rdata': {
                'txtdata': {
                    'flag': 'd',
                    'help': 'Free text box containing SPF record information',
                }
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                }
            },
            'help': 'Add a SPF record to a zone',
        },
        'update': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'PUT',
            'rdata': {
                'txtdata': {
                    'flag': 'd',
                    'help': 'Free text box containing SPF record information',
                }
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                }
            },
            'help': 'Update an SPF record',
        },
        'delete': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'DELETE',
            'help': 'Delete a SPF record from a zone',
        },
    },
}
DYN_API_MAP['SRVRecord'] = {
    'actions': {
        'list': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
            'help': 'List SRV records that match fqdn in zone',
        },
        'get': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
            'help': 'Get a specific SRV Record from zone',
        },
        'add': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'POST',
            'rdata': {
                'port': {
                    'flag': 'P',
                    'help': 'Indicates the port where the service is running'
                },
                'priority': {
                    'flag': 'N',
                    'help': 'Numeric value for priority usage. Lower value takes precedence over higher value where two records of the same type exist on the zone/node.'
                },
                'target': {
                    'flag': 'd',
                    'help': 'he domain name of a host where the service is running on the specified port'
                },
                'weight': {
                    'flag': 'W',
                    'help': 'Secondary prioritizing of records to serve. Records of equal priority should be served based on their weight. Higher values are served more often.',
                },
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                }
            },
            'help': 'Add a SRV record to a zone',
        },
        'update': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'PUT',
            'rdata': {
                'port': {
                    'flag': 'P',
                    'help': 'Indicates the port where the service is running',
                },
                'priority': {
                    'flag': 'N',
                    'help': 'Numeric value for priority usage. Lower value takes precedence over higher value where two records of the same type exist on the zone/node.',
                },
                'target': {
                    'flag': 'd',
                    'help': 'The domain name of a host where the service is running on the specified port'
                },
                'weight': {
                    'flag': 'W',
                    'help': 'Secondary prioritizing of records to serve. Records of equal priority should be served based on their weight. Higher values are served more often.',
                },
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                },
            },
            'help': 'Update an SRV record',
        },
        'delete': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'DELETE',
            'help': 'Delete a SRV record from a zone',
        },
    },
}
DYN_API_MAP['SOARecord'] = {
    'actions': {
        'list': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'List of matching SOARecords',
                },
            },
            'help': 'List PTR record details',
        },
        'get': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'GET',
            'options': {
                'detail': {
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },
            },
            'help': 'List PTR record details',
        },
        'update': {
            'url_vars': ['resource', 'zone', 'fqdn', 'record_id'],
            'method': 'PUT',
            'rdata': {
                'rname': {
                    'flag': 'd',
                    'help': 'Domain name which specifies the mailbox of the person responsible for this zone',
                }
            },
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                },
                'serial_style': {
                    'flag': 'S',
                    'help': 'The style in which serial numbers will be generated for the zone',
                    'choices': [
                        'increment',
                        'epoch',
                        'day',
                        'minute',
                    ],
                }
            },
            'help': 'Update an SOA record',
        },
    },
}
DYN_API_MAP['Zone'] = {
    'actions': {
        'list': {
            'url_vars': ['resource'],
            'method': 'GET',
            'help': 'List of all zones',
        },
        'get': {
            'url_vars': ['resource', 'zone'],
            'method': 'GET',
            'help': 'List of all zones',
            'options': {
                'detail': {
                    'flag': False,
                    'constant': 'y',
                    'help': 'Provides extra detail about each record',
                },   
            },
        },
        'add': {
            'url_vars': ['resource', 'zone'],
            'method': 'POST',
            'options': {
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                },
                'rname': {
                    'flag': 'd',
                    'help': 'Administrative contact for this zone',
                },
            },
            'help': 'Add a new zone',
        },
        'publish': {
            'url_vars': ['resource', 'zone'],
            'method': 'PUT',
            'options': {
                'publish': {
                    'constant': True,
                    'help': 'Publish changes to a zone',
                }
            },
            'help': 'Publish changes to a zone',
        },
        'thaw': {
            'url_vars': ['resource', 'zone'],
            'method': 'PUT',
            'options': {
                'thaw': {
                    'constant': True,
                    'help': 'Unfreeze a zone',
                }
            },
            'help': 'Unfreeze a zone to allow changes',
        },
        'freeze': {
            'url_vars': ['resource', 'zone'],
            'method': 'PUT',
            'options': {
                'freeze': {
                    'constant': True,
                    'help': 'Freeze a zone to prevent chnages',
                }
            },
            'help': 'Freeze a zone to stop changes',
        },
        'delete': {
            'url_vars': ['resource', 'zone'],
            'method': 'DELETE',
            'help': 'Delete a zone',
        },
    },
}
DYN_API_MAP['ZoneTransfer'] = {
    'actions': {
        'status': {
            'url_vars': ['resource', 'zone'],
            'method': 'GET',
            'help': 'Check the status of a zone transfer job',
        },
        'start': {
            'url_vars': ['resource', 'zone'],
            'method': 'POST',
            'options': {
                'master_ip': {
                    'flag': 'd',
                    'help': 'IP address of the master server where the zone data exists',
                }
            },
            'help': 'Start a zone transfer for a zone',
        },
        'retry': {
            'url_vars': ['resource', 'zone'],
            'method': 'PUT',
            'options': {
                'master_ip': {
                    'flag': 'd',
                    'help': 'IP address of the master server where the zone data exists',
                }
            },
            'help': 'Retry a failed zone transfer',
        },
    },
}
DYN_API_MAP['IPTrack'] = {
    'actions': {
        'list': {
            'url_vars': ['resource', 'fqdn'],
            'method': 'GET',
            'help': 'Retrieves all instances of the IPTrack service on the zone/node indicated',
        },
        'add': {
            'url_vars': ['resource', 'zone', 'fqdn'],
            'method': 'POST',
            'options': {
                'record_types': {
                    'flag': 'r',
                    'help': 'Type of records to track (array)',
                },
                'hosts': {
                    'flag': 'd',
                    'nargs': '*',
                    'help': 'Hostnames of the zones where you want to track records (array)',
                },
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                },
                'netmask': {
                    'flag': 'n',
                    'help': 'A netmask to match A/AAAA rdata against. Matched records will get PTR records, others will not',
                },
            },
            'help': 'Creates a new instance of the IPTrack service on the zone/node indicated.',
        },
        'update': {
            'url_vars': ['resource', 'zone', 'fqdn', 'service_id'],
            'method': 'PUT',
            'options': {
                'record_types': {
                    'flag': 'r',
                    'help': 'Type of records to track (array)',
                },
                'hosts': {
                    'flag': 'd',
                    'nargs': '*',
                    'help': 'Hostnames of the zones where you want to track records (array)',
                },
                'ttl': {
                    'flag': 't',
                    'help': 'Time To Live for Record',
                },
                'netmask': {
                    'flag': 'n',
                    'help': 'A netmask to match A/AAAA rdata against. Matched records will get PTR records, any others will not',
                },
                'activate': {
                    'help': 'Activate policy',
                },
                'deactivate': {
                    'help': 'Deactivate policy',
                },
            },
            'help': 'Updates an existing instance of the IPTrack service on the zone/node indicated.',
        },
        'delete': {
            'url_vars': ['resource', 'zone', 'fqdn', 'service_id'],
            'method': 'DELETE',
            'help': 'Deletes an existing instance of the IPTrack service on the zone/node indicated',
        },
    },
}
DYN_API_MAP['ZoneNoteReport'] = {
    'actions': {
        'get': {
            'url_vars': ['resource'],
            'method': 'POST',
            'options': {
                'zone': {
                    'flag': 'z',
                    'help': 'Zone to get notes from',
                },
                'limit': {
                    'flag': 'l',
                    'help': 'The number of notes to be retrieved.  Limit 1000 notes'
                },
                'offset': {
                    'flag': 'o',
                    'help': 'Count of the most recent notes to skip. Defaults to 0'
                },
            },
            'help': 'Get a report of zone notes',
        },
    },
}
