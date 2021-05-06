# gcloud auth login

instance_names=("instance-template-1" "instance-template-2" "instance-template-3" "instance-template-4" "instance-template-5" "instance-template-6" "instance-template-7" "instance-template-8" "instance-template-9" "instance-template-10")
count=0

for instance_name in ${instance_names[@]}; do
    # Connect using SSH
    gcloud compute ssh --project=directed-pier-294505 --zone=us-west2-a $instance_name 
    # cd prometeo && ls data/enhanced/ | grep .xlsx | wc -l && exit

done

echo $count
