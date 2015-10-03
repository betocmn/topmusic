# Top Music
A plain PHP/Angular JS app to list top artists and music by country, using LAST.FM'S or Spotify's API

- Server Automation Script (locally and in AWS)
- Custom MVC written in plain PHP
- Flexible to give support to any other vendor's API (last.fm, spotify, etc...)
- Angular JS for the views


### Technologies Used

#### Back-End
- PHP >= 5.4

#### Front-End
- Angular JS (HTML, CSS, JAVASCRIPT)

#### Server Side
- Ubuntu 14.0.4
- Vagrant
- Virtual Box
- GIT

#### APIs
- [Last.fm](http://www.last.fm/api)


### Installing required software
1. Install Vagrant (Go to: http://www.vagrantup.com/downloads.html)
2. Install Virtual Box (Go to: https://www.virtualbox.org/wiki/Downloads)
3. Install GIT, including command line options. (Go to: http://git-scm.com/downloads)
4. Install Python 3.4 (Go to: https://www.python.org/)


### Cloning the code

1. Clone the GIT Repository using the following command:
    ```
    git clone https://github.com/humbertomn/topmusic.git ~/topmusic
    ```

    PS: If you want to install anywhere on your system, change the path: "~/topmusic"

2. To start up your virtual environment, run the following command:
    ```
    cd ~/topmusic/infra
    vagrant up
    ```
    Vagrant is configured to use the ports 2222, 8080, 8181 and 4443, so make sure they are free to be used.

3. If you see an error message that starts with 'Failed to mount folders in Linux guest' run the following commands:
    ```
    vagrant ssh
    sudo useradd www-data
    sudo groupadd topmusic-dev
    sudo usermod -a -G topmusic-dev vagrant
    sudo usermod -a -G topmusic-dev www-data
    exit
    vagrant reload
    ```

4. Run the following command to configure your environment (Make sure you're still in the 'infra' folder).
    ```
    python helper.py config site on local
    ```

    The helper.py script will install all needed packages on your local environment, such as apache and git.


### Testing
To make sure it works open up http://localhost:8080/
