#!/usr/bin/python
""" helper.py

Utility python script to setup and update local and remote servers.

Examples:

# Setup a local server
python helper.py config site on local

# Setup a prod server
python helper.py config site on prod

# Updates prod code (from git)
python helper.py update prod

:Author: Humberto Moreira <humberto.mn@gmail.com>
"""

##############################
# Imports
##############################
import sys, os, subprocess, re, time



##############################
# Configurations
##############################
# Servers' info
SERVERS = {
    # Local server
    "local" : {
        "IP" : "localhost",             # The IP address of the server.
        "DOMAIN" : "localhost",         # Server's domain name.
        "KEYPAIR" : "",                 # The keypair file used to connect to the server.
        "DEFAULT_USER" : "vagrant",     # The default user and user group of the server.
        "HTTP_PORT" : 80,               # The HTTP port on the server.
        "HTTPS_PORT" : 443,             # The HTTPS port on the server.
        "HTTP_FORWARDED_PORT" : 8080,   # The HTTP forwarded port
        "HTTPS_FORWARDED_PORT" : 4443,  # The HTTPS forwarded port
        "BRANCH" : "master",            # Vagrant server doesn't require git
    },

    "dev" : {
        "IP" : "54.94.211.154",                 # The IP address of the server.
        "DOMAIN" : "topmusic.humbertomn.com",   # Server's domain name.
        "KEYPAIR" : "topmusicaws.pem",          # The keypair file used to connect to the server.
        "DEFAULT_USER" : "ubuntu",              # The default user and user group of the server.
        "HTTP_PORT" : 80,                       # The HTTP port on the server.
        "HTTPS_PORT" : 443,                     # The HTTPS port on the server.
        "HTTP_FORWARDED_PORT" : 80,             # The HTTP forwarded port
        "HTTPS_FORWARDED_PORT" : 443,           # The HTTPS forwarded port
        "BRANCH" : "master",                    # Vagrant server doesn't require git
    },

    "prod" : {
        "IP" : "ip-here",               # The IP address of the server.
        "DOMAIN" : "domain-here",       # Server's domain name.
        "KEYPAIR" : "key-here.pem",     # The keypair file used to connect to the server.
        "DEFAULT_USER" : "ubuntu",      # The default user and user group of the server.
        "HTTP_PORT" : 80,               # The HTTP port on the server.
        "HTTPS_PORT" : 443,             # The HTTPS port on the server.
        "HTTP_FORWARDED_PORT" : 80,     # The HTTP forwarded port
        "HTTPS_FORWARDED_PORT" : 443,   # The HTTPS forwarded port
        "BRANCH" : "master",            # Vagrant server doesn't require git
    },

}

# Global settings
GIT_REPO = "https://github.com/humbertomn/topmusic.git"     # Git repository
DEPLOYMENT_ROOT = ""                                        # Root folder for deploying web projects (Leave empty for a single project)
VIRTUALENV_ROOT = ""                                        # Root folder for virtualenvs  (Leave empty for a single project)
PROJECT_ALIAS = "topmusic"                                  # Current project alias
APP_NAME = "topmusic"                                       # Current project main application

# Packages to be installed for PHP Development
PHP_PACKAGES = [
    "apache2", "libapache2-mod-php5", "php5-mysql",
    "libmysqlclient-dev", "mysql-client"
]



#############################################
# PRE-CALCULATED CONFIGURATIONS (NOT RECOMMENDED TO MODIFY)
#############################################

# Pre-calculate the available servers regex pattern
AVAILABLE_SERVERS_PATTERN = '(' + '|'.join( sorted( SERVERS.keys() ) ) + ')'

# Project root
PROJECT_ROOT = DEPLOYMENT_ROOT + '/' + PROJECT_ALIAS

# Aliases for PHP
PHP_ALIAS = "php"

# Apache's default user
APACHE_DEFAULT_USER = "www-data"

# User group for the project
DEFAULT_USER_GROUP = PROJECT_ALIAS + "-dev"

# Root path for php
PHP_ROOT = PROJECT_ROOT + '/' + PHP_ALIAS

