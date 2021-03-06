# gcloud auth login

instance_names=(
    "instance-extra-1-07zg"
    "instance-extra-1-0x5l"
    "instance-extra-1-3gwq"
    "instance-extra-1-578b"
    "instance-extra-1-596n"
    "instance-extra-1-5hxj"
    "instance-extra-1-609c"
    "instance-extra-1-8m0f"
    "instance-extra-1-8qs9"
    "instance-extra-1-csnb"
    "instance-extra-1-f7jr"
    "instance-extra-1-g674"
    "instance-extra-1-k5n7"
    "instance-extra-1-kt9f"
    "instance-extra-1-kw4m"
    "instance-extra-1-n0r9"
    "instance-extra-1-p3kr"
    "instance-extra-1-rmcn"
    "instance-extra-1-t4cx"
    "instance-extra-1-tl3w"
)

counter=1

for instance_name in ${instance_names[@]}; do
    echo $instance_name
    # Connect using SSH
    #gcloud compute ssh --project=directed-pier-294505 --zone=us-west2-a $instance_name --command='sudo apt update -y && sudo apt install -y nano git screen unzip zip && sudo apt install -y apt-transport-https ca-certificates curl software-properties-common && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable" && sudo apt update -y && apt-cache policy docker-ce && sudo apt install -y docker-ce && sudo usermod -aG docker ${USER} && su - ${USER} && id -nG && sudo curl -L "https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose'
    gcloud compute ssh --project=directed-pier-294505 --zone=us-west2-a $instance_name --command="cd prometeo && sudo git pull && sudo python3 scripts/split_file.py --path valid_zipcodes.csv --chunks ${#instance_names[@]} --keep $counter"
    let counter++
    # # Create a screen
    # screen
    # # Build containers
    # cd prometeo && sudo git pull && sudo docker-compose up -d --build && sudo docker exec -it prometeo_server_1 bash
    # python3 fetchers/test_all/run.py --workers 3
    echo "ending" 
    echo $counter
done
