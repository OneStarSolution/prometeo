sudo apt install -y unzip zip git
sudo git clone https://github.com/OneStarSolution/prometeo.git prometeo
sudo mkdir prometeo/data
sudo mkdir prometeo/data/enhanced
sudo mkdir prometeo/data/phones_urls
sudo mkdir prometeo/data/yelp_data
sudo mv secrets.env prometeo/config
sudo unzip Archive.zip -d prometeo
cd prometeo
sudo git checkout run_quick
bash scripts/run.sh
sudo docker-compose up -d --build
# screen
# sudo docker exec -it prometeo_server_1 bash
# python3 scripts/split_file.py --path valid_zipcodes.csv --chunks 20 --keep 1
# python3 fetchers/test_all/run.py --workers 2
