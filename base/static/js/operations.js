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
                featuresGeojson.push(obj.feature);
            }
            return turf.featureCollection(featuresGeojson);
        },
        deleteLayer: function (layer) {
            return this.$http.delete('/layers/' + layer.id + '/')
        },
        bufferFeatures: function (features, extraArgs) {
            var data = {
                'operation': 'buffer',
                'geojson': this.extractFeatureJson(features),
                'extra_args': extraArgs,
            };
            return this.$http.post('/gis-operations/operation/', data);
        },
        intersectFeatures: function (features, extraArgs) {
            var data = {
                'operation': 'intersect',
                'geojson': this.extractFeatureJson(features),
                'extra_args': extraArgs,
            };

        },
        mergeFeatures: function (features, extraArgs) {
            var data = {
                'operation': 'merge',
                'geojson': this.extractFeatureJson(features),
                'extra_args': extraArgs,
            };
            return this.$http.post('/gis-operations/operation/', data);
        },
        doGisOperation: function (operationName, extraArgs) {
            // Close all dialogs
            this.clearDialogs();
            this.operations.push({'name': operationName, 'extraArgs': extraArgs});
            extraArgs.exercise_slug = exerciseSlug;
            switch (operationName) {
                case 'buffer':
                    this.bufferFeatures(this.selectedFeatures, extraArgs).then(this.handleOperationResponse, this.handleError);
                    break;
                case 'intersect':
                    this.intersectFeatures(this.selectedFeatures, extraArgs).then(this.handleOperationResponse, this.handleError);
                    break;
                case 'merge':
                    this.mergeFeatures(this.selectedFeatures, extraArgs).then(this.handleOperationResponse, this.handleError);
            }
            this.resetSelectedFeatures();
        },
        handleOperationResponse: function (response) {
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
