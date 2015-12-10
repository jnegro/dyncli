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

####  Common options ####
OPT_RECORD_TYPES = {
    'flag': 'r',
    'nargs': "*",
    'choices': SUPPORTED_RECORD_TYPES,
    'help': 'Record types',
}
OPT_ZONES = {
    'flag': 'z',
    'nargs': "*",
    'help': 'Zones to search',
}
OPT_ZONE = {
    'flag': 'z',
    'help': 'Zones to search',
}
OPT_FQDN = {
    'flag': 1,
    'help': 'FQDN of record',
}
OPT_TTL = {
    'flag': 't',
    'help': 'TTL for record',
}
OPT_DATAFIELDS = {
    'flag': 'D',
    'nargs': "*",
    'help': 'Datafields you would like to receive in what order',
}
OPT_RECORD_ID = {
    'flag': 'i',
    'help': 'ID for specific record.  Required if more than one record exists for FQDN',
}
OPT_DETAIL = { 'constant': 'Y', 'help': 'Detailed output', }
OPT_UPDATE_ALL = { 'help': 'Update all records that match', }
OPT_NOHEADERS = { 'help': 'Do not show headers at top of CSV', }
OPT_CSV = { 'help': 'Show output as CSV', }
OPT_YES = { 'help': 'Answer yes to all prompts', }
OPT_DELETE_ALL = { 'help': 'Delete all matching records', }
OPT_AS_LIST = { 'help': 'Display data as a Bash-style list, space separated if multiple datafields are requested.', }

#### Not-so-common options ####
OPT_SERVICE_TYPE = {
    'flag': 'S',
    'help': 'Service type to search',
    'choices': [
        'HTTPRedirect',
    ]
}
OPT_PORT = {
    'flag': 'P',
    'help': 'Indicates the port where the service is running'
}
OPT_PRIORITY = {
    'flag': 'N',
    'help': 'Numeric value for priority usage. Lower value takes precedence over higher value where two records of the same type exist on the zone/node.'
}
OPT_WEIGHT = {
    'flag': 'W',
    'help': 'Secondary prioritizing of records to serve. Records of equal priority should be served based on their weight. Higher values are served more often.',
}
OPT_CODE = {
    'flag': 'C',
    'help': 'HTTP response code to return for redirection',
    'choices': [
        '301',
        '302',
    ]
}
OPT_KEEP_URI = {
    'flag': 'K',
    'help': """A flag indicating whether the redirection
             should include the originally requested URI""",
    'choices': [
        'Y',
        'N',
    ]
}
OPT_SERIAL_STYLE = {
    'flag': 'S',
    'help': 'The style in which serial numbers will be generated for the zone',
    'choices': [
        'increment',
        'epoch',
        'day',
        'minute',
    ],
}

DYN_HELPERS = {}
DYN_HELPERS['search'] = {
    'actions': {
        'records': {
            'options': {
                'record_types': OPT_RECORD_TYPES,
                'zones': OPT_ZONES,
                'datafields': OPT_DATAFIELDS,
                'noheaders': OPT_NOHEADERS,
                'as_list': OPT_AS_LIST,
                'ttl_min': {
                    'flag': 'm',
                    'help': 'Minimum TTL to search for',
                },
                'ttl_max': {
                    'flag': 'M',
                    'help': 'Maximum TTL to search for',
                },
                'csv': {
                    'flag': False,
                    'help': "Output as CSV",
                },
            },
        },
        'changelog': {
            'options': {
                'zones': OPT_ZONES,
                'csv': OPT_CSV,
                'limit': {
                    'flag': 'l',
                    'help': 'Limit the record of numbers to be returned',
                },
                'age': {
                    'flag': 'A',
                    'help': 'Minimum age of note in hours',
                },
            },
        },
        'zones': {
            'options': {
                'as_list': OPT_AS_LIST,
            },
        },
        'services': {
            'options': {
                'service_type': OPT_SERVICE_TYPE,
                'zone': OPT_ZONE,
                'detail': OPT_DETAIL,
            },
        }
    },
    'help': 'Search Dyn Data',
}

DYN_HELPERS['add'] = {
    'actions': {
        'ARecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'ttl': OPT_TTL,
                'address': {
                    'flag': 'd',
                    'help': 'Data - IP Address',
                    'required': True,
                },
            },
            'help': 'Add an A Record',
        },
        'CNAMERecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'ttl': OPT_TTL,
                'cname': {
                    'flag': 'd',
                    'help': 'Data - CNAME Address to point to',
                },
            },
            'help': 'Add a CNAME Record',
        },
        'NSRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'ttl': OPT_TTL,
                'nsdname': {
                    'flag': 'd',
                    'help': 'Data - FQDN of Name Server',
                },
            },
            'help': 'Add an NS Record',
        },
        'PTRRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'ttl': OPT_TTL,
                'ptrdname': {
                    'flag': 'd',
                    'help': 'Data - FQDN Address to point to',
                },
            },
            'help': 'Add a PTR Record',
        },
        'TXTRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'ttl': OPT_TTL,
                'txtdata': {
                    'flag': 'd',
                    'help': 'Data - Free form text',
                },
            },
            'help': 'Add a TXT Record',
        },
        'SRVRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'ttl': OPT_TTL,
                'port': OPT_PORT,
                'priority': OPT_PRIORITY,
                'weight': OPT_WEIGHT,
                'target': {
                    'flag': 'd',
                    'help': 'Data - The domain name of a host where the service is running on the specified port',
                },
            },
            'help': 'Add an SRV Record',
        },
        'MXRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'preference': OPT_PRIORITY,
                'ttl': OPT_TTL,
                'exchange': {
                    'flag': 'd',
                    'help': 'Hostname of the server responsible for accepting mail messages in the zone',
                },
            },
            'help': 'Add an MX Record',
        },
        'HTTPRedirect': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'code': OPT_CODE,
                'keep_uri': OPT_KEEP_URI,
                'url': {
                    'flag': 'd',
                    'help': 'Data - The URL of the redirect destination'
                },
            },
            'help': 'Add an HTTPRedirect service',
        },
    },
    'help': 'Add stuff',
}

