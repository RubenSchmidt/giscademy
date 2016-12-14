/**
 * Created by ruben on 14.12.16.
 */
Vue.http.headers.common['X-CSRFToken'] = csrftoken;

var gisOperationsMixin = {
    methods: {
        bufferFeatures: function (features, bufferMeters) {
            var data = {
                'geojson': turf.featureCollection(features),
                'meters': bufferMeters
            };
            return this.$http.post('/gis-operations/buffer/', data);
        }
    }
};
