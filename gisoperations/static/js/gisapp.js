/**
 * Created by rubenschmidt on 26.12.2016.
 */
var GISApp = new Vue({
    el: '#gisapp',
    // Custom delimiters so we do not interfere with django natives.
    delimiters: ["[[", "]]"],
    // Add the gisoperationsmixin so we can use the operations api.
    mixins: [gisOperationsMixin],
    data: {
        defaultStyle: {
            "color": "#4b7eff",
            "weight": 5,
            "opacity": 1,
            "fillOpacity": 0.7
        },
        newLayerName: '',
        loadingLayers: false,
        file: null,
        bufferSize: null,
        layers: [],
        selectedFeatures: [],
        lineStringLayer: null,
        polygonLayer: null,
        geoJson: null,
        map: null,
        dialogs: {
            'buffer': false,
            'intersect': false,
            'completed': false,
            'mergeSelected': false,
            'union': false,
            'difference': false,
            'upload': false,
            'error': false
        },
        operations: []

    },
    mounted: function () {
        // When the app is ready. Add the map.
        this.map = L.map('map').setView([0, 0], 2);

        // Add OSM tilelayer as basemap.
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.map);

        this.map.on('click', function (e) {
            GISApp.resetSelectedFeatures();
        });
    },
    computed: {
        selectedLayers: function () {
            var layers = [];
            for (var i = 0; i < this.layers.length; i++) {
                var obj = this.layers[i];
                if (obj.checked) layers.push(obj);
            }
            return layers
        }
    },
    methods: {
        setCenter: function (lat, lng, zoom) {
            this.map.setView([lat, lng], zoom)
        },
        addData: function (layers) {
            for (var i = 0; i < layers.length; i++) {
                var layer = layers[i];

                var style = {
                    "color": this.getRandomColor(),
                    "weight": 5,
                    "opacity": 1,
                    "fillOpacity": 0.7
                };
                var geoJson = L.geoJSON(layer.points.features, {
                    style: style,
                    onEachFeature: this.onEachFeature
                })
                geoJson.addData(layer.polygons.features);
                geoJson.addData(layer.linestrings.features);
                layer.leafletLayer = geoJson;
                layer.checked = false;
                layer.leafletLayer.addTo(this.map);
            }
            this.layers = this.layers.concat(layers);
        },
        getRandomColor: function () {
            var letters = '0123456789ABCDEF'.split('');
            var color = '#';
            for (var i = 0; i < 6; i++) {
                color += letters[Math.round(Math.random() * 15)];
            }
            return color;
        },
        onEachFeature: function (feature, layer) {

            var props = feature.properties;
            if (props) {
                var body = "<table class='table is-bordered'>";
                for (var key in props) {
                    if (props.hasOwnProperty(key)) {
                        body +=
                            ('<tr><td>' + key + '</td><td>' + props[key] + '</td></tr>');
                    }
                }
                body += "</table>";
                layer.bindPopup(body);
            }
            //bind click and mouse events.
            layer.on({
                click: this.whenClicked,
                mouseover: this.onMouseOver,
                mouseout: this.onMouseOut
            });
        },
        whenClicked: function (e) {
            // Stop propagation so only the feature click is fired and not the map click.
            L.DomEvent.stopPropagation(e);
            e.target.openPopup();
            this.addOrRemoveFeatureFromList(e.target);
        },

        onMouseOver: function (e) {
            this.highlightFeature(e.target);
        },
        onMouseOut: function (e) {
            e.target.closePopup();
            this.resetHighlight(e.target);
        },
        highlightFeature: function (layer) {
            if (layer._icon) {
                // Points cant be resized stock
                // TODO implement
            } else {
                layer.setStyle({
                    weight: 5,
                    color: '#23c6ff',
                    dashArray: '',
                    fillOpacity: 0.7
                });
            }
        },
        resetHighlight: function (target) {
            for (var i = 0; i < this.layers.length; i++) {
                var layer = this.layers[i];
                if (this.selectedFeatures.indexOf(target) === -1) {
                    layer.leafletLayer.resetStyle(target);
                }
            }
        },
        resetSelectedFeatures: function () {
            // When the map is clicked we want to reset the selected features
            var resetFeatures = GISApp.selectedFeatures.slice();
            GISApp.selectedFeatures = [];

            for (var i = 0; i < resetFeatures.length; i++) {
                var feature = resetFeatures[i];
                GISApp.resetHighlight(feature);
            }

        },
        resetLayerList: function () {
            for (var i = 0; i < this.layers.length; i++) {
                var layer = this.layers[i];
                layer.checked = false;
                // Vue.set
                Vue.set(this.layers, i, layer);
            }
        },
        addOrRemoveFeatureFromList: function (layer) {
            var index = this.selectedFeatures.indexOf(layer);
            if (index === -1) {
                this.selectedFeatures.push(layer);
                this.highlightFeature(layer);

            } else {
                this.selectedFeatures.splice(index, 1);
            }
        },
        toggleDialog: function (dialogName) {
            this.dialogs[dialogName] = !this.dialogs[dialogName];
        },
        clearDialogs: function () {
            for (var property in this.dialogs) {
                if (this.dialogs.hasOwnProperty(property)) {
                    this.dialogs[property] = false;
                }
            }
        },
        deleteSelectedLayers: function () {
            for (var i = 0; i < this.layers.length; i++) {
                var layer = this.layers[i];
                if (!layer.checked || !layer.user) continue;
                this.map.removeLayer(layer.leafletLayer);

                // Remove the layer from the layers list
                this.layers.splice(i, 1);
                this.deleteLayer(layer);
            }
        },
        bringSelectedLayersToFront: function () {
            for (var i = 0; i < this.layers.length; i++) {
                var layer = this.layers[i];
                if (!layer.checked) continue;
                var lf = layer.leafletLayer;
                lf.bringToFront();
            }
        },
        setFile: function (e) {
            var file = e.target.files[0];
            this.file = file;
        },
        addLayerFromFile: function () {
            if (!this.file) return;

            var fileReader = new FileReader();
            if (this.file.name.split('.')[1] == 'zip') {
                fileReader.onload = function () {
                    shp(this.result).then(function (geojson) {
                        console.log(geojson);
                        GISApp.toggleDialog('upload');
                        GISApp.importJson(geojson, GISApp.newLayerName);
                    });
                };
                fileReader.readAsArrayBuffer(this.file);
            }
            else if (this.file.name.split('.')[1] == 'geojson') {
                fileReader.onload = function () {
                    var geojson = JSON.parse(this.result);
                    console.log(geojson);
                    GISApp.toggleDialog('upload');
                    GISApp.importJson(geojson, GISApp.newLayerName);
                };
                fileReader.readAsText(this.file);
            }
        },
        handleError: function () {

        }
    }
});
