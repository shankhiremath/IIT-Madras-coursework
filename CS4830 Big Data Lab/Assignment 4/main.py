def publish(data, context):

    from google.cloud import pubsub_v1
    
    project_id = "big-data-lab-345012"
    topic_id = "pubsub-lab6"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    pub_data = data['name']
    pub_data = pub_data.encode("utf-8")
    future = publisher.publish(topic_path, pub_data)
    print(future.result())
    print("Published ", pub_data," to ", topic_path)