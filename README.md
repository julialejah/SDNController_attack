# SDNController_attack

## Install on Azure:

Install MyDockerVM:

https://learn.microsoft.com/es-es/samples/azure/azure-quickstart-templates/docker-simple-on-ubuntu/

1. Change the template VM size from "Standard_F1" to "Standard B2s" (2 vcpu, 4 GiB de memoria). Standard_FW size does not have enough capacity to run the script "pyscripts/Data_gather_csv.py"
2. Install containernet Bare Metal
3. Clone SDNController_attack repository and run start.sh

## Install on Debian:
1. Create odl and scapy images from Dockerfiles in SDNController_attack Dockerfiles
2. Install containernet in Nested  Docker deployment (docker pull containernet/containernet)
3. Run container containernet from shell (docker run --name containernet -it --rm --privileged --pid='host' -v /var/run/docker.sock:/var/run/docker.sock containernet/containernet /bin/bash)
4. Inside the container, install scapy and pandas (pip3 install scapy pandas).
5. Inside the container, clone SDNController_attack repository
6. From the host shell, create a new image with the changes (sudo docker commit containernet sdnets)
7. Run the new image (sudo docker run --name sdnets -it --rm --privileged --pid='host' -v /var/run/docker.sock:/var/run/docker.sock sdnets /bin/bash)
