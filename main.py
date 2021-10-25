import cv2
import os
import requests
import time
import cognitive_face as CF
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

from threading import Thread

llaveSuscripcionFaceApiAzure = ''
urlSuscripcionFaceApiAzure = '/face/v1.0/'
CF.BaseUrl.set(urlSuscripcionFaceApiAzure)
CF.Key.set(llaveSuscripcionFaceApiAzure)

llaveSuscripcionFaceApiAzure2 = ''
urlSuscripcionFaceApiAzure2 = '/face/v1.0/'
CF.BaseUrl.set(urlSuscripcionFaceApiAzure2)
CF.Key.set(llaveSuscripcionFaceApiAzure2)

ubicacionArchivoEncontrado=''

def mostrarFotogramaCuadradoCara(imagen, analisisImagen):
    global ubicacionArchivoEncontrado
    imagen = cv2.imread(imagen)
    imagenMostrar = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    imagenTemporal = imagenMostrar.copy()

    caras = []
    for cara in analisisImagen:
        fotogramaCara = cara['faceRectangle']
        caras.append(fotogramaCara)
        arriba = fotogramaCara['top']
        izquierda = fotogramaCara['left']
        ancho = fotogramaCara['width']
        alto = fotogramaCara['height']
        print(arriba, izquierda, ancho, alto)
        parte1 = (izquierda, arriba)
        parte2 = (izquierda + ancho, arriba + alto)
        color = (23, 200, 54)
        espesor = 10
        cv2.rectangle(imagenTemporal, parte1, parte2, color, espesor)
    arreglarColor = cv2.cvtColor(imagenTemporal, cv2.COLOR_BGR2RGB)
    cv2.imwrite('./fotogramaCara/' + ubicacionArchivoEncontrado, arreglarColor)

agregarCaras= []

def crearEstadisticas():
    global agregarCaras
    listaDatos=[]
    anger = 0
    contempt = 0
    disgust = 0
    fear = 0
    happiness = 0
    neutral = 0
    sadness = 0
    surprise =0
    for i in agregarCaras:
        faceAttributes = i['faceAttributes']
        emotions = faceAttributes['emotion']

        if emotions['anger']>=0.5:
            anger += 1
        elif emotions['contempt'] >=0.5:
            contempt += 1
        elif emotions['disgust'] >=0.5:
                disgust += 1
        elif emotions['fear'] >=0.5:
            fear += 1
        elif emotions['happiness'] >=0.5:
            happiness += 1
        elif emotions['sadness'] >=0.5:
            sadness += 1
        elif emotions['surprise'] >=0.5:
            surprise += 1
        else:
            neutral += 1

    listaDatos.append(anger)
    listaDatos.append(contempt)
    listaDatos.append(disgust)
    listaDatos.append(fear)
    listaDatos.append(happiness)
    listaDatos.append(neutral)
    listaDatos.append(sadness)
    listaDatos.append(surprise)
    return listaDatos

def func(pct, allvals):
    absolute = int(round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n({:d} Persona)".format(pct, absolute)

def imprimirEstadisticas():
        global agregarCaras
        fig, ax = plt.subplots(figsize=(7, 5), subplot_kw=dict(aspect="equal"))

        data = crearEstadisticas()
        emocionesBuscadas = ["anger","contempt","disgust","fear","hapiness","neutral","sadness","surprise"]

        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                          textprops=dict(color="w"))

        ax.legend(wedges, emocionesBuscadas,
                  title="Emociones",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=7, weight="bold")

        ax.set_title("Emociones detectadas en forma general")

        plt.savefig('./fotogramaCara/EstadisticasEmociones.png')


def emociones(imagen):
  global agregarCaras
  imagenObtenida = imagen
  imagenDatos = open(imagenObtenida, "rb").read()
  encabezados = {'Ocp-Apim-Subscription-Key': llaveSuscripcionFaceApiAzure,
  'Content-Type': 'application/octet-stream'}
  parametros = {
      'returnFaceId': 'true',
      'returnFaceLandmarks': 'false',
      'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
  }
  respuesta = requests.post(
      urlSuscripcionFaceApiAzure + "detect/", headers=encabezados, params=parametros, data=imagenDatos)
  analisis = respuesta.json()
  agregarCaras.extend(analisis)
  return analisis

