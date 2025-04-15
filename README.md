# Ejercicio docker

## Consigna
### Crear una imagen con una aplicación asíncronica en python que se comunique con un broker mqtt utilizando comunicación cifrada (mqtts).

- recibe por variable de entorno la dirección del servidor (broker)
- recibe por variables de entorno dos tópicos a los cuales suscribirse.
- los mensajes de los distintos tópicos se atenderán en sus correspondientes corrutinas. (logg info)
- recibe por variables de entorno un tópico en el cuál publica cada 5 segundos el estado de un contador.
- el contador se incrementa cada 3 segundos en una corrutina (task) diferente.
- no utilizar variables globales.
- utilizar aiomqtt.
- crear un solo objeto client.
- en el formato del logging se deberá incluir el nombre de la corrutina (task) utilizando la etiqueta correspondiente del modulo logging.
- capturar la excepción al detener con ctrl-c.
- se crea el contenedor con docker compose

## Descripción

Se implementa un cliente MQTT asíncrono utilizando la biblioteca aiomqtt:
- Se configura el formato de los logs para registrar eventos con nivel de información (INFO). 
- Se crean dos funciones para manejar los mensajes provenientes de las subscripciones recibidas por la variable de entorno TOPICOS: msg_topico1 y msg_topico2. 
- Estos mensajes son adminstrados por la función "distributor" que escucha los mensajes entrantes del cliente MQTT y los distribuye a las colas correspondientes según el tema (topic).
- Para incrementar el contador, se crea una tarea "incremet", la cual incrementa el valor en un diccionario (data["count"]) cada 3 segundos.
- Se publica el valor del contador (data["count"]) en el topico proveniente de la variable de entorno TOPICO cada 5 segundos.
El programa se ejecuta con asyncio.run(main()) y maneja la interrupción del teclado (KeyboardInterrupt) para detener el cliente MQTT.

