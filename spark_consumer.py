
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from EventCoder import EventCoder
from actordiscovery123 import DiscoverActor
from _functools import partial
from datetime import datetime
import os

def map_articles(articleText):
    return articleText.encode('utf-8')


def code_articles(articleText, petrGlobals={}):
    coder = EventCoder(petrGlobal = petrGlobals)
    events_map = coder.encode(articleText)
    return str(events_map)

dc = DiscoverActor()


def es_object(rdd):
    for x in rdd.collect():
        obj = {}
        obj['text'] = x
        dc.discoverActor(x)



if __name__ == "__main__":

    os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars spark-streaming-kafka-0-8-assembly_2.11-2.3.0.jar pyspark-shell'

    conf = SparkConf().setAppName("Political Application")
    sc = SparkContext(conf=conf)

    coder = EventCoder(petrGlobal={})

    bMap = sc.broadcast(coder.get_PETRGlobals())
    print(bMap.__class__)

    ssc = StreamingContext(sc, 5)
    constream = KafkaUtils.createStream(ssc=ssc,
                                        zkQuorum='localhost:2181',
                                        groupId='my_group',
                                        topics={'Newsfeed':1})


    lines = constream.map(lambda x: x[1])
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    lines.pprint(1)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    events_rdd = lines.map(map_articles)
    events_rdd.foreachRDD(es_object)

    #events_rdd.pprint(1)
    events_rdd = events_rdd.map(partial(code_articles, petrGlobals = bMap.value))
    #     events_rdd.pprint(1)
    #
    #     events_rdd.foreachRDD(lambda x: x.saveAsTextFile("home/nilesh/Events"+ datetime.strftime(datetime.now(), "%Y%m%d_%I%M%S")))

    ssc.start()
    ssc.awaitTermination()
