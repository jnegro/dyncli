#!/bin/bash

die ()
{
    echo $1
    exit 1
}

die_deactivate ()
{
    echo $1
    deactivate
    exit 1
}

interactive=1
if [ $# > 0 ]
then
    if [ $1 == "-y" ]
    then
        interactive=0
    fi
fi

printf 'Installing dns_tools application\n'

ROOT_DIR=`pwd`

# check if root
if [ $EUID -ne 0 ]
then
    die "This script must be run as root"
fi

# create global shortcut
printf "Checking for dyncli shortcut...."
if [ -L /usr/local/bin/dyncli ]
then
    printf "Link already exists\n"
else
    ln -s $ROOT_DIR/dyncli /usr/local/bin/dyncli || die "\n\nError while setting up shortcut, exiting"
fi

# make virtualenv
printf "Deleting previous virtualenv...:"
rm -Rf env
if [ $? == 0 ]
then
    printf "Done\n"
else
    printf "None Found"
fi

printf "Creating virtualenv...."
virtualenv -p python2.7 env || die "\n\nError while setting up virualenv, exiting"
printf "Done\n"

# install pip dependencies
printf "Installing Python requirements via PIP...."
source $ROOT_DIR/env/bin/activate || die "Error activating virtualenv, exiting"
pip install -r requirements.txt || die "Error while PIPing dependencies, exiting"
printf "Done\n"

# copy settings.sample to settings.py

if [ -f etc/settings.py ]
then
    printf "Existing settings.py found.  Retaining\n"
else
    cp etc/settings.sample etc/settings.py || die_deactivate "\n\nError while creating settings.py, exiting"
fi

printf "\nConfiguration:\n"
if [ $interactive == 0 ]
then
    syslog_enable="Y"
    printf "Non-interactive mode detected\n"
else
    printf "Would you like to enable syslog support? [Y/n]"
    read syslog_enable
fi

if [ $syslog_enable == "n" ]
then
    printf "\nSyslog Support disabled\n"
else
    sed -i 's/^SYSLOG_ENABLED\ =\ 0$/SYSLOG_ENABLED\ =\ 1/g' etc/settings.py || die_deactivate "\n\nError enabling syslog, existing"
    operating_system=`uname` || printf "Operating system not detected, using default\n"; operating_system="default"

    if [ $operating_system == 'Darwin' ]
    then
        sed -i 's/^#SYSLOG_ADDRESS\ =\ ('localhost',514)$/SYSLOG_ADDRESS\ =\ ('localhost',514)/g' etc/settings.py || die_deactivate "\n\nError enabling syslog, exiting"
        printf "\nSyslog address set to localhost:514 for Darwin kernel\n"
        
    else
        sed -i 's/^#SYSLOG_ADDRESS\ =\ \/dev\/log$/SYSLOG_ADDRESS\ =\ \/dev\/log/g' etc/settings.py || die_deactivate "\n\nError enabling syslog, exiting"
        printf "\nSyslog address set to /dev/log\n"
    fi
fi

# set DT_ROOT environment variable globally
printf "Setting DT_ROOT environment variable for virtualenv"
unset DT_ROOT
printf "export DT_ROOT=%s" $ROOT_DIR > /etc/profile.d/dns_tools.sh || die_deactivate "Problem creating /etc/profile.d/dns_tools.sh, exiting"
export DT_ROOT=$ROOT_DIR || die_deactivate "Problem exporting DT_ROOT environment variable, exiting"

printf "\nInstallation Completed, please set DYN_USER and DYN_PASSWORD in your ~/.bash_profile or use the -U and -P flags in dyncl\n\n"