# Apache configurations folder
APACHE_SITES_ENABLED_PATH = "/etc/apache2/sites-enabled"    # Sites enabled folder on Apache
APACHE_MODS_ENABLED_PATH = "/etc/apache2/mods-enabled"      # Mods enabled folder on Apache
APACHE_MODS_AVAILABLE_PATH = "/etc/apache2/mods-available"  # Mods available folder on Apache

# Spacing for help messages.
N_DEFAULT_HELP_SPACING = 15

# Apacha Config Files
# Requires formatting on the fly. Params:
# http_port, php_alias, domain, php_root.
WIKI_CONF = """
    <VirtualHost *:{http_port}>
        ServerName {php_alias}.{domain}
        DocumentRoot {php_root}
        <Directory {php_root}>
            Require all granted
        </Directory>
    </VirtualHost>
"""



########################################################################
# PUBLIC METHODS
# If you want to add a new method, please follow the pattern from
# the other methods (Regex to check usage at beginning, method help if
# usage wont match, etc).
########################################################################
def config( args ):
    """
        Usage: python helper.py config <feature> on <server> (with database)
        Installs the desired app on the remote.
        :args: A string indicating the server to run the update.
    """

    # The usage regex.
    usage_pattern = "^(site|php) on {0}( with database)?$".format( AVAILABLE_SERVERS_PATTERN )
    cmd_str = " ".join( args )

    # Checks if the user typed the command correctly
    if not re.match( usage_pattern, cmd_str ):
        print
        print( "usage: python {0} {1} {2}".format( __file__, config.__name__, usage_pattern ) )
        print
        print( "Params explanation:")
        print( "    {0}{1}".format( "(site|php)".ljust( N_DEFAULT_HELP_SPACING ), "The application to install." ) )
        print( "    {0}{1}".format( "(local|dev|prod)".ljust( N_DEFAULT_HELP_SPACING ), "The server to configure." ) )
        print( "    {0}{1}".format( "[with database]".ljust( N_DEFAULT_HELP_SPACING ), "(Optional) Indicates to install a local database on the server." ) )
    else:

        # The commands to be executed in the server
        remote_commands = []

        # The command to generate the conf file for the specified app
        conf_file_generator_cmd = ""

        # Extracts params from command line
        app = args[0] # App
        server = args[2] # Server

        # The number of the ports to display on the .conf files
        http_workaround_port = ""
        https_workaround_port = ""
        php_workaround_port = ""

        # Connecting to the server
        if server == "local":
            commands = [ "vagrant ssh" ]
        else:
            commands = [ "ssh", "-i", SERVERS[ server ][ "KEYPAIR" ], "{0}@{1}".format( SERVERS[ server ][ "DEFAULT_USER" ], SERVERS[ server ][ "IP" ] ) ]

        # Creates the user group and adds server's and apache's user to it.
        remote_commands.append( "echo \" \"" )
        remote_commands.append( "echo \"##############################\"" )
        remote_commands.append( "echo \"# CONFIG. GROUP PERMISSIONS  #\"" )
        remote_commands.append( "echo \"##############################\"" )
        remote_commands.append( "echo \" \"" )
        remote_commands.extend( [
            "sudo groupadd {0}".format( DEFAULT_USER_GROUP ),
            "sudo usermod -a -G {0} {1}".format( DEFAULT_USER_GROUP, SERVERS[ server ][ "DEFAULT_USER"] ),
            "sudo usermod -a -G {0} {1}".format( DEFAULT_USER_GROUP, APACHE_DEFAULT_USER ),
        ] )
        remote_commands.append( "echo \"   ...DONE!\"" )

        # Updates apt-get
        remote_commands.append( "echo \" \"" )
        remote_commands.append( "echo \"#########################\"" )
        remote_commands.append( "echo \"# UPDATING APT-GET      #\"" )
        remote_commands.append( "echo \"#########################\"" )
        remote_commands.append( "echo \" \"" )
        remote_commands.append( "sudo apt-get update" )
        remote_commands.append( "echo \"   ...DONE!\"" )

        # Install packages
        remote_commands.append( "echo \" \"" )
        remote_commands.append( "echo \"##################################\"" )
        remote_commands.append( "echo \"# INSTALLING REQUIRED PACKAGES   #\"" )
        remote_commands.append( "echo \"##################################\"" )
        remote_commands.append( "echo \" \"" )

        INSTALL_PACKAGES = PHP_PACKAGES
        for package in INSTALL_PACKAGES:
            remote_commands.append( "sudo apt-get install {0} --yes".format( package ) )
        remote_commands.append( "echo \"   ...DONE!\"" )

        # Checks for the WITH param to know if
        # there is more features to install, like database.
        if "with" in args:

            # LOCAL DATABASE required?
            if "database" in args:
                # Asks for root password
                root_password = input( "Please type the root's password for MySQL: " )
                root_password_confirm = input( "Please confirm the root's password for MySQL: " )

                # If they are different, return.
                if root_password != root_password_confirm:
                    print( "Error: Passwords do not match." )
                    return

                # Add commands to install the mysql-server
                remote_commands.append( "echo \" \"" )
                remote_commands.append( "echo \"############################\"" )
                remote_commands.append( "echo \"# INSTALLING MYSQL-SERVER  #\"" )
                remote_commands.append( "echo \"############################\"" )
                remote_commands.append( "echo \" \"" )
                remote_commands.extend( [
                    "echo mysql-server mysql-server/root_password password {0} | sudo debconf-set-selections".format( root_password ),
                    "echo mysql-server mysql-server/root_password_again password {0} | sudo debconf-set-selections".format( root_password ),
                    "sudo apt-get -y install mysql-server",
                ] )
                remote_commands.append( "echo \"   ...DONE!\"" )


        # Creating the project's root folder
        remote_commands.append( "echo \" \"" )
        remote_commands.append( "echo \"########################\"" )
        remote_commands.append( "echo \"# CREATING ROOT FOLDER #\"" )
        remote_commands.append( "echo \"########################\"" )
        remote_commands.append( "echo \" \"" )
        remote_commands.extend([
            "sudo mkdir -p {0}".format( PROJECT_ROOT ),
            "sudo chown {0}:{1} {2}".format( SERVERS[ server ][ "DEFAULT_USER" ], DEFAULT_USER_GROUP, PROJECT_ROOT ),
            "sudo chgrp -R {0} {1}".format( DEFAULT_USER_GROUP, PROJECT_ROOT ),
            "cd {0}".format( PROJECT_ROOT ),
            "sudo mkdir -p {0}".format( PHP_ROOT ),
            "sudo chown -R {0}:{1} {2}".format( SERVERS[ server ][ "DEFAULT_USER" ], DEFAULT_USER_GROUP, PHP_ROOT ),
            "sudo chgrp -R {0} {1}".format( DEFAULT_USER_GROUP, PHP_ROOT ),
        ])
        remote_commands.append( "echo \"   ...DONE!\"" )



        ######################################
        # Configuring Apache Conf
        ######################################
        # Formats the conf file for the given server
        php_conf = WIKI_CONF.format(
            http_port = SERVERS[ server ][ "HTTP_PORT" ],
            php_alias = PHP_ALIAS,
            domain = SERVERS[ server ][ "DOMAIN" ],
            php_root = PHP_ROOT
        )

        remote_commands.append( "echo \" \"" )
        remote_commands.append( "echo \"#############################\"" )
        remote_commands.append( "echo \"# GENERATING PHP.CONF FILE #\"" )
        remote_commands.append( "echo \"#############################\"" )
        remote_commands.append( "echo \" \"" )
        # Creates the conf file containing the virtualhosts for the php on apache sites-enabled folder.
        remote_commands.extend([
            "sudo touch {0}/{1}.conf".format( APACHE_SITES_ENABLED_PATH, PHP_ALIAS ),
            "sudo chmod 777 {0}/{1}.conf".format( APACHE_SITES_ENABLED_PATH, PHP_ALIAS ),
            "echo \"{0}\" > {1}/{2}.conf".format( php_conf, APACHE_SITES_ENABLED_PATH, PHP_ALIAS ),
            "sudo chmod 644 {0}/{1}.conf".format( APACHE_SITES_ENABLED_PATH, PHP_ALIAS ),
        ])
        remote_commands.append( "echo \"   ...DONE!\"" )

        # Downloading git code.
        if server != "local":
            remote_commands.append( "echo \" \"" )
            remote_commands.append( "echo \"#########################\"" )
            remote_commands.append( "echo \"# DOWNLOADING CODE      #\"" )
            remote_commands.append( "echo \"#########################\"" )
            remote_commands.append( "echo \" \"" )
            remote_commands.extend([
                "cd {0}".format( PROJECT_ROOT ),
                "git clone {0} temp".format( GIT_REPO ),
                "shopt -s dotglob",
                "mv temp/* {0}".format( PROJECT_ROOT ),
                "git checkout {0}".format( SERVERS[ server ][ "BRANCH" ] ),
                "rm -R temp",
                "rm -R infra",
            ])
            remote_commands.append( "echo \"   ...DONE!\"" )

        # Enabling mode rewrite on apache
        remote_commands.append( "echo \"Enabling mode rewrite\"" )
        remote_commands.append( "sudo a2enmod rewrite" )

        # Clears apache's default conf.
        remote_commands.append( "echo \"Removing apache's default conf file\"" )
        remote_commands.append( "sudo rm {0}/000-default.conf".format( APACHE_SITES_ENABLED_PATH ) )

        # Reinforce the owner and group of all project's folders
        remote_commands.append( "echo \"Reinforcing owner and group over all project's folders\"" )
        remote_commands.extend([
            "sudo chown -R {0}:{1} {2}".format( SERVERS[ server ][ "DEFAULT_USER" ], DEFAULT_USER_GROUP, PROJECT_ROOT ),
            "sudo chgrp -R {0} {1}".format( DEFAULT_USER_GROUP, PROJECT_ROOT ),
        ])

        # Restarting apache
        remote_commands.append( "sudo service apache2 restart" )
        call_by_cloning_script( server, remote_commands )

        # Print ending hints
        print()
        print()
        print( "###############################################")
        print( "# Installation COMPLETE")
        print( "###############################################")
        print()


