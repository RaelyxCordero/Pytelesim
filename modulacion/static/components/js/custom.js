function draw(fun) {
    try {
        var func = functionPlot({
            target: '#plot-' + fun,
            grid: true,
            data: [{
                fn: $('#eq-' + fun).val(),
                sampler: 'builtIn', // this will make function-plot use the evaluator of math.js
                graphType: 'polyline'
            }]
        });
        func.programmaticZoom([0, 1], [-10, 10]); //Para definir el zoom de la grafica
    } catch (err) {
        console.log(err);
        alert(err);
    }
}

function modulate() {
    $.ajax({
        accepts: {
            mycustomtype: 'application/x-some-custom-type'
        },

        // Instructions for how to deserialize a `mycustomtype`
        converters: {
            'text mycustomtype': function(result) {
                // Do Stuff
                return newresult;
            }
        },

        // Expect a `mycustomtype` back from server
        dataType: 'mycustomtype'
    });




    draw('moduladora');
    draw('portadora');
    draw('modulada');

}

function demodulate() {
    draw('moduladora');
    draw('portadora');
    draw('modulada');
}
