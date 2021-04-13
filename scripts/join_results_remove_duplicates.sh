instance_names=("instance-team-1-2j48")

for instance_name in ${instance_names[@]}; do
    echo $instance_name
    # Connect using SSH
    gcloud compute ssh --project=directed-pier-294505 --zone=us-west2-a $instance_name --command="zip -r $instance_name.zip prometeo/data/enhanced/heating*"
    gcloud compute scp --recurse --zone=us-west2-a $instance_name:$instance_name.zip $PWD/data/download
    echo "Downloaded" 
done

#zip -r $PWD/data/download/all_machines.zip $PWD/data/download/
# Delete all the zip downloaded and keep all
#rm -rf $PWD/data/download/instance*
