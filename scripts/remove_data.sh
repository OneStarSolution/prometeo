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

N=10
for instance_name in ${instance_names[@]}; do
    ((i=i%N)); ((i++==0)) && wait
    (echo $instance_name
    # Connect using SSH
    gcloud compute ssh --project=directed-pier-294505 --zone=us-west2-a $instance_name --command='sudo find . -wholename "./prometeo/data/enhanced/*" -delete && sudo find . -wholename "./prometeo/data/yelp_data/*" -delete && sudo find . -wholename "./prometeo/data/phones_urls/*" -delete'
    # # Create a screen
    # screen
    # # Build containers
    # cd prometeo && sudo git pull && sudo docker-compose up -d --build && sudo docker exec -it prometeo_server_1 bash
    # python3 fetchers/test_all/run.py --workers 3
    echo "ending" ) &
done
