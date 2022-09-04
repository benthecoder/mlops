# GCP

1. Compute engine > vm instances > create instance
2. gcloud compute ssh --zone "ZONE" "INSTANCE_NAME" --project "PROJECT_NAME"
3. create a config file

```txt
Host mlops
  2   HostName <External_IP>
  3   User <username>
  4   IdentityFile <path to private key>
  5   StrictHostKeyChecking no
```

Now you can do `ssh mlops` to open the vm instance

alternative option for ssh keys:

- `ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048`
- add ssh public file to metadata ssh

## stop instances with gcloud

- `gcloud compute instances stop INSTANCE_NAME`

## install necessary libraries

install anaconda

- <https://www.anaconda.com/products/distribution> for linux
- run `bash filename.sh`

install docker and docker compose

- `sudo apt update`
- `sudo apt install docker.io`
- `sudo apt install docker-compose`
- `sudo usermod -aG docker $USER` (run docker without sudo)

## for ssh into vs code

- install remote - ssh extension
