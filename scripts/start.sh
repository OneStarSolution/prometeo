screen
cd prometeo
cd prometeo && sudo git pull && sudo docker-compose up -d --build && sudo docker exec -it prometeo_server_1 bash scripts/run_crawl.sh