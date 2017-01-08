/**
 * Created by ruben on 14.12.16.
 */
Vue.http.headers.common['X-CSRFToken'] = csrftoken;

var gisOperationsMixin = {
    methods: {
        extractFeatureJson: function (features) {
            // Return a featurecollection of the features.
            var featuresGeojson = [];
            for (var i = 0; i < features.length; i++) {
                var obj = features[i];
                if (obj.feature) {
                    featuresGeojson.push(obj.feature);
                }else {
                    featuresGeojson.push(obj);
                }
            }
            return turf.featureCollection(featuresGeojson);
        },
        deleteLayer: function (layer) {
            return this.$http.delete('/layers/' + layer.id + '/')
        },
        importJson: function (geojson, name) {
            // Close all dialogs
            this.clearDialogs();

            var extraArgs = {
                'layer_name': name
            };
            var data = {
                'operation': 'import',
                'geojson': geojson,
                'extra_args': extraArgs
            };
            this.$http.post('/gis-operations/operation/', data)
                .then(this.handleOperationResponse, this.handleError);
        },
        doGisOperation: function (operationName, extraArgs) {
            // Close all dialogs
            this.clearDialogs();
            // Save the operation
            this.operations.push({'name': operationName, 'extraArgs': extraArgs});

            if (typeof exerciseSlug !== 'undefined') {
                // Add the exercise name if it exists
                extraArgs.exercise_slug = exerciseSlug;
            }

            // Add all the features from both selected from map and the slected layers.
            var features = [];
            features = features.concat(this.selectedFeatures);
            for (var i = 0; i < this.layers.length; i++) {
                var layer = this.layers[i];
                if (!layer.checked) continue;
                features = features.concat(layer.leafletLayer.toGeoJSON().features);
            }

            var data = {
                'operation': operationName,
                'geojson': this.extractFeatureJson(features),
                'extra_args': extraArgs,
            };

            this.$http.post('/gis-operations/operation/', data)
                .then(this.handleOperationResponse, this.handleError);

            this.resetSelectedFeatures();
        },
        handleOperationResponse: function (response) {

            this.newLayerName = '';

            var layer = response.body;
            // Create the leaflet layer.
            var geojson = L.geoJSON([],{onEachFeature: this.onEachFeature});
            // Add all the data from the server
            geojson.addData(layer.points.features);
            geojson.addData(layer.linestrings.features);
            geojson.addData(layer.polygons.features);
            geojson.addTo(this.map);
            // Save reference to leafletlayer
            layer.leafletLayer = geojson;
            this.layers.push(layer);
            // Zoom the map to the created layer.
            this.map.fitBounds(geojson.getBounds());
        }
    }
};
