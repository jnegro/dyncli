<<<<<<< HEAD
#DynCLI

DynCLI is a command line client written in Python for making changes to your Managed DNS account via DynectAPI.
The included DynResource module is used by DynCLI as an abstraction layer from the rather stark DynAPI client.

As part of installation, a virtualenv must be built on Python 2.7.  Run the install.sh script to build the virtualenv,
PIP in requirements, and add environment variables and shortcuts for ease of use.

##Developers Notes

The structure of the application is based around the DynRestResource and DynHelper modules.  

1. DynRestResource - This class is used to make a single API call to the DynectAPI.
2. DynHelper - This class is a base class for other helper modules included.
        
The use of dynresourcemap.py is two fold in order to keep things consistent and extensible.  DynRestResource class uses 
it to load the mapped-out options for the specified DynectAPI resource, which means that DynHelper uses this in aggregate.
The other place where dynresourcempa.py is important is in argument parsing in dyncli.py.  The argparse module builds out
contextual options based on the resource spec in the file.   In other words, by adding a Dynect API Resource in dynresourcemap.py,
you are using the same config for both creating the argument parsing and the actual parameters for the DynResource to use.
No change in code (should be) required to add a Dynect API resource to the library and the dyncli.py script.

##dyncli usage

dyncli utilizes argparse to provide contextual help at the command line.  By using the -h flag you can see further options
from your current arguments:

    $ dyncli -h
    usage: dyncli.py [-h] [-U USER] [-A ACCOUNT]
                     [-L {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
                     {search,delete,add,update,resource}...

    positional arguments:
      {search,delete,add,update,resource}
        search              Search Dyn Data
        delete              Delete stuff
        add                 Add stuff
        update              Update stuff
        resource            Make direct API Calls
    
    optional arguments:
      -h, --help            show this help message and exit
      -U USER, --user USER  The username to connect to the dyn api. Can also be
                            set as DYN_USER in environment or in settings.py.
      -A ACCOUNT, --account ACCOUNT
                            The account name used to make API requests. Can be set
                            as DYN_ACCOUNT in environment or in settings.py.
      -L {CRITICAL,ERROR,WARNING,INFO,DEBUG}, --loglevel {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                            Logging output level

In the above help, we can see that our command first positional(required) argument is one of the ones in brackets

    positional arguments:
      {search,delete,add,update,resource}
        search              Search Dyn Data
        delete              Delete stuff
        add                 Add stuff
        update              Update stuff
        resource            Make direct API Calls

All of the above options are self-explanitory actions, except for 'resource' which maps to a single DynectAPI Resource as 
found in the documentation (https://help.dyn.com/rest-resources/)
The ones in that list are the ones we have already mapped out in dynresourcemap.py.  Adding more resources later only requires an
addition to that file, not to dyncli.py.  They populate dynamically.

There are also some optional arguments in the first section above in capital letter flags.  If you have configured your etc/settings.py
properly, you should not need to use these flags.

###Simple Resource-specific Commands

Next, lets say we are going to use the ARecord resource.  The contextual help at the next level looks like this:

    $ dyncli resource ARecord -h
    usage: dyncli.py resource ARecord [-h] {add,delete,list,update,get} ...
    
    positional arguments:
      {add,delete,list,update,get}
        add                 Add ARecord to a zone
        delete              Delete ARecord from a zone
        list                List ARecord that match in a zone
        update              Update an A record
        get                 Get a specific ARecord from a zone
    
    optional arguments:
      -h, --help            show this help message and exit


Our next required argument is the action we would like to perform with the resource.  In this case, let us say we want to add an ARecord:

    $ dyncli resource ARecord add -h
    usage: dyncli.py resource ARecord add [-h] [-a ADDRESS] [-t [TTL]] zone fqdn
    
    positional arguments:
      zone
      fqdn
    
    optional arguments:
      -h, --help            show this help message and exit
      -a ADDRESS, --address ADDRESS
                            IPv4 Address
      -t [TTL], --ttl [TTL]
                            IPv4 Address

At this point we appear to be at the nitty gritty of adding an ARecord.  We will have to provide the required arguments of the zone
that the new ARecord will be added to, and the fqdn of the new record.  We then use the -a and -t options to set the IP Address
and the TTL.  Address is required (by the api, not yet required in argparse), but TTL is optional.

###Aggregate Commands / Helpers
Aggregate Commands based on the action that the user wishes to perform.  Most day to day tasks would require many resource/single
command calls to accomplish, so CLI users and bash scripters will use these commands.
Unlike single resource-based calls, these commands require an actual function in lib/DynAPIHelpers.py DynHelper class in order to carry out
specific tasks.  

The current helpers are based on CRUD standards - search, add, update, and delete.  They behave much like the resource commands:

    $ dyncli search -h
    usage: dyncli.py search [-h] {zones,records,services,changelog} ...

    positional arguments:
      {zones,records,services,changelog}
        zones               Search Dyn Data
        records             Search Dyn Data
        services            Search Dyn Data
        changelog           Search Dyn Data
    
    optional arguments:
      -h, --help            show this help message and exit

and the submenu for the records option:

    $ dyncli search records -h
    usage: dyncli.py search records [-h] [-z [ZONES [ZONES ...]]]
                                    [-r [RECORD_TYPES [RECORD_TYPES ...]]]
                                    [--as_list] [-m TTL_MIN] [-M TTL_MAX] [--csv]
                                    [--noheaders]
                                    [-D [DATAFIELDS [DATAFIELDS ...]]]
                                    
    optional arguments:
      -h, --help            show this help message and exit
      -z [ZONES [ZONES ...]], --zones [ZONES [ZONES ...]]
                            Zones to search
      -r [RECORD_TYPES [RECORD_TYPES ...]], --record_types [RECORD_TYPES [RECORD_TYPES ...]]
                            Record types
      --as_list             Display data as a Bash-style list, space separated if
                            multiple datafields are requested.
      -m TTL_MIN, --ttl_min TTL_MIN
                            Minimum TTL to search for
      -M TTL_MAX, --ttl_max TTL_MAX
                            Maximum TTL to search for
      --csv                 Output as CSV
      --noheaders           Do not show headers at top of CSV
      -D [DATAFIELDS [DATAFIELDS ...]], --datafields [DATAFIELDS [DATAFIELDS

You many notice that there is a combination of short and long flag types, as well as position arguments.  The logic currently
behind this is very uniform with Resource commands, and rather uniform with Helpers as follows:

1. Positional arguments are used for the major parts of the command, including the FQDN of a record in question.
2. Short flags represent GET or POST style parameters for the requests.  Some are required, some are not.
3. Long flags present True/False type options that have no trailing data.  Their data is always a constant.

NOTE:  Right now we do not have strict enough requirements/exclusive(and/or) argument checking, so the API will just kick back
an error if you have used the resource incorrectly.  This will be upgraded in later versions.

##TO DO
1. Add better argument checking, including required and/or mutually exclusive options.
2. Add more DynectAPI resource mappings
3. Add a unit test facility, hopefully leveraging the DynAPIMap to make tests with parameters only.
=======
# Dyn DNS cli tool
### Usage
```
usage: dyncli [-h] [-e ENDPOINT] [-c CREATE] [--cname] [-v VALUE] [-t TTL]
              [-d DELETE] [-u UPDATE_RECORD] [-U USER] [-P PASSWORD]
              [-A ACCOUNT] [-Z ZONE] [-l] [--verbose]

optional arguments:
  -h, --help            show this help message and exit
  -e ENDPOINT, --endpoint ENDPOINT
                        The endpoint to make API requests.
  -c CREATE, --create CREATE
                        Create a new record. Defaults to A record unless
                        --cname is set.
  --cname               Create a cname record instead of an A record.
  -v VALUE, --value VALUE
                        The value to set the DNS record to. Eg 10.0.0.101.
  -t TTL, --ttl TTL     TTL of record in seconds.
  -d DELETE, --delete DELETE
                        Delete an existing record
  -u UPDATE_RECORD, --update UPDATE_RECORD
                        Perform a DNS update on an existing record.
  -U USER, --user USER  The username to connect to the dyn api. Can also be
                        set as DYN_USER in environment.
  -P PASSWORD, --password PASSWORD
                        The password to use with the dyn api. Can also be set
                        as DYN_PW in environment.
  -A ACCOUNT, --account ACCOUNT
                        The account name used to make API requests. Can be set
                        as DYN_ACCOUNT in environment.
  -Z ZONE, --zone ZONE  The zone to take action on. Eg example.com. Can be set
                        as DYN_ZONE in environment.
  -l, --list            List all dns records as a csv file.
  --verbose             Print out api responses.
```

Dyn is a nice DNS service. It's an alternative to Amazon's Route 53. Though I do not believe that dyn's API is as robust as amazone, with the right set of tools is just dandy.

This tool allows for the manipulation of DNS records via the restful API.

It currently supports the following:
* Create A and CNAME records
* Update A and CNAME records
* Delete A and CNAME records
* List all of the records as a CSV

### Requirements
The requests & argparse packages are required but not currently part of the standard library. Get them with pip: 
```
pip install -r requirements.txt
```

You can pass your username and password directly into the script, but it's better if you setup a few environment variables. dyncli will take advantage of the following environment variables if they are present:
```
DYN_USER
DYN_PW
DYN_ZONE
DYN_ACCOUNT
```

You can activate these by appending them to your ```~/.bash_profile```:
```
export DYN_USER='foo'
export DYN_PW='bar'
export DYN_ZONE='example.com'
export DYN_ACCOUNT='example'
```

### Creating a record
Right now both A and CNAME record creation is supported. Create a record uses the ```-c``` flag along with the optional ```--cname``` flag if that's your desired record type.

The default record type is an address (A) record.
```
# Create an A record with default TTL
$ ./dyncli -c myfqdn.example.net -v 10.0.0.100

# Create an A record with custom TTL
$ ./dyncli -c myfqdn.example.net -v 10.0.0.100 --ttl 3600

# Create a CNAME record
$ ./dyncli -c myfqdn.example.net -v otherfqdn.example.net --cname
```

### Updating a record
Once records are created, they can be easily updated with the ```-u``` or ```--update``` flag.

```
# Update the TTL of an existing record
$ ./dyncli -u myfqdn.example.net --ttl 3600

# Update the value of an existing cname record
$ ./dyncli -u myfqdn.example.net -v someotherfqdn.example.net
```

## Deleting a record
Records are deleted by passing the ```-d``` or ```--delete``` flag.
```
# Delete an address (A) record
$ ./dyncli -d myfqdn.example.net

# Delete a cname record (requires the --cname flag)
$ ./dyncli -d myfqdn.example.net --cname
```

### List all records (csv format)
Sometimes it's useful to list all of the records. We use this to do a simple nightly backup of our DNS zone.

The output format is a simple CSV file. Beware that if you have commas in your TXT record, they'll be translated to a pipe (```|```).
```
$ ./dyncli --list
zone,ttl,fqdn,record_type,data
example.net,300,test.example.net,CNAME,test2.example.net
example.net,300,foo.example.net,A,172,16.0.100
example.net,3600,example.net,TXT,public_key=sdjflksdj
..
```

Sometimes it's also useful to check if a zone exists before you go creating one willy nilly
```
$ ./dyncli --list | grep database
example.net,300,database.example.net,A,172.16.0.100
example.net,300,database.internal.example.net,A,172.16.0.100
example.net,300,database.something.example.net,A,172.16.0.100

(See what happens when you go on creating records without checking first?)
```

If you notice any bugs please open an issue.
>>>>>>> 943c862f0bb8d09b89b5280f58001ff310f927a7
