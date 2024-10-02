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
mutex = threading.Semaphore(1)

def filosofo(id):
  global filosofos_estado

  while True:
    filosofos_estado[id] = "pensando"
    print("Filosofo %d pensando" % id)
    time.sleep(2)

    mutex.acquire()
    filosofos_estado[id] = "comiendo"
    print("Filosofo %d comiendo" % id)
    time.sleep(2)

    filosofos_estado[id] = "hambriento"
    print("Filosofo %d ha terminado de comer y está hambriento" % id)
    mutex.release()
    time.sleep(2)


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
