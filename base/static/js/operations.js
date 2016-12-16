/**
 * Created by ruben on 14.12.16.
 */
Vue.http.headers.common['X-CSRFToken'] = csrftoken;

var gisOperationsMixin = {
    methods: {
        bufferFeatures: function (features, extraArgs) {
            var featuresGeojson = [];
            for (var i = 0; i < features.length; i++) {
                var obj = features[i];
                featuresGeojson.push(obj.feature);
            }
            var data = {
                'geojson': turf.featureCollection(featuresGeojson),
                'meters': extraArgs.size,
                'name': extraArgs.name
            };
            return this.$http.post('/gis-operations/buffer/', data);
        }
    }
};