def connect( args ):
    """
        Connects to the specified server via ssh.
        :args: A string indicating the server to connect to.
    """

    # The usage regex.
    usage_pattern = "{0}".format( AVAILABLE_SERVERS_PATTERN )
    cmd_str = " ".join( args )

    # Checks if the user typed the command correctly
    if not re.match( usage_pattern, cmd_str ):
        print
        print( "usage: python {0} {1} {2}".format( __file__, connect.__name__, usage_pattern ) )
        print
        print( "Params explanation:")
        print( "    {0}{1}".format( "local".ljust( N_DEFAULT_HELP_SPACING ), "Connects to your local vagrant instance." ) )
        print( "    {0}{1}".format( "dev".ljust( N_DEFAULT_HELP_SPACING ), "Connects to your development instance." ) )
        print( "    {0}{1}".format( "prod".ljust( N_DEFAULT_HELP_SPACING ), "Connects to production instance." ) )
    else:
        # Gets the server name
        server = args[0]

        # Connects to the server.
        if server == "local":
            return cmd( "vagrant ssh" )
        else:
            return cmd( "ssh -i {0} {1}@{2}".format( SERVERS[ server ][ "KEYPAIR" ], SERVERS[ server ][ "DEFAULT_USER" ], SERVERS[ server ][ "IP" ] ) )


