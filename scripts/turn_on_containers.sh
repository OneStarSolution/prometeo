# gcloud auth login

# instance_names=("instance-extra-1-07zg" "instance-extra-1-0x5l" "instance-extra-1-3gwq" "instance-extra-1-578b" "instance-extra-1-596n" "instance-extra-1-5hxj" "instance-extra-1-609c"
# "instance-extra-1-8m0f" "instance-extra-1-8qs9" "instance-extra-1-csnb" "instance-extra-1-f7jr" "instance-extra-1-g674" "instance-extra-1-k5n7"
# "instance-extra-1-kt9f" "instance-extra-1-kw4m" "instance-extra-1-n0r9" "instance-extra-1-p3kr" "instance-extra-1-rmcn" "instance-extra-1-t4cx" "instance-extra-1-tl3w")

instance_names=("instance-team-1-2j48" "instance-team-1-3ph2" "instance-team-1-95x5" "instance-team-1-ch6w" "instance-team-1-fxfl" "instance-team-1-g03g" "instance-team-1-hb8h" "instance-team-1-j0k2" "instance-team-1-jkm2" "instance-team-1-kzq9" "instance-team-1-m42s" "instance-team-1-m9mp" "instance-team-1-mk32" "instance-team-1-mwlp" "instance-team-1-n9g8" "instance-team-1-nvxl" "instance-team-1-q2xl" "instance-team-1-s131" "instance-team-1-v94h" "instance-team-1-zhp8")


for instance_name in ${instance_names[@]}; do
    echo $instance_name
    # Connect using SSH
    gcloud compute ssh --project=directed-pier-294505 --zone=us-west2-a $instance_name --command="cd prometeo && sudo git pull && sudo docker rmi $(docker images -q --filter "dangling=true") && sudo docker-compose up -d --build"
    # # Create a screen
    # screen
    # # Build containers
    # cd prometeo && sudo git pull && sudo docker-compose up -d --build && sudo docker exec -it prometeo_server_1 bash
    # python3 fetchers/test_all/run.py --workers 3
    echo "ending" 
done