DYN_HELPERS['update'] = {
    'actions': {
        'ARecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'ttl': OPT_TTL,
                'record_id': OPT_RECORD_ID,
                'update_all': OPT_UPDATE_ALL,
                'yes': OPT_YES,
                'address': {
                    'flag': 'd',
                    'help': 'IP Address',
                },
            },
            'help': 'Update an A Record',
        },
        'CNAMERecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'ttl': OPT_TTL,
                'record_id': OPT_RECORD_ID,
                'update_all': OPT_UPDATE_ALL,
                'yes': OPT_YES,
                'cname': {
                    'flag': 'd',
                    'help': 'Data - CNAME Address to point to',
                },
            },
            'help': 'Update a CNAME Record',
        },
        'NSRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'ttl': OPT_TTL,
                'recordid': OPT_RECORD_ID,
                'update_all': OPT_UPDATE_ALL,
                'yes': OPT_YES,
                'nsdname': {
                    'flag': 'd',
                    'help': 'Data - FQDN of Name Server',
                },
            },
            'help': 'Update an NS Record',
        },
        'PTRRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'ttl': OPT_TTL,
                'record_id': OPT_RECORD_ID,
                'update_all': OPT_UPDATE_ALL,
                'yes': OPT_YES,
                'ptrdname': {
                    'flag': 'd',
                    'help': 'Data - FQDN Address to point to',
                },
            },
            'help': 'Update a PTR Record',
        },
        'TXTRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'ttl': OPT_TTL,
                'id': OPT_RECORD_ID,
                'update_all': OPT_UPDATE_ALL,
                'yes': OPT_YES,
                'txtdata': {
                    'flag': 'd',
                    'help': 'Data - Free form text',
                },
            },
            'help': 'Update a TXT Record',
        },
        'SRVRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'port': OPT_PORT,
                'priority': OPT_PRIORITY,
                'weight': OPT_WEIGHT,
                'id': OPT_RECORD_ID,
                'update_all': OPT_UPDATE_ALL,
                'yes': OPT_YES,
                'target': {
                    'flag': 'd',
                    'help': 'Data - The domain name of a host where the service is running on the specified port'
                },
            },
            'help': 'Update an SRV Record',
        },
        'MXRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'preference': OPT_PRIORITY,
                'ttl': OPT_TTL,
                'id': OPT_RECORD_ID,
                'yes': OPT_YES,
                'exchange': {
                    'flag': 'd',
                    'help': 'Data - Hostname of the server responsible for accepting mail messages in the zone',
                },
            },
            'help': 'Update an MX Record',
        },
        'SOARecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'ttl': OPT_TTL,
                'serial_style': OPT_SERIAL_STYLE,
                'update_all': OPT_UPDATE_ALL,
                'yes': OPT_YES,
                'rname': {
                    'flag': 'd',
                    'help': 'Data - Domain name which specifies the mailbox of the person responsible for this zone',
                },
            },
            'help': 'Update an SOA record',
        },
        'HTTPRedirect': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'code': OPT_CODE,
                'keep_uri': OPT_KEEP_URI,
                'url': {
                    'flag': 'd',
                    'help': 'Data - The URL of the redirect destination'
                },
            },
            'help': 'Update HTTP Redirect service',
        }
    },
    'help': 'Update stuff',
}

DYN_HELPERS['delete'] = {
    'actions': {
        'ARecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'record_id': OPT_RECORD_ID,
                'delete_all': OPT_DELETE_ALL,
                'yes': OPT_YES,
            },
            'help': 'Delete an A Record',
        },
        'CNAMERecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'record_id': OPT_RECORD_ID,
                'delete_all': OPT_DELETE_ALL,
                'yes': OPT_YES,
            },
            'help': 'Delete a CNAME Record',
        },
        'NSRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'record_id': OPT_RECORD_ID,
                'delete_all': OPT_DELETE_ALL,
                'yes': OPT_YES,
            },
            'help': 'Delete an NS Record',
        },
        'PTRRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'record_id': OPT_RECORD_ID,
                'delete_all': OPT_DELETE_ALL,
                'yes': OPT_YES,
            },
            'help': 'Delete a PTR Record',
        },
        'TXTRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'record_id': OPT_RECORD_ID,
                'delete_all': OPT_DELETE_ALL,
                'yes': OPT_YES,
            },
            'help': 'Delete a TXT Record',
        },
        'SRVRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'record_id': OPT_RECORD_ID,
                'delete_all': OPT_DELETE_ALL,
                'yes': OPT_YES,
            },
            'help': 'Delete an SRV Record',
        },
        'MXRecord': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE,
                'record_id': OPT_RECORD_ID,
                'delete_all': OPT_DELETE_ALL,
                'yes': OPT_YES,
            },
            'help': 'Delete an MX Record',
        },
        'HTTPRedirect': {
            'options': {
                'fqdn': OPT_FQDN,
                'zone': OPT_ZONE
            },
            'help': 'Delete HTTPRedirect service',
        },
    },
    'help': 'Delete stuff',
}