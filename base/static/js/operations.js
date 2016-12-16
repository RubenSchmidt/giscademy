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
            return this.$http.post('/gis-operations/operation/', data);
        }
    }
};
