/**
 * Created by ruben on 09.01.17.
 */
var vue = new Vue({
    el: '#side-menu',
    delimiters: ["[[", "]]"],
    data: {
        hasCompletedExercise: false,
        currentInstruction: null,
        instructions: [],
        dialogs: {
            'completed': false,
        }
    },
    mounted: function () {
        this.fetchData();
    },
    methods: {
        fetchData: function () {
            this.resetInstructions();
            // Fetch the predefined data for the current exercise.
            GISApp.loadingLayers = true;
            this.$http.get('/layers/' + exerciseSlug + '/').then(this.handleResponse, this.handleError)
        },
        resetInstructions: function () {
            this.$http.get('/courses/' + exerciseSlug + '/instructions/').then(function (response) {
                this.instructions = response.body;
                for (var i = 0; i < this.instructions.length; i++) {
                    var instruction = this.instructions[i];
                    if (!instruction.completed) {
                        this.currentInstruction = instruction;
                        break;
                    }
                }
            }, function () {

            });
        },
        handleError: function () {
            GISApp.loadingLayers = false;
            GISApp.dialogs.error = true;
        },
        handleResponse: function (response) {
            var layers = response.body.layers;
            layers = layers.concat(response.body.user_layers);
            GISApp.addData(layers);
            GISApp.loadingLayers = false;
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
        checkLastInstruction: function () {
            var last = GISApp.operations[GISApp.operations.length - 1];
            if (!last) {
                return;
            }
            var correctOperation = this.currentInstruction.completionOperation === last.name;
            var correctArgs = true;
            var extraArgs = last.extraArgs;
            // Check that the extra args contains all the required ones.
            for (var property in this.currentInstruction.completionArgs) {
                if (!extraArgs.hasOwnProperty(property)) {
                    correctArgs = false;
                    break;
                }
                if (extraArgs[property] != this.currentInstruction.completionArgs[property]) {
                    correctArgs = false;
                    break;
                }
            }
            if (correctOperation && correctArgs) {
                // Complete step.
                var index = this.instructions.indexOf(this.currentInstruction);
                this.instructions[index].completed = true;
                var data = {'instruction_id': this.currentInstruction.id};
                this.$http.post('/courses/' + exerciseSlug + '/instructions/complete-instruction/', data).then(function (response) {
                    this.resetInstructions();
                    this.hasCompletedExercise = response.body.completed_exercise;
                    if (this.hasCompletedExercise) {
                        GISApp.toggleDialog('completed');
                    }
                }, function () {

                })
            }
        },
    }
});