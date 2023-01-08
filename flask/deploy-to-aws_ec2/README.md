# Deploy to AWS

## Setup ec2 Instance for Deployment

Set `400` permissions to private key.

After logging in to ec2 instance as `ec2-user`, [add user to docker user group](https://stackoverflow.com/questions/47854463/docker-got-permission-denied-while-trying-to-connect-to-the-docker-daemon-socke) 
so you can run  docker commands without sudo.

```bash
sudo usermod -a -G docker
docker:x:998:ec2-user
newgrp docker
```

### Install `docker-compose`

```bash
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose version
```

## Inbound/Outbound Rules in Security Group

Inbound
```
IPv4	HTTP	TCP	80	0.0.0.0/0
IPv4	HTTPS	TCP	443	0.0.0.0/0
IPv4	SSH	    TCP	22	<MY-IP>
```

Outbound
```
IPv4	"All traffic"	All	All	0.0.0.0/0
```

## Docker

Expose port 5000 in `Dockerfile`.

Connect host's port 80 to docker container's port 5000 `80:5000`.

```bash
docker-compose up -d
curl localhost
```

Open up the instance's public IPV4 address or public IPV4 DNS in browser.

`ec2-x-y-z-a.ap-south-1.compute.amazonaws.com `

## Resources

- [Deploying Docker Containers with AWS ec2 instance](https://medium.com/@chandupriya93/deploying-docker-containers-with-aws-ec2-instance-265038bba674)