def restart( args ):
    """
        Restarts the required services running on the server.
        :args: A string indicating the server to restart.
    """

    # The usage regex.
    usage_pattern = "{0}".format( AVAILABLE_SERVERS_PATTERN )
    cmd_str = " ".join( args )

    # Checks if the user typed the command correctly
    if not re.match( usage_pattern, cmd_str ):
        print
        print( "usage: python {0} {1} {2}".format( __file__, restart.__name__, usage_pattern ) )
        print
        print( "Params explanation:")
        print( "    {0}{1}".format( "local".ljust( N_DEFAULT_HELP_SPACING ), "Restarts the services on the local instance (vagrant)." ) )
        print( "    {0}{1}".format( "dev".ljust( N_DEFAULT_HELP_SPACING ), "Restarts the services on the development instance." ) )
        print( "    {0}{1}".format( "prod".ljust( N_DEFAULT_HELP_SPACING ), "Restarts the services on the production instance." ) )
    else:
        # Gets the server name
        server = args[0]
        services = [ "mysql", "apache2" ]

        cmd_str = ""
        for service in services:
            cmd_str += "sudo service {0} restart; ".format( service )

        if server == "local":
            cmd( "vagrant ssh -c '{0}'".format( cmd_str ) )
        else:
            # Generates the ssh command for the given server
            ssh_command = "ssh -i {0} {1}@{2} -t".format(
                SERVERS[ server ][ "KEYPAIR" ],
                SERVERS[ server ][ "DEFAULT_USER" ],
                SERVERS[ server ][ "IP" ]
            )
            cmd( "{0} '{1}'".format( ssh_command, cmd_str ) )


