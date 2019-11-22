sudo mkdir /data

sudo mkdir /data/db
sudo mongod --dbpath . --bind_ip 0.0.0.0 --port 7050
