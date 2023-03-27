# MonkEy-commerce

Site de ecommerce utilisant jakartaEE, docker, mysql

# Configuration de l'environnement de développement sous IntelliJ IDEA

## Téléchargement et installation de Java 17

Téléchargez Java 17 à partir du site officiel : https://www.oracle.com/java/technologies/downloads/#java17.

## Téléchargement et installation de IntelliJ IDEA

Téléchargez IntelliJ IDEA à partir du site officiel : https://www.jetbrains.com/idea/download/.

## Téléchargement et installation de Git

Téléchargez Git à partir du site officiel : https://git-scm.com/downloads.

## Configuration de Git

1. Ouvrez le terminal de votre système d'exploitation.
2. Exécutez la commande suivante pour clone le dépôt Git :

```bash
git clone https://github.com/coutand-bastien/ecommerce.git
```


# Configuration docker MySQL8 et Payara 6.2023.1

## Installation de Docker Compose et lancement d'une instance de MySQL8

1. Installez Docker Compose en suivant les instructions officielles : https://docs.docker.com/compose/install/.
2. Créez un fichier `docker-compose.yml` dans le répertoire de votre choix.
3. Ajoutez le contenu suivant pour lancer une instance de MySQL8 et charger un script SQL pour initialiser la base de données :

```yaml
   version: '3.9'

   services:
     db:
       image: mysql:8.0.31
       container_name: mysql
       restart: always
       ports:
         - "3306:3306"
       volumes:
         - ./script/<fichier-construcrt-db.sql>:/docker-entrypoint-initdb.d/contruct_ecommerce_db.sql
       environment:
         MYSQL_ROOT_PASSWORD: 123
         MYSQL_DATABASE: <database-name>
```

Le fichier `<fichier-construcrt-db.sql>` doit être situé dans le répertoire `./script/` et doit contenir les instructions SQL nécessaires pour créer les tables et les données de votre application.
De plus, `<database-name>` doit être remplacé par le nom de la base de données que vous souhaitez créer.

4. Enregistrez le fichier `docker-compose.yml`.
5. Dans le répertoire où se trouve le fichier `docker-compose.yml`, exécutez la commande suivante pour lancer l'instance de MySQL8 :

```bash
docker-compose up -d
```

## Configuration de la base de données sous IntelliJ IDEA

1. Ouvrez IntelliJ IDEA.
2. Allez dans le menu DataBase > Data Source > MySQL.
3. Cliquez sur le bouton `+` pour ajouter une nouvelle source de données.
4. Remplissez les champs comme suit : `host : localhost, port : 3306, username : root, password : 123, database : ecommerce`.
5. Cliquez sur le bouton `Test Connection` pour tester la connexion.

## Installation de Payara 6.2023.1

1. Téléchargez Payara Server 6.2023.1 à partir du site officiel : https://www.payara.fish/downloads/payara-server-full/.
2. Extrayez le contenu de l'archive téléchargée dans un répertoire de votre choix.
3. Allez dans le répertoire où vous avez extrait l'archive et exécutez la commande `./bin/asadmin start-domain` pour démarrer le serveur Payara.

## Configuration de payara et ajout du war sous IntelliJ IDEA

1. Ouvrez IntelliJ IDEA.
2. Allez dans le menu Run > Edit Configurations.
3. Cliquez sur le bouton `+` pour ajouter une nouvelle configuration.
4. Sélectionnez `Payara Server` dans la liste des configurations.
5. Remplissez les champs comme suit : `Name : Payara, Domain : domain1, url : http://localhost:8080/, Username : admin, Password : admin`.
6. Cliquez sur le bouton `Apply` puis sur le bouton `OK` pour enregistrer la configuration.
7. Cliquez sur le bouton `+` pour ajouter un nouveau déploiement.
8. Sélectionnez le fichier `war` de votre projet Java.
9. Cliquez sur le bouton `Apply` puis sur le bouton `OK` pour enregistrer la configuration.

## Création d'un pool MySQL8

1. Téléchargez le pilote JDBC pour MySQL8 depuis le site officiel : https://dev.mysql.com/downloads/connector/j/.
2. Placez le fichier JAR dans le répertoire `glassfish/domains/domain1/lib` ou exécutez la commande suivante pour le copier dans le répertoire :

```bash
./bin/asadmin add-library <chemin-vers-le-fichier-jar>
```

3. Exécutez la commande suivante pour créer un pool de connexions :

```bash
./bin/asadmin create-jdbc-connection-pool --datasourceclassname=com.mysql.cj.jdbc.MysqlDataSource --restype=javax.sql.DataSource --property=user=<utilisateur>:password=<mot-de-passe>:DatabaseName=<nom-de-la-base>:ServerName=<adresse-du-serveur>:port=<port-du-serveur>:UseSSL=false:allowPublicKeyRetrieval=true mysql8_pool
```

Remplacez `<utilisateur>`, `<mot-de-passe>`, `<nom-de-la-base>`, `<adresse-du-serveur>` et `<port-du-serveur>` par les informations de votre base de données MySQL8.

4. Exécutez la commande suivante pour tester la connexion :

```bash
./bin/asadmin ping-connection-pool mysql8_pool
 ```

## Création d'une ressource de données

5. Exécutez la commande suivante pour créer une ressource de données (JNDI) associée au pool de connexions MySQL8 :

```bash
./bin/asadmin create-jdbc-resource --connectionpoolid mysql8_pool jdbc/mysql8_resource
```

Remplacez `mysql8_pool` par le nom du pool de connexions que vous avez créé à l'étape 3 et `jdbc/mysql8_resource` par le nom que vous souhaitez donner à la ressource JNDI.

## Configuration de persistence.xml

1. Créez un fichier `persistence.xml` dans le répertoire `src/main/resources/META-INF/` de votre projet Java.
2. Ajoutez la configuration suivante pour utiliser la ressource de données créée précédemment :

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<persistence xmlns="http://xmlns.jcp.org/xml/ns/persistence"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.2"
xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/persistence http://www.oracle.com/webfolder/technetwork/jsc/xml/ns/persistence/persistence_2_2.xsd">

<persistence-unit name="ecommercePersistenceUnit" transaction-type="JTA">
        <jta-data-source>jdbc/mysql8_pool</jta-data-source>
        <exclude-unlisted-classes>false</exclude-unlisted-classes>
        <shared-cache-mode>NONE</shared-cache-mode>
    </persistence-unit>
</persistence>
```

Remplacez `mysql8_pool` par le nom du pool de connexions que vous avez créé à l'étape 3 et `jdbc/mysql8_resource` par le nom que vous souhaitez donner à la ressource JNDI.

