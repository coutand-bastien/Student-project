# Projet S7 (web platform to monitor room occupancy in real time)


The platform would be accessible to all the actors involved in this service as well as to those responsible for timetables. The objective would be to acquire a global vision of the state of the rooms and to be able to extract statistics in order to support the decisions taken by the service and to propose solutions in case of conflict. The challenge is also to better anticipate the evolution of the campus population, Indeed, it is quite possible with this information to anticipate the arrival of The challenge is also to better anticipate the evolution of the campus population, as it is quite possible with this information to anticipate the arrival of additional classes following the opening of a new course. 

<br>

# Pre-requisite

You need to download the [source code](https://forgens.univ-ubs.fr/gitlab/e2100676/projets7.git) :

``` bash
$ git clone https://forgens.univ-ubs.fr/gitlab/e2100676/projets7.git
```

You need also [docker-compose](https://www.docker.com/products/docker-desktop/) to launch the application container and the database container and [mysql-client](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html) to be able to connect to the database via the CLI.

## Linux

``` bash
$ sudo apt-get install docker-compose 
$ sudo apt-get install mysql-client
```

## Windows
### Docker-compose

Download [docker-compose](https://www.docker.com/products/docker-desktop/) and start the installation, it is very simple. **Make sure you check "Install required Windows components for WSL 2" during the installation.**

Now open Docker Desktop if it is not already open. **Click on the settings icon on the top right**. In the "General" tab, I invite you to check the "Use the WSL 2 based engine" option if it is not already checked.

Next, click on the **Resources > WSL Integration**. This is where you need to select the distributions for which you want to enable Docker support.
By default, the option "Enable integration with my default WSL distro" is checked. This means that your default Linux distribution already has Docker support.

Now you need to open the distribution for which you have previously activated Docker.

``` bash
wsl -d <linux_distribution>
```

### MYSQL-client

Follow the [link](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html)

<br>

# Launch

Then you will need launch the 2 containers with docker-compose and after wait for the application to launch ~ 30s

## Linux
 
``` bash
$ cd server # if you are not already in the repository
$ sudo docker-compose up -d
```

## Windows

``` bash
$ cd server # if you are not already in the repository
$ docker-compose up -d
```


<br>

# Usage
## App
<br>
<center>

### The app at http://192.168.10.3:8000

</center>

<br>
<br>

The documentation is available at http://192.168.10.3:8000/docs


## Database
To see the database follow the order below (password=123):
``` bash
$ mysql --host=192.168.10.2 --port=3306 -u root -p
```

## CAS
If you want to change the CAS server to your own you can do so by changing the line CAS_IP and CAS_PORT in the [.env](./server/app-container/.env) file.

After that, you have to setup your CAS users with their rights in the database by modifying the [init_db.py](./server/app-container/api/database/init_db.py) file. 


><i>('e2100676', 1) --> The user e2100676 has the admin role
>
>('e2485631', 2) --> The user e2485631 has the supervisor role
>
>('e2107325', 3) --> The user e2107325 has the reader role
>
>('e2108676', 4) --> The user e2108676 has the new_user role</i>

<br>

# Authors and acknowledgment

## Programmer
COUTAND Bastien (coutand.e2100676@etud.univ-ubs.fr)  
DAOUDI Elyes (daoudi.e2105383@etud.univ-ubs.fr)  
DENOUE Enzo (denoue.e187412@etud.univ-ubs.fr)  
MARCHAND Robin (marchand.e2101234@etud.univ-ubs.fr)  

## CAS master
MORVAN Fabien (morvan.e2103606@etud.univ-ubs.fr) 

<br>

# License

ENSIBS licensed

<br>

# Project status

DEVELOPPEMENT