sudo docker exec -it prometeo_server_1 bash python3 scripts/split_file.py --path valid_zipcodes.csv --chunks 20 --keep $counter