def emociones2(imagen):
  global agregarCaras
  imagenObtenida = imagen
  imagenDatos = open(imagenObtenida, "rb").read()
  encabezados = {'Ocp-Apim-Subscription-Key': llaveSuscripcionFaceApiAzure2,
  'Content-Type': 'application/octet-stream'}
  parametros = {
      'returnFaceId': 'true',
      'returnFaceLandmarks': 'false',
      'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
  }
  respuesta = requests.post(
      urlSuscripcionFaceApiAzure2 + "detect/", headers=encabezados, params=parametros, data=imagenDatos)
  analisis = respuesta.json()
  agregarCaras.extend(analisis)
  return analisis


contadorRostro=0
contadorSegundoRostro=0

def comprobacionRostroFotograma(imagenFotograma):
    global contadorRostro
    global contadorSegundoRostro

    ubicacionImagen = './fotogramaCara/temp/'+ imagenFotograma
    print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print("Rastreando el fotograma: "+ imagenFotograma)

    if(contadorSegundoRostro==20):
        contadorRostro=0
        print("DESCANSANDO LAS SUSCRIPTION KEY (30 SEGUNDOS).")
        time.sleep(30)
        print("")

    if (contadorRostro==20):
        analisis = emociones2(ubicacionImagen)
        print("")
        if analisis == []:
            print("No se detectan personas en la imagen.")
            print("")
        else:
            print("Se encontro:", len(analisis), "Persona(s):")
            print(('{}\n' * len(analisis)).format(*analisis))
        mostrarFotogramaCuadradoCara(ubicacionImagen, analisis)

        print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
              "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
              "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
              "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
              "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
              "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
              "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
              "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
              "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
              "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
              "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
              "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
              "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        print("")
        contadorSegundoRostro+=1
        os.remove('./fotogramaCara/temp/' + imagenFotograma)
        return True

    analisis = emociones(ubicacionImagen)
    print("")
    if analisis == []:
        print("No se detectan personas en la imagen.")
        print("")
    else:
        print("Se encontro:", len(analisis), "Persona(s):")
        print(('{}\n'*len(analisis)).format(*analisis))
    mostrarFotogramaCuadradoCara(ubicacionImagen, analisis)

    print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
            "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print("")
    contadorRostro+=1
    contadorSegundoRostro=0
    os.remove('./fotogramaCara/temp/'+ imagenFotograma)
    return True


i = 0
j = 500

def extraerFotogramasVideo(video):
    global i
    global j
    video= cv2.VideoCapture(video)

    while(video.isOpened()):
        ret, frame = video.read()

        if ret == False:
            break

        if i == j:
          cv2.imwrite('./fotograma/'+ 'fotograma'+str(i)+'.jpg',frame)
          cv2.imwrite('./fotogramaCara/temp/'+ 'fotograma'+str(i)+'.jpg',frame)
          j +=500
          print("Fotograma realizado exitosamente: "+'fotograma'+str(i)+'.jpg')
        i+=1

    video.release()

def verificarCarpetas():
    if not os.path.isdir('fotograma'):
        os.mkdir('fotograma')

    if not os.path.isdir('fotogramaCara'):
        os.mkdir('fotogramaCara')

    if not os.path.isdir('video'):
        os.mkdir('video')

    if not os.path.isdir('fotogramaCara/temp'):
        os.mkdir('fotogramaCara/temp')

    carpetaFotograma1 = './fotograma/'
    for carpeta in os.listdir(carpetaFotograma1):
        ubicacionCarpeta = os.path.join(carpetaFotograma1, carpeta)
        try:
            if os.path.isfile(ubicacionCarpeta):
                os.unlink(ubicacionCarpeta)
        except Exception as e:
            print(e)

    carpetaFotogramaCara1 = './fotogramaCara/'
    for carpeta in os.listdir(carpetaFotogramaCara1):
        ubicacionCarpeta = os.path.join(carpetaFotogramaCara1, carpeta)
        try:
            if os.path.isfile(ubicacionCarpeta):
                os.unlink(ubicacionCarpeta)
        except Exception as e:
            print(e)


    carpetaFotogramaCaraTemp1 = './fotogramaCara/temp/'
    for carpeta in os.listdir(carpetaFotogramaCaraTemp1):
        ubicacionCarpeta = os.path.join(carpetaFotogramaCaraTemp1, carpeta)
        try:
            if os.path.isfile(ubicacionCarpeta):
                os.unlink(ubicacionCarpeta)
        except Exception as e:
            print(e)

