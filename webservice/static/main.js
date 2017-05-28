///////////////////////////////////////////////////////////////////////////////

URI = 'http://localhost:8000/api/v7/';

///////////////////////////////////////////////////////////////////////////////

var app = angular.module('ris', [ 'naif.base64', 'angular-loading-bar' ])

///////////////////////////////////////////////////////////////////////////////
app.controller('MainController', [ '$scope', '$http', function($scope, $http)	{

	$scope.modeloSelected = null;
	$scope.modelos = [];
	$scope.url = '';
	$scope.imagen = {};
	$scope.imagen_thumb = '';
	
	$http({
		method: 'GET',
		url: URI + 'modelos',
		data: { }
		}).success(function (result)	{
			$scope.modelos = result.modelos;
		});

	///////////////////////////////////////////////////////////////////////////
	$scope.clases = function()	{
		$http({
			method: 'GET',
			url: URI + 'clases/' + $scope.modeloSelected,
			data: { }
			}).success(function (result)	{
				alert(JSON.stringify(result));
			});
	}
	
	///////////////////////////////////////////////////////////////////////////
	$scope.onAfterValidateImagen = function(event, fileObjs, fileList)	{
		var filename = fileObjs[0].filename;
		var filetype = fileObjs[0].filetype;
		var base64 = fileObjs[0].base64;
		$scope.imagen_thumb = 'data:' + filetype + ';base64,' + base64;
	}
		
	///////////////////////////////////////////////////////////////////////////
	$scope.clasificar = function()	{

		if (!$scope.modeloSelected)	{
			$scope.resultado = 'No se seleccionó modelo.';
			return;
		}

		var data = {};
		if ($scope.url)	{
			data = angular.toJson({ 'url': $scope.url });
		} else if ($scope.imagen.base64)	{
			data = angular.toJson({ 'base64': $scope.imagen.base64 });
		} else	{
			$scope.resultado = 'No se especificó URL o imagen.';
			return;
		}
		
		try {
			var responsePromise = $http.post(URI + 'clasificar/' + $scope.modeloSelected, data);
		} catch (err) {
			$scope.resultado = 'Se ha producido un error (1): ' + JSON.stringify(err);
		}
		responsePromise.success(function(data, status, headers, config)	{
			$scope.resultado = JSON.stringify(data);
		});
		responsePromise.error(function(data, status, headers, config)	{
			$scope.resultado = 'Se ha producido un error (2): ' + JSON.stringify(data);
		});		
	}
} ])
