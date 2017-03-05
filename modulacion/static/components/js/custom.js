var width = 800;
var height = 400;
function computeYScale (width, height, xScale) {
  var xDiff = xScale[1] - xScale[0]
  var yDiff = height * xDiff / width
  return [-yDiff / 2, yDiff / 2]
}
function drawModuladora(fun, T, A) {
    var eq = $('#eq-' + fun).val();
    console.log('Drawing '+fun+': '+eq);
    try {
        var moduladora = functionPlot({
            width: width,
            height: height,
            xDomain: [-3*T, 3*T],
            yDomain: [-A,A],
            xLabel: 'Frecuencia(Hz)',
            yLabel: 'Amplitud(V)',
            target: '#plot-' + fun,
            grid: true,
            data: [{
                fn: $('#eq-' + fun).val(),
                sampler: 'builtIn', // this will make function-plot use the evaluator of math.js
                graphType: 'polyline'
            }]
        });
        console.log('intancia moduladora '+ moduladora.id);
        //moduladora.programmaticZoom([0, 2*T], [-A, A]); //Para definir el zoom de la grafica
    } catch (err) {
        console.log(err);
        alert(err);
    }
}
function drawPortadora(fun, T, A) {
    var eq = $('#eq-' + fun).val();
    console.log('Drawing '+fun+': '+eq);
    try {
        var portadora = functionPlot({
            width: width,
            height: height,
            xDomain: [-3*T, 3*T],
            yDomain: [-A,A],
            xLabel: 'Frecuencia(Hz)',
            yLabel: 'Amplitud(V)',
            target: '#plot-' + fun,
            grid: true,
            data: [{
                fn: $('#eq-' + fun).val(),
                sampler: 'builtIn', // this will make function-plot use the evaluator of math.js
                graphType: 'polyline'
            }]
        });
        console.log('intancia portadora '+ portadora.id);
        //portadora.programmaticZoom([0, 2*T], [-A, A]); //Para definir el zoom de la grafica
    } catch (err) {
        console.log(err);
        alert(err);
    }
}
function drawModulada(fun, T, A) {
    eq = $('#eq-' + fun).val();
    console.log('Drawing '+fun+': '+eq);
    try {
        var modulada = functionPlot({
            width: width,
            height: height,
            xDomain: [-3*T, 3*T],
            yDomain: [-4,4],
            xLabel: 'Frecuencia(Hz)',
            yLabel: 'Amplitud(V)',
            target: '#plot-' + fun,
            grid: true,
            data: [{
                fn: $('#eq-modulada').val(),
                sampler: 'builtIn', // this will make function-plot use the evaluator of math.js
                graphType: 'polyline'
            }]
        });
        //modulada.programmaticZoom([0, 2*T], [-A, A]); //Para definir el zoom de la grafica
    } catch (err) {
        console.log(err);
        alert(err);
    }
}

function modulate() {
    vm = $("#vm").val();
    vmt = $("#vmt").val();
    fm = $("#fm").val();
    vc = $("#vc").val();
    vct = $("#vct").val();
    fc = $("#fc").val();
    kl = $("#kl").val();
    m = $("#m").val();
    var post_data = {
        'vm': vm,
        'vmt': vmt,
        'fm': fm,
        'vc': vc,
        'vct': vct,
        'fc': fc,
        'kl': kl,
        'm': m
    };
    $.ajax({
        url: "http://localhost:8000/",
        type: 'POST',
        data: post_data,
        dataType: 'json',
        cache: false,
        success: function(data) {
            $('#eq-moduladora').val(data.moduladora);
            $('#eq-portadora').val(data.portadora);
            //$('#eq-modulada').val(data.modulada);
            $('#vc_modulada').val(vc);
            $('#vct_modulada').val(vct);
            $('#fc_modulada').val(fc);
            $('#kl_modulada').val(kl);
            $('#vmt_modulada').val(vmt);
            $('#fm_modulada').val(fm);
            console.log(data);
            //drawModuladora('moduladora', 1/fm, vm);
            //drawPortadora('portadora', 1/fc, vc);
            drawModulada('modulada', 1/fc+1/fm, vc);
        }
    });
}

function demodulate() {
    draw('moduladora');
    draw('portadora');
    draw('modulada');
}
