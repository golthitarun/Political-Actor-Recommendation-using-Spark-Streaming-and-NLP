from kafka import KafkaConsumer, KafkaProducer
import time
producer = KafkaProducer(bootstrap_servers='localhost:9092')
count = 0
for i in range(1,11):
    with open("Data/"+str(i)+".txt", "r") as ins:
        for line in ins:
            time.sleep(2)
            count +=1
            print("Count",count)
            producer.send("Newsfeed", line)
