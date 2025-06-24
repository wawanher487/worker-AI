import pika
import json
from pipeline import run_pipeline
from dotenv import load_dotenv
import os


load_dotenv()

# Konfigurasi RabbitMQ
RABBITMQ_HOST = os.getenv("RMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RMQ_USER")
RABBITMQ_PASS = os.getenv("RMQ_PASS")
RABBITMQ_PORT = int(os.getenv("RMQ_PORT", 5672))
RABBITMQ_VHOST = os.getenv("RMQ_VHOST", "/")
QUEUE_NAME = os.getenv("TO_AI_QUEUE", "to_ai_service")

def callback(ch, method, properties, body):
    print("[RECEIVED] Data dari worker 1:")
    data = json.loads(body)
    print(data)

    # Jalankan pipeline klasifikasi
    run_pipeline(data)

def start_consumer():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        virtual_host=RABBITMQ_VHOST,
        credentials=credentials,
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=False)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

    print(f"[*] Menunggu pesan dari queue: {QUEUE_NAME}")
    channel.start_consuming()
    
if __name__ == "__main__":
    start_consumer()
