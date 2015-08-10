from kazoo.client import KazooClient
from samsa.cluster import Cluster
zookeeper = KazooClient()
zookeeper.start()
cluster = Cluster(zookeeper)
topic = cluster.topics['topicname']
topic.publish('msg')


from kazoo.client import KazooClient
from samsa.cluster import Cluster
zookeeper = KazooClient()
zookeeper.start()
cluster = Cluster(zookeeper)
topic = cluster.topics['topicname']
consumer = topic.subscribe('groupname')
for msg in consumer:
    print msg




# consumer 必需在 producer 向 kafka 的 topic 里面提交数据后才能连接，否则会出错。
# 在 Kafka 中一个 consumer 需要指定 groupname ， groue 中保存着 offset 等信息，新开启一个 group 会从 offset 0 的位置重新开始获取日志。
# kafka 的配置参数中有个 partition ，默认是 1 ，这个会对数据进行分区，如果多个 consumer 想连接同个 group 就必需要增加 partition , partition 只能大于 consumer 的数量，否则多出来的 consumer 将无法获取到数据。