def update( args ):
    """
        Updates the code of the instance with git HEAD modifications.
        :args: A string indicating the server to run the update.
    """
    # The usage regex.
    usage_pattern = "{0}".format( AVAILABLE_SERVERS_PATTERN )
    cmd_str = " ".join( args )

    # Checks if the user typed the command correctly
    if not re.match( usage_pattern, cmd_str ):
        print
        print( "usage: python {0} {1} {2}".format( __file__, update.__name__, usage_pattern ) )
        print
        print( "Params explanation:")
        print( "    {0}{1}".format( "local".ljust( N_DEFAULT_HELP_SPACING ), "Updates your local instance." ) )
        print( "    {0}{1}".format( "dev".ljust( N_DEFAULT_HELP_SPACING ), "Updates your development instance." ) )
        print( "    {0}{1}".format( "prod".ljust( N_DEFAULT_HELP_SPACING ), "Updates your production instance." ) )
    else:
        # Configuring the params and the commands to call.
        server = args[0]

        remote_commands = []
        # Connects to the server.
        if server == "local":
            remote_commands = [
                "sudo service apache2 restart",
            ]

        else:
            # Configuring the remote commands.
            remote_commands = [
                "cd {0}".format( PROJECT_ROOT ),
                "git checkout {0}".format( SERVERS[ server ][ "BRANCH" ] ),
                "git pull origin {0}".format( SERVERS[ server ][ "BRANCH" ] ),
                "rm -R infra",
                "sudo service apache2 restart",
            ]

        return call_by_cloning_script( server, remote_commands )


###########################################################
# Utility function to extract the filename from a string.
###########################################################
def path_leaf( path ):
    import ntpath
    head, tail = ntpath.split( path )
    return tail or ntpath.basename( head )
###########################################################


def copy( args ):
    """
    Copy a file or a folder from/to the remote server.
    :args: A set of arguments including the server to run the command, the file and
    recursive option.
    """
    # The usage regex.
    usage_pattern = "[^ ]+( -[rR])? (from|to) {0} (to|into) [^ ]+".format( AVAILABLE_SERVERS_PATTERN )
    cmd_str = " ".join( args )

    # Check if the minimal number of arguments was passed.
    if not re.match( usage_pattern, cmd_str ):
        print
        print( "usage: python {0} {1} <file> [-r] from <server> to <local_path>".format( __file__, copy.__name__ ) )
        print( "usage: python {0} {1} <file> [-r] to <server> into <remote_path>".format( __file__, copy.__name__ ) )
        print
        print( "Params explanation:")
        print( "    {0}{1}".format( "file".ljust( N_DEFAULT_HELP_SPACING ), "The file or folder to be copied." ) )
        print( "    {0}{1}".format( "-r".ljust( N_DEFAULT_HELP_SPACING ), "(Optional) param indicating to download the <file> path recursively." ) )
        print( "    {0}{1}".format( "dev".ljust( N_DEFAULT_HELP_SPACING ), "Copy files from/to the development server." ) )
        print( "    {0}{1}".format( "prod".ljust( N_DEFAULT_HELP_SPACING ), "Copy files from/to the production server." ) )
        print( "    {0}{1}".format( "local_path".ljust( N_DEFAULT_HELP_SPACING ), "The directory on your local machine to put the file." ) )
        print( "    {0}{1}".format( "remote_path".ljust( N_DEFAULT_HELP_SPACING ), "The directory on your remote to put the file." ) )
    else:
        # Extracts the recursive param
        recursive = ( "-r" in args or "-R" in args )
        if recursive:
            del args[1]

        # Extracts the other params (Note: The recursive arg was removed if it was passed).
        src = args[0]
        from_to = args[1]
        server = args[2]
        dest = args[4]

        ################################
        # Copying from server to local.
        ################################
        if from_to == "from":
            # The scp command with params set.
            commands = [ "scp", "-r", "-i", SERVERS[ server ][ "KEYPAIR" ], "{0}@{1}:{2}".format( SERVERS[ server ][ "DEFAULT_USER" ], SERVERS[ server ][ "IP" ], src ), dest ]
            if not recursive:
                commands.remove( "-r" )

            return cmd( commands )

        ################################
        # Copying from local to server.
        ################################
        else:
            if recursive:   # Recursive? (src and dest are folders)
                commands = [ "scp", "-r", "-i", SERVERS[ server ][ "KEYPAIR" ], src, "{0}@{1}:{2}".format( SERVERS[ server ][ "DEFAULT_USER" ], SERVERS[ server ][ "IP" ], dest ) ]
            else:
                # Extracts the filename from source
                filename = path_leaf( src )
                if not dest.endswith( os.pathsep ):
                    filename = '/' + filename

                commands = [ "scp", "-i", SERVERS[ server ][ "KEYPAIR" ], src,  "{0}@{1}:{2}{3}".format( SERVERS[ server ][ "DEFAULT_USER" ], SERVERS[ server ][ "IP" ], dest, filename ) ]
            return cmd( commands )










