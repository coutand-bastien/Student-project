# Install elastic search with docker (https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)
```bash
$ docker network create elastic
$ docker pull docker.elastic.co/elasticsearch/elasticsearch:8.10.2
$ docker run -d --name es01 --net elastic -p 9200:9200 -it -m 8GB docker.elastic.co/elasticsearch/elasticsearch:8.10.2
```
If there is an error with the memory, you can add the following option to the docker run command:
```bash
$ sudo sh -c 'echo "vm.max_map_count = 262144" >> /etc/sysctl.conf'
$ sudo sysctl -p
```
After that you need to get the password and certificate:
```bash
$ docker logs es01 | grep "PASSWORD elastic"
$ docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .
```
### Reset password and create enrollment token
```bash
$ docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
$ docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
```
### Test
```bash
$ export ELASTIC_PASSWORD="your_password"
$ curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
```

### **!!! You need to copy the password of your elastic in the .env !!!**
```env
...
ELASTIC_PASSWORD=**your_password**
...
CRT_PATH=**your_path_to_the_certificate**
...