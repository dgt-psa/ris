# -*- coding: utf-8 -*-

###############################################################################

from flask import Flask, request, jsonify, redirect
import tensorflow as tf
from PIL import Image
from urllib2 import urlopen
from io import BytesIO
import base64
import json
import re
from ws_configuracion import CONF_API_PREFIX, CONF_MODELOS

###############################################################################

app = Flask(__name__, static_url_path='/static')

###############################################################################
# objeto específico para interpretar resultados de modelo inception (google) adaptado desde 
# https://github.com/tensorflow/models/blob/master/tutorials/image/imagenet/classify_image.py
class NodeLookup(object):

  def __init__(self,
               label_lookup_path=None,
               uid_lookup_path=None):
    modelo_tmp = [modelo for modelo in CONF_MODELOS if modelo['id'] == 1][0]
    if not label_lookup_path:
      label_lookup_path = modelo_tmp['archivo_labels_map']
    if not uid_lookup_path:
      uid_lookup_path = modelo_tmp['archivo_labels_txt']
    self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

  def load(self, label_lookup_path, uid_lookup_path):
    if not tf.gfile.Exists(uid_lookup_path):
      tf.logging.fatal('File does not exist %s', uid_lookup_path)
    if not tf.gfile.Exists(label_lookup_path):
      tf.logging.fatal('File does not exist %s', label_lookup_path)
    proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
    uid_to_human = {}
    p = re.compile(r'[n\d]*[ \S,]*')
    for line in proto_as_ascii_lines:
      parsed_items = p.findall(line)
      uid = parsed_items[0]
      human_string = parsed_items[2]
      uid_to_human[uid] = human_string
    node_id_to_uid = {}
    proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
    for line in proto_as_ascii:
      if line.startswith('  target_class:'):
        target_class = int(line.split(': ')[1])
      if line.startswith('  target_class_string:'):
        target_class_string = line.split(': ')[1]
        node_id_to_uid[target_class] = target_class_string[1:-2]
    node_id_to_name = {}
    for key, val in node_id_to_uid.items():
      if val not in uid_to_human:
        tf.logging.fatal('Failed to locate: %s', val)
      name = uid_to_human[val]
      node_id_to_name[key] = name
    return node_id_to_name

  def id_to_string(self, node_id):
    if node_id not in self.node_lookup:
      return ''
    return self.node_lookup[node_id]

###############################################################################
# rutas para flask

# devolver html demo estático para prueba de los métodos del webservice
@app.route("/", methods=['GET'])
def static_index():
	return redirect('static/index.html')

# devolver lista de modelos (se usarán campos id y nombre)
@app.route(CONF_API_PREFIX + "/modelos", methods=['GET'])
def get_modelos():
	return jsonify({'modelos': CONF_MODELOS})

# devolver lista de clases de un modelo
@app.route(CONF_API_PREFIX + "/clases/<int:modelo_id>", methods=['GET'])
def get_clases(modelo_id):
    modelo = [modelo for modelo in CONF_MODELOS if modelo['id'] == modelo_id][0]
    if modelo_id == 1:
        node_lookup = NodeLookup()
        clases = node_lookup.node_lookup.values()
    else:
        clases = [linea.rstrip() for linea in tf.gfile.GFile(modelo['archivo_labels_txt'])]
    return jsonify({'modelo':modelo_id, 'clases': clases})

# clasificar imagen de entrada (contenido recibido en base64 o url para descargar)
@app.route(CONF_API_PREFIX + "/clasificar/<int:modelo_id>", methods=['POST'])
def clasificar(modelo_id):
    try:

        modelo = [modelo for modelo in CONF_MODELOS if modelo['id'] == modelo_id][0]

        data = json.loads(request.data.decode())
        tmp_jpg_file = '/tmp/ris_tmp.jpg'
        if 'url' in data:
            url = data['url']
            tmp_url = urlopen(url)
            f = BytesIO(tmp_url.read())
            im = Image.open(f)
            if im.mode != "RGB":
                im = im.convert("RGB")
            im.save(tmp_jpg_file)

        elif 'base64' in data:
            base64_txt = data['base64']
            im = Image.open(BytesIO(base64.b64decode(base64_txt)))
            if im.mode != "RGB":
                im = im.convert("RGB")
            im.save(tmp_jpg_file)
        
        image_data = tf.gfile.FastGFile(tmp_jpg_file, 'rb').read()

        with tf.gfile.FastGFile(modelo['archivo_pb'], 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

        with tf.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name(modelo['tensor_final'])
            predictions = sess.run(softmax_tensor, \
                {'DecodeJpeg/contents:0': image_data})
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

            resultados = []
            node_lookup = {}
            if modelo_id == 1:
                node_lookup = NodeLookup()
            else:
                clases = [linea.rstrip() for linea in tf.gfile.GFile(modelo['archivo_labels_txt'])]

            for node_id in top_k:
                if modelo_id == 1:
                    clase_nombre = node_lookup.id_to_string(node_id)
                else:
                    clase_nombre = clases[node_id]
                score = predictions[0][node_id]
                estimacion = '%.5f' % score

                resultados.append({"clase": clase_nombre, "estimacion": estimacion})

        return jsonify({'modelo':modelo_id, 'resultados': resultados})

    except Exception as e:
        return jsonify({'error interno': str(type(e)) + ': ' + str(e)}), 500

###############################################################################
if __name__ == "__main__":
	app.run(debug=True)
