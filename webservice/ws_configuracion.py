# -*- coding: utf-8 -*-

###############################################################################

CONF_API_PREFIX = "/api/v7"

CONF_MODELOS = [

	{
		'id': 1,
		'nombre': u'Modelo original de google (inception)',
		'descripcion': u'inception-2015-12-05',
		'archivo_labels_txt': '../modelos/google/inception-2015-12-05/imagenet_synset_to_human_label_map.txt',
		'archivo_pb': '../modelos/google/inception-2015-12-05/classify_image_graph_def.pb',
		'tensor_final': 'softmax:0',
        'archivo_labels_map': '../modelos/google/inception-2015-12-05/imagenet_2012_challenge_label_map_proto.pbtxt' 
	},
	# {
		# 'id': 2,
		# 'nombre': u'Modelo original de google #2 (inception)',
		# 'descripcion': u'inception_v3_2016_08_28_frozen', 
		# 'archivo_labels_txt': '../modelos/google/inception_v3_2016_08_28_frozen/imagenet_slim_labels.txt',
		# 'archivo_pb': '../modelos/google/inception_v3_2016_08_28_frozen/inception_v3_2016_08_28_frozen.pb',
		# #'tensor_final': 'final_result:0'
        # 'tensor_final': 'InceptionV3/Predictions/Reshape_1'
	# },
    
	{
		'id': 11,
		'nombre': u'Modelo p/recon. de armas de fuego (dataset GDXray)',
		'descripcion': u'', 
		'archivo_labels_txt': '../modelos/gdxray/gdxr1/retrained_labels.txt',
		'archivo_pb': '../modelos/gdxray/gdxr1/retrained_graph.pb',
		'tensor_final': 'final_result:0'
	},
	{
		'id': 12,
		'nombre': u'Modelo p/recon. de armas blancas (dataset GDXray)',
		'descripcion': u'', 
		'archivo_labels_txt': '../modelos/gdxray/gdxr2/retrained_labels.txt',
		'archivo_pb': '../modelos/gdxray/gdxr2/retrained_graph.pb',
		'tensor_final': 'final_result:0'
	},
	{
		'id': 13,
		'nombre': u'Modelo p/recon. de armas de fuego + armas blancas (dataset GDXray)',
		'descripcion': u'', 
		'archivo_labels_txt': '../modelos/gdxray/gdxr3/retrained_labels.txt',
		'archivo_pb': '../modelos/gdxray/gdxr3/retrained_graph.pb',
		'tensor_final': 'final_result:0'
	},

	{
		'id': 21,
		'nombre': u'Modelo p/recon. de artefactos explosivos #1 (dataset PSA)',
		'descripcion': u'', 
		'archivo_labels_txt': '../modelos/psa/1/output_labels.txt',
		'archivo_pb': '../modelos/psa/1/output_graph.pb',
		'tensor_final': 'final_result:0'
	},
	# {
		# 'id': 22,
		# 'nombre': u'Modelo p/recon. de artefactos explosivos #2 (dataset PSA)',
		# 'descripcion': u'', 
		# 'archivo_labels_txt': '../modelos/psa/2/output_labels.txt',
		# 'archivo_pb': '../modelos/psa/2/output_graph.pb',
		# 'tensor_final': 'final_result:0'
	# },
	{
		'id': 23,
		'nombre': u'Modelo p/recon. de artefactos explosivos #2 (dataset PSA)',
		'descripcion': u'', 
		'archivo_labels_txt': '../modelos/psa/3/output_labels.txt',
		'archivo_pb': '../modelos/psa/3/output_graph.pb',
		'tensor_final': 'final_result:0'
	}
]

###############################################################################
