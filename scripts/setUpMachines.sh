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

N=50
for instance_name in ${instance_names[@]}; do
    echo $instance_name
    ((i=i%N)); ((i++==0)) && wait
    # Connect using SSH
    #gcloud compute ssh --project=directed-pier-294505 --zone=us-west2-a $instance_name --command='sudo apt update -y && sudo apt install -y nano git screen unzip zip && sudo apt install -y apt-transport-https ca-certificates curl software-properties-common && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable" && sudo apt update -y && apt-cache policy docker-ce && sudo apt install -y docker-ce && sudo usermod -aG docker ${USER} && su - ${USER} && id -nG && sudo curl -L "https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose'
    (gcloud compute scp --recurse --zone=us-west2-a Archive.zip $instance_name:~
    gcloud compute scp --recurse --zone=us-west2-a config/secrets.env $instance_name:~
    gcloud compute ssh --project=directed-pier-294505 --zone=us-west2-a $instance_name --command='sudo git clone https://github.com/OneStarSolution/prometeo.git && sudo mkdir prometeo/data && sudo mkdir prometeo/data/enhanced && sudo mkdir prometeo/data/phones_urls && sudo mkdir prometeo/data/yelp_data && sudo mv secrets.env prometeo/config && sudo unzip Archive.zip -d prometeo && cd prometeo && sudo git checkout run_quick && bash scripts/run.sh && sudo docker-compose up -d --build'
    #gcloud compute ssh --project=directed-pier-294505 --zone=us-west2-a $instance_name --command="cd prometeo/ && sudo git pull && cd .. && bash prometeo/scripts/start.sh"
    ) &

    # # Create a screen
    # screen
    # # Build containers
    # cd prometeo && sudo git pull && sudo docker-compose up -d --build && sudo docker exec -it prometeo_server_1 bash
    # python3 fetchers/test_all/run.py --workers 3
    echo "ending" 
done