########################################################################
# INTERNAL METHODS
# Please do not modify the code above if you don't know what you're doing.
# This script was made to you just modify the configurations bellow.
########################################################################
def init():
    """
        Parse the command line params and calls the desired method.
        If the method is not encountered displays the help.
    """
    if len( sys.argv ) > 1:
        # Tries to get the method to be called.
        method = globals().get( sys.argv[1] )
        # Gets the params
        params = sys.argv[2:]

        # If method exists
        if method:
            method( params )
        # Else Displays help
        else:
            h()
    # Displays help
    else:
        h()



def h():
    """
        Displays info about the helper's methods.
    """

    # A big list of dictionaries mapping available methods names
    # and its respectives descriptions
    METHODS_HELP = [
        {
            "name": config.__name__,
            "description": "Configures a site or php on the remote server."
        },

        {
            "name": connect.__name__,
            "description": "Connects via ssh to the remote server."
        },
        {
            "name": update.__name__,
            "description": "Updates the remote server."
        },
        {
            "name": copy.__name__,
            "description": "Copy files from/to remote server."
        },
        {
            "name": restart.__name__,
            "description": "Restarts the services running on the server."
        },
    ]
    print
    print( "USAGE: python {0} <command> <params>".format( __file__ ) )
    print
    print( "Available commands:" )

    for help in METHODS_HELP:
        print( "    {0}{1}".format( help[ "name" ].ljust( N_DEFAULT_HELP_SPACING ), help[ "description" ] ) )



def cmd( commands ):
    """
        Internal function. Used to call command line methods and pass input to it.
    """

    # Converts commands to string
    if type( commands ) is list:
        commands = " ".join( commands )

    # Calls the command
    shell = subprocess.call( commands, shell = True )



def call_by_cloning_script( server, commands ):

    # Generates the script file.
    script_filename = "cs-{0}.sh".format( time.time() )
    with open( script_filename, "wb" ) as script:
        script.write( bytes( "\n".join( commands ).replace( "\r", '' ), "UTF-8" ) )


    # Sending and executing the script
    if server == "local":
        cmd( "vagrant ssh -c 'bash /vagrant/{0};'".format( script_filename ) )
    else:
        home_folder = "/home/" + SERVERS[ server ][ "DEFAULT_USER" ]
        copy( [ script_filename, "to", server, "into", home_folder ] )

        # Generates the ssh command for the given server
        ssh_command = "ssh -i {0} {1}@{2} -t".format(
            SERVERS[ server ][ "KEYPAIR" ],
            SERVERS[ server ][ "DEFAULT_USER" ],
            SERVERS[ server ][ "IP" ]
        )

        # The full path to the script on the remote server
        script_remote_path = home_folder + '/' + script_filename

        # Call the script and removes it
        callcmd = "{0} 'bash {1}; sudo rm {1};'".format( ssh_command, script_remote_path )
        cmd( callcmd )

    # Removes the generated file
    cmd( "rm {0}".format( script_filename ) )

# Calls the initial method and exit.
init()
exit()