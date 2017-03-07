var width = 800;
var height = 400;

var modx = "";

$(document).ready(function() {
    modalidad('FM');
    
});

function modalidad(mod) {
    if (mod == 'FM') {
        $('#modalidad').html('FM');
        modx = 'FM';
    } else {
        $('#modalidad').html('PM');
        modx = 'PM';
    }
}

function drawModuladora(fun, T, A) {
    try {
        var moduladora = functionPlot({
            width: width,
            height: height,
            xDomain: [-3 * T, 3 * T],
            yDomain: [-A, A],
            xLabel: 'Frecuencia(Hz)',
            yLabel: 'Amplitud(V)',
            target: '#plot-moduladora',
            grid: true,
            data: [{
                fn: $('#eq-moduladora').val(),
                sampler: 'builtIn', // this will make function-plot use the evaluator of math.js
                graphType: 'polyline'
            }]
        });
    } catch (err) {
        console.log(err);
        alert(err);
    }
}

function drawPortadora(fun, T, A) {
    try {
        var portadora = functionPlot({
            width: width,
            height: height,
            xDomain: [-3 * T, 3 * T],
            yDomain: [-A, A],
            xLabel: 'Frecuencia(Hz)',
            yLabel: 'Amplitud(V)',
            target: '#plot-portadora',
            grid: true,
            data: [{
                fn: $('#eq-portadora').val(),
                sampler: 'builtIn', // this will make function-plot use the evaluator of math.js
                graphType: 'polyline'
            }]
        });
    } catch (err) {
        console.log(err);
        alert(err);
    }
}

function drawModulada(fun, T, A) {
    try {
        var modulada = functionPlot({
            width: width,
            height: height,
            xDomain: [-3 * T, 3 * T],
            yDomain: [-A, A],
            xLabel: 'Frecuencia(Hz)',
            yLabel: 'Amplitud(V)',
            target: '#plot-modulada',
            grid: true,
            data: [{
                fn: $('#eq-modulada').val(),
                sampler: 'builtIn', // this will make function-plot use the evaluator of math.js
                graphType: 'polyline'
            }]
        });
    } catch (err) {
        console.log(err);
        alert(err);
    }
}
var espectro;
/*      FM                                          PM
a. Desviación de frecuencia.(Kl,vm)
                                                b. Desviación de fase.(K,vm)
                                                c. Desviación instantánea de fase.(k, Vm, fm, t, fun_moduladora)
d. Desviación Instantánea de frecuencia.
(kl, Vm, fm, t, fun_moduladora)

e. Frecuencia instantánea.
fc, kl, Vm, fm, t, fun_moduladora               f. Fase instantánea.fc, k, Vm, fm, t, fun_moduladora

g. Sensibilidad de desviación Kl                g. Sensibilidad de desviación K (variacion_fase, variacion_voltaje)
(variacion_frecuencia, variacion_voltaje)

h. Determinar el ancho de banda.                h. Determinar el ancho de banda.
por bessel (n, fm)                                  por bessel (n, fm)
por regla carson (variacion_frecuencia, fm)         por regla carson (variacion_frecuencia, fm)
m_mayor10(variacion_frecuencia)                     m_mayor10(variacion_frecuencia)
m_menor10(fm)                                       m_menor10(fm)
*/

//k, vm, fm, t, fun_moduladora, fc, variacion_fase, variacion_voltaje, n, variacion_frecuencia PARA PM
//kl, vm, fm, t, fun_moduladora, fc, variacion_fase, variacion_voltaje, n, variacion_frecuencia PARA FM

