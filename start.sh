
#Build images from dockerfile
sudo docker build --tag=scapy -f Dockerfiles/scapy/Dockerfile  Dockerfiles/scapy
sudo docker build --tag=odl -f Dockerfiles/odl/Dockerfile  Dockerfiles/odl

#Create directory for the dockers in file "red2.py"
sudo mkdir /home/juli/shvol

#run the odl docker
sudo docker run -t -d -p 6633:6633 -p 6653:6653 -p 8181:8181 -p 8101:8101 -p 2222:22 --name odl --privileged odl 
