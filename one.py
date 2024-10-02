import threading
import time
import random
from flask import Flask, Response
from flask_cors import CORS
import json

app = Flask(__name__)

CORS(app)

NUM_FILOSOFOS = 5
ESTADOS = ["pensando", "comiendo", "hambriento"]
filosofos_estado = ["pensando"] * NUM_FILOSOFOS
comedor = threading.Semaphore(1)  # Semáforo para permitir que solo un filósofo coma a la vez
mutex = threading.Semaphore(1)

def filosofo(id):
  global filosofos_estado

  while True:
    # Pensando
    filosofos_estado[id] = "pensando"
    time.sleep(2)

    # Intentando comer
    mutex.acquire()  # Proteger acceso a estados
    filosofos_estado[id] = "hambriento"
    mutex.release()

    # Intentar comer
    comedor.acquire()  # Esperar a que el comedor esté disponible

    # Comer
    mutex.acquire()  # Proteger acceso a estados
    filosofos_estado[id] = "comiendo"
    mutex.release()

    time.sleep(2)

    # Estado después de comer
    mutex.acquire()  # Proteger acceso a estados
    filosofos_estado[id] = "pensando"
    mutex.release()

    comedor.release()  # Liberar el comedor para el siguiente filósofo

def iniciar_simulacion():
  for i in range(NUM_FILOSOFOS):
    threading.Thread(target=filosofo, args=(i,)).start()


@app.route('/simulation')
def inefficient_solution():
  def generar_eventos():
    while True:
      estados = json.dumps(filosofos_estado)
      ## mandar el arreglo
      yield f"data: {estados}\n\n"
      time.sleep(1)

  return Response(generar_eventos(), mimetype='text/event-stream')

if __name__ == '__main__':
  threading.Thread(target=iniciar_simulacion).start()
  app.run(debug=True)
