bin/plugin install mobz/elasticsearch-head
bin/plugin install lmenezes/elasticsearch-kopf
bin/plugin install file:/usr/share/elasticsearch/data/license-2.0.0.zip 
bin/plugin install file:/usr/share/elasticsearch/data/marvel-agent-2.0.0.zip 
root@6230495b6aa5:/usr/share/elasticsearch/plugins# ls
head  kopf  license  marvel-agent
kibana plugin --install marvel --url file:///var/www/marvel-2.0.0.tar.gz 
kibana plugin --install elastic/sense
