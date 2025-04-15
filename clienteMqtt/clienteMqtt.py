import asyncio, ssl, certifi, logging, os
import aiomqtt

# Se configura el log %(taskName)s -
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S %z')

async def msg_topico1(topics):
    while True:
        task_name = asyncio.current_task().get_name()
        message = await topico_1_queue.get()
        logging.info(" "+task_name+" - "+str(topics[0]) + ": "+ message.payload.decode("utf-8"))

async def msg_topico2(topics):
    while True:
        task_name = asyncio.current_task().get_name()
        message = await topico_2_queue.get()
        logging.info(" "+task_name +" - "+str(topics[1]) + ": "+ message.payload.decode("utf-8"))

topico_1_queue = asyncio.Queue()
topico_2_queue = asyncio.Queue()

async def distributor(client, topics):
    '''función para distribuir los mensajes a las colas correspondientes'''
    # Sacada de la documentación de aiomqtt y modificada
    try:
        async for message in client.messages:
            if message.topic.matches(topics[0]):
                topico_1_queue.put_nowait(message)
            elif message.topic.matches(topics[1]):
                topico_2_queue.put_nowait(message)
    except aiomqtt.MqttError:
        pass

async def incremet(data):
    '''modifica el valor de count cada 3 segundos'''
    while True:
        await asyncio.sleep(3)
        data["count"] += 1

async def main():
    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_context.verify_mode = ssl.CERT_REQUIRED
    tls_context.check_hostname = True
    tls_context.load_default_certs()
    
    data = {"count": 0}

    async with aiomqtt.Client(
        os.environ["SERVIDOR"],
        port=8883,
        tls_context=tls_context,
    ) as client:
        # se crea la tarea para incrementar el valor de count
        asyncio.create_task(incremet(data))
        # se crea realiza la subscripción a los tópicos
        topics = os.environ["TOPICOS"].split(',')
        for topic in topics:
            await client.subscribe(topic)
        # se crean las tareas para recibir los mensajes y distribuirlos
        asyncio.create_task(distributor(client, topics))
        asyncio.create_task(msg_topico1(topics), name="msg_topico1")
        asyncio.create_task(msg_topico2(topics), name="msg_topico2")

        while True:
            # se publica el valor de count cada 5 segundos
            await asyncio.sleep(5)
            await client.publish(os.environ["TOPICO"],data["count"])
           
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info(" Cliente MQTT detenido")