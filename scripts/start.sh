screen -S crawl -q
screen -S crawl -X cd prometeo
screen -S crawl -X sudo git pull && sudo docker-compose up -d --build && sudo docker exec -it prometeo_server_1 bash scripts/run_crawl.sh