verificarTotal=0

class revisarVideoFotogramas(Thread):
    def run(self):
        global verificarTotal
        contarTiempo = time.time()
        for file in os.listdir("./video/"):
            if file.endswith(".mp4"):
                path=os.path.join("./video/", file)
                print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
                print("SE HA DETECTADO EL VIDEO:", file)
                print("")
                extraerFotogramasVideo(path)
                print("")
                print("SE HAN EXTRAIDO LOS FOTOGRAMAS DEL VIDEO:", file)
                print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
                      "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
                print("")

        tiempoFinal = time.time() - contarTiempo
        print("Duracion total en segundos de la obtencion de los fotogramas:", round(tiempoFinal, 1))
        print("")
        verificarTotal=1

finalizarMultiproceso=0

class revisarFotogramasCaras(Thread):
    def run(self):
        global verificarTotal
        global ubicacionArchivoEncontrado
        global finalizarMultiproceso
        contarTiempo = time.time()
        path, dirs, files = next(os.walk("./fotograma/"))
        contadorArchivos = len(files)

        if (contadorArchivos==0):
            time.sleep(3)
            finalizarMultiproceso = 1

        while verificarTotal==0:
            for archivo in os.listdir('./fotogramaCara/temp/'):
                if archivo.endswith(".jpg"):
                    ubicacionArchivoEncontrado=os.path.join(archivo)
                    comprobacionRostroFotograma(ubicacionArchivoEncontrado)

        if verificarTotal == 1:
            for archivo in os.listdir('./fotogramaCara/temp/'):
                if archivo.endswith(".jpg"):
                    ubicacionArchivoEncontrado = os.path.join(archivo)
                    comprobacionRostroFotograma(ubicacionArchivoEncontrado)

        tiempoFinal = time.time() - contarTiempo
        print("Duracion total en segundos de la obtencion de los resultados de caras:", round(tiempoFinal, 1))
        os.rmdir('./fotogramaCara/temp/')

        if finalizarMultiproceso == 1:
            tiempoFinalTiempoMultiproceso = time.time() - contarTiempoMultiproceso
            convertirAMinutosMultiproceso = tiempoFinalTiempoMultiproceso // 60
            convertirASegundosMultiproceso = tiempoFinalTiempoMultiproceso % 60
            imprimirEstadisticas()
            print("")
            print("Duracion total del programa en segundos con multiproceso:", round(tiempoFinalTiempoMultiproceso, 1))
            print("Su equivalente a minutos con segundos (min : seg):", int(convertirAMinutosMultiproceso), ":",
                  int(convertirASegundosMultiproceso))

contarTiempoMultiproceso=None

def desicion():
    global contarTiempoMultiproceso
    escoger = input("Ingresa '1' si deseas ejecutar el programa en forma secuencial o ingresa '2' para ejecutarlo con multiproceso\n")
    escoger=int(escoger)

    if escoger==1:
        contarTiempoSecuencial = time.time()
        revisarVideoFotogramas().run()
        revisarFotogramasCaras().run()
        tiempoFinalTiempoSecuencial = time.time() - contarTiempoSecuencial
        convertirAMinutosSecuencial=tiempoFinalTiempoSecuencial // 60
        convertirASegundosSecuencial=tiempoFinalTiempoSecuencial % 60
        imprimirEstadisticas()
        print("")
        print("Duracion total del programa en segundos de forma secuencial:", round(tiempoFinalTiempoSecuencial, 1))
        print("Su equivalente a minutos con segundos (min : seg):", int(convertirAMinutosSecuencial),":",int(convertirASegundosSecuencial))
        return True

    if escoger==2:
        contarTiempoMultiproceso = time.time()
        revisarVideoFotogramas().start()
        revisarFotogramasCaras().start()

    if escoger !=1 and escoger!=2:
        print("")
        print("Solo son validos los numeros 1 y 2.")
        print("")
        desicion()

verificarCarpetas()
desicion()