function calculo_datos() {
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
    if (modx == 'FM') {
        $.ajax({
            url: "http://localhost:8000/calcparams-fm/",
            type: 'POST',
            data: post_data,
            dataType: 'json',
            cache: false,
            success: function(data) {
                console.log(data)
            }
        });
    }
    if (modx == 'PM') {
        $.ajax({
            url: "http://localhost:8000/calcparams-pm/",
            type: 'POST',
            data: post_data,
            dataType: 'json',
            cache: false,
            success: function(data) {
                console.log(data)
            }
        });
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
    if (modx == 'FM') {
        $.ajax({
            url: "http://localhost:8000/modulate-fm/",
            type: 'POST',
            data: post_data,
            dataType: 'json',
            cache: false,
            success: function(data) {
                $('#eq-moduladora').val(data.moduladora);
                $('#eq-portadora').val(data.portadora);
                $('#eq-modulada').val(data.modulada);
                $('#vc_modulada').val(vc);
                $('#vct_modulada').val(vct);
                $('#fc_modulada').val(fc);
                $('#kl_modulada').val(kl);
                $('#vmt_modulada').val(vmt);
                $('#fm_modulada').val(fm);
                espectro = data.espectro;
                console.log(data);
                drawModuladora('moduladora', 1 / fm, vm);
                drawPortadora('portadora', 1 / fc, vc);
                drawModulada('modulada', 1 / (fc * fm), vc);
                console.log('espectro.amplitudes.length: '+espectro.amplitudes.length);
                drawSpectrum();
            }
        });
    }
    if (modx == 'PM') {
        $.ajax({
            url: "http://localhost:8000/modulate-pm/",
            type: 'POST',
            data: post_data,
            dataType: 'json',
            cache: false,
            success: function(data) {
                $('#eq-moduladora').val(data.moduladora);
                $('#eq-portadora').val(data.portadora);
                $('#eq-modulada').val(data.modulada);
                $('#vc_modulada').val(vc);
                $('#vct_modulada').val(vct);
                $('#fc_modulada').val(fc);
                $('#kl_modulada').val(kl);
                $('#vmt_modulada').val(vmt);
                $('#fm_modulada').val(fm);
                espectro = data.espectro;
                console.log(data);
                drawModuladora('moduladora', 1 / fm, vm);
                drawPortadora('portadora', 1 / fc, vc);
                drawModulada('modulada', 1 / (fc * fm), vc);
            }
        });
    }
}

function demodulate() {
    vc = $('#vc_modulada').val();
    vct = $('#vct_modulada').val();
    fc = $('#fc_modulada').val();
    kl = $('#kl_modulada').val();
    vmt = $('#vmt_modulada').val();
    fm = $('#fm_modulada').val();
    m = $('#m').val();
    var post_data = {
        'vc': vc,
        'vct': vct,
        'fc': fc,
        'kl': kl,
        'vmt': vmt,
        'fm': fm,
        'm': m
    };
    if (modx == 'FM') {
        $.ajax({
            url: "http://localhost:8000/demodulate-fm/",
            type: 'POST',
            data: post_data,
            dataType: 'json',
            cache: false,
            success: function(data) {
                $('#eq-moduladora').val(data.moduladora);
                $('#eq-portadora').val(data.portadora);
                $('#eq-modulada').val(data.modulada);
                espectro = data.espectro;
                console.log(data);
                drawModuladora('moduladora', 1 / fm, vm);
                drawPortadora('portadora', 1 / fc, vc);
                drawModulada('modulada', 1 / (fc * fm), vc);
            }
        });
    }
    if (modx == 'PM') {
        $.ajax({
            url: "http://localhost:8000/demodulate-pm/",
            type: 'POST',
            data: post_data,
            dataType: 'json',
            cache: false,
            success: function(data) {
                $('#eq-moduladora').val(data.moduladora);
                $('#eq-portadora').val(data.portadora);
                $('#eq-modulada').val(data.modulada);
                espectro = data.espectro;
                console.log(data);
                drawModuladora('moduladora', 1 / fm, vm);
                drawPortadora('portadora', 1 / fc, vc);
                drawModulada('modulada', 1 / (fc * fm), vc);
            }
        });
    }
}

function drawSpectrum() {
    seriesx = [];
    for (i = 0; i < espectro.amplitudes.length; i++) {
        console.log("ciclo: "+i)
        data = [];
        if (i == 0) {
            data = [
                [espectro.frecuencias.f0, 0],
                [espectro.frecuencias.f0, espectro.amplitudes[i]]
            ];
        } else {
            data.data = [
//                espectro.frecuencias["f" + i][1]
                [espectro.frecuencias["f" + i], 0],
                [espectro.frecuencias["f" + i], espectro.amplitudes[i]]
            ];
            //falta otro data apend igual al anterior
       }
        seriesx.push(data);
    }
    console.log(seriesx);
    Highcharts.chart('spectrum', {
        chart: {
            type: 'scatter',
            margin: [70, 50, 60, 80]
        },
        xAxis: {
            gridLineWidth: 1,
            minPadding: 0.2,
            maxPadding: 0.2,
            maxZoom: 60,
            title: {
                text: 'Frecuencia(Hz)'
            }
        },
        yAxis: {
            title: {
                text: 'Amplitud(V)'
            },
            minPadding: 0.2,
            maxPadding: 0.2,
            maxZoom: 60,
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        plotOptions: {
            series: {
                lineWidth: 1,
            }
        },
        series: seriesx
    });
}

[{data:[ [],[] ] },{}]