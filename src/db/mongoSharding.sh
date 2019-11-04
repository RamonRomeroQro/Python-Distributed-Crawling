# A Shard – This is the basic thing, and this is nothing but a MongoDB instance which holds the subset of the data. In production environments, all shards need to be part of replica sets.
# (Clients)

# Config server – This is a mongodb instance which holds metadata about the cluster, basically information about the various mongodb instances which will hold the shard data.
# (Master)

# A Router – This is a mongodb instance which basically is responsible to re-directing the commands send by the client to the right servers.


sudo mkdir /data/configdb

mongod –configdb ServerD: 27019

# Step 3) Start the mongos instance by specifying the configuration server

mongos –configdb ServerD: 27019