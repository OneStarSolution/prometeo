instance_names=("instance-team-1-2j48" "instance-team-1-3ph2" "instance-team-1-95x5" "instance-team-1-ch6w" "instance-team-1-fxfl" "instance-team-1-g03g" "instance-team-1-hb8h" "instance-team-1-j0k2" "instance-team-1-jkm2" "instance-team-1-kzq9" "instance-team-1-m42s" "instance-team-1-m9mp" "instance-team-1-mk32" "instance-team-1-mwlp" "instance-team-1-n9g8" "instance-team-1-nvxl" "instance-team-1-q2xl" "instance-team-1-s131" "instance-team-1-v94h" "instance-team-1-zhp8")

for instance_name in ${instance_names[@]}; do
    echo $instance_name
    # Connect using SSH
    gcloud beta compute ssh $instance_name --project=directed-pier-294505 --zone=us-west2-a --command="curl -sSO https://dl.google.com/cloudagents/add-monitoring-agent-repo.sh && sudo bash add-monitoring-agent-repo.sh && sudo apt-get update -y && sudo apt-get install -y stackdriver-agent && sudo service stackdriver-agent start"
    echo "ending" 
done
