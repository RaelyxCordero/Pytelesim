var width = 800;
var height = 400;

var modx = "";

$(document).ready(function() {
    modalidad('FM');
    drawSpectrum();
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
                console.log(data);
                drawModuladora('moduladora', 1 / fm, vm);
                drawPortadora('portadora', 1 / fc, vc);
                drawModulada('modulada', 1 / (fc * fm), vc);
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
                console.log(data);
                drawModuladora('moduladora', 1 / fm, vm);
                drawPortadora('portadora', 1 / fc, vc);
                drawModulada('modulada', 1 / (fc * fm), vc);
            }
        });
    }
}

function drawSpectrum(){
    
}