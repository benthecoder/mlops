# setup aws

## launch ec2 instance

1. choose OS and architecture
   - ubuntu OS image
   - 64-bit x86 architecture
2. Choose instance type
   - t2.xlarge
3. create key pair
   - give name and select .pem
   - place in `~/.ssh` filder
4. configure storage
   - set 30 GB storage
5. copy public IP
6. `chmod 400 ~/.ssh/<key>.pem`
7. run `ssh -i path/to/key.pem ubuntu@public_ip`
   - for "WARNING: UNPROTECTED PRIVATE KEY FILE!" error, do `sudo chmod 600 /path/to/key.pem`
   - for permission denied? username might be wrong, go connect to instance and check username
