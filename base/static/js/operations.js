/**
 * Created by ruben on 14.12.16.
 */
Vue.http.headers.common['X-CSRFToken'] = csrftoken;

var gisOperationsMixin = {
    methods: {
        bufferFeatures: function (features, extraArgs) {
            var data = {
                'geojson': turf.featureCollection(features),
                'meters': extraArgs.size,
                'name': extraArgs.name
            };
            return this.$http.post('/gis-operations/buffer/', data);
        }
    }
};
