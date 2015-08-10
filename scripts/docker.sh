#Docker启动容器命令

docker run --name crawler -p 80:80 -p 8080:8080 -p 9200:9200 -p 8088:8088 -v /opt:/opt -t -i crawler/scrapy /bin/bash

docker run -t -i crawler:zookeeper /usr/bin/supervisord -n



