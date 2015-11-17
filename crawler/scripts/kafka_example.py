from kazoo.client import KazooClient
from samsa.cluster import Cluster


# consumer 必需在 producer 向 kafka 的 topic 里面提交数据后才能连接，否则会出错。
# 在 Kafka 中一个 consumer 需要指定 groupname ， groue 中保存着 offset 等信息，新开启一个 group 会从 offset 0 的位置重新开始获取日志。
# kafka 的配置参数中有个 partition ，默认是 1 ，这个会对数据进行分区，如果多个 consumer 想连接同个 group 就必需要增加 partition , partition 只能大于 consumer 的数量，否则多出来的 consumer 将无法获取到数据。
def producer():
    zookeeper = KazooClient()
    zookeeper.start()
    cluster = Cluster(zookeeper)
    topic = cluster.topics['topicname']
    topic.publish('msg')


def consumer():
    zookeeper = KazooClient()
    zookeeper.start()
    cluster = Cluster(zookeeper)
    topic = cluster.topics['topicname']
    for msg in topic.subscribe('groupname'):
        print msg


def producer1():
    from pykafka import KafkaClient
    client = KafkaClient(hosts="192.168.1.1:9092, 192.168.1.2:9092")  # 可接受多个Client这是重点
    client.topics  # 查看所有topic
    topic = client.topics['my.test']  # 选择一个topic
    producer = topic.get_producer()
    producer.produce(['test message ' + str(i ** 2) for i in range(4)])  # 加了个str官方的例子py2.7跑不过


def consumer1():
    # 生产者直接连接kafaka服务器列表，消费者才用zookeeper。
    from pykafka import KafkaClient
    client = KafkaClient(hosts="192.168.1.1:9092, 192.168.1.2:9092")  # 可接受多个Client这是重点
    client.topics  # 查看所有topic
    topic = client.topics['my.test']  # 选择一个topic
    balanced_consumer = topic.get_balanced_consumer(
        consumer_group='testgroup',
        auto_commit_enable=True,  # 设置为Flase的时候不需要添加 consumer_group
        zookeeper_connect='myZkClusterNode1.com:2181,myZkClusterNode2.com:2181/myZkChroot'  # 这里就是连接多个zk
    )
