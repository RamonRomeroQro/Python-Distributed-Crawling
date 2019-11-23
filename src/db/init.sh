DIR="./data"
if [ -d "$DIR" ]; then
    ### Take action if $DIR exists ###
    echo "Installing db files in ${DIR}..."
else
    ###  Control will jump here if $DIR does NOT exists ###
    mkdir $DIR
    echo "Installing db files in ${DIR}..."

fi
sudo mongod --dbpath ./data --bind_ip 0.0.0.0 --port 7050

# mongo --port 7050
