# gcloud auth login

instance_names_query=("instance-extra-1-07zg"
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
    "instance-extra-1-tl3w")

instance_names=("instance-extra-1-07zg"
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
    "instance-extra-1-tl3w")
paths=()

for instance_name in ${instance_names_query[@]}; do
    echo $instance_name
    # Connect using SSH
    paths+=($(gcloud compute ssh --project=directed-pier-294505 --zone=us-west2-a $instance_name --command="ls prometeo/data/enhanced | grep tile"))
done

echo "----"
echo ${#paths[@]}
printf "%s\n" "${paths[@]}" > paths_crawled.txt
python3 scripts/get_missing_zipcodes.py -p heating+ -i ${#instance_names[@]} -r

counter=1
for instance_name in ${instance_names[@]}; do
    echo $instance_name
    # Connect using SSH
    # gcloud compute ssh --project=directed-pier-294505 --zone=us-west2-a $instance_name --command='sudo rm instance_*.txt'
    gcloud compute scp --recurse --zone=us-west2-a data/redistribution/instance_$counter.txt $instance_name:~
    gcloud compute ssh --project=directed-pier-294505 --zone=us-west2-a $instance_name --command='sudo mv instance_*.txt prometeo/redistribution.txt'
    let counter++

done    
    # # Create a screen
    # screen
    # # Build containers
    # cd prometeo && sudo git pull && sudo docker-compose up -d --build && sudo docker exec -it prometeo_server_1 bash
    # python3 fetchers/test_all/run.py --workers 3

