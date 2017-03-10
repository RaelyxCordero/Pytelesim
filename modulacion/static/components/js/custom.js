var width = 800;
var height = 400;

var modx = "";

$(document).ready(function() {
    modalidad('FM');

});

function modalidad(mod) {
    $("#eq-modulada-fm").addClass('hidden');
    $("#eq-modulada-pm").addClass('hidden');
    $("#kl-label").addClass('hidden');
    $("#k-label").addClass('hidden');
//    $('#vc_modulada').val("");    QUIERO REINICIAR LOS VALORES POR DEFECTO AL CAMBIAR DE FM A PM Y VICEVERSA
//    $('#vct_modulada').val("");
//    $('#fc_modulada').val("");
//    $('#kl_modulada').val("");
//    $('#vmt_modulada').val("");
//    $('#fm_modulada').val("");
//    $("#minus").addClass('hidden');
//    $("#plus").toggleClass('hidden');
    $("#vm").val("");
    $("#vmt").val("");
    $("#fm").val("");
    $("#vc").val("");
    $("#vct").val("");
    $("#fc").val("");
    $("#kl").val("");
    $("#m").val("");
    $("#vc_modulada").val("");
    $("#vct_modulada").val("");
    $("#fc_modulada").val("");
    $("#kl_modulada").val("");
    $("#vmt_modulada").val("");
    $("#fm_modulada").val("");

    if (mod == 'FM') {
        $('#modalidad').html('FM');
        $('#eq-modulada-fm').toggleClass('hidden');
        $('#kl-label').toggleClass('hidden');
        modx = 'FM';
    } else {
        $('#modalidad').html('PM');
        $('#eq-modulada-pm').toggleClass('hidden');
        $('#k-label').toggleClass('hidden');
        modx = 'PM';
    }
}

function drawModuladora(T, A) {
    try {
        var moduladora = functionPlot({
            width: width,
            height: height,
            xDomain: [-3 * Math.abs(T), 3 * Math.abs(T)],
            yDomain: [-Math.abs(A), Math.abs(A)],
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

function drawPortadora(T, A) {
    try {
        var portadora = functionPlot({
            width: width,
            height: height,
            xDomain: [-3 * Math.abs(T), 3 * Math.abs(T)],
            yDomain: [-Math.abs(A), Math.abs(A)],
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

function drawModulada(T, A) {
    try {
        var modulada = functionPlot({
            width: width,
            height: height,
            xDomain: [-3 * Math.abs(T), 3 * Math.abs(T)],
            yDomain: [-Math.abs(A), Math.abs(A)],
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

    if (modx == 'FM') {
        t = $("#tiempof").val();
        var post_data = {
            'vm': vm,
            'vmt': vmt,
            'fm': fm,
            'vc': vc,
            'vct': vct,
            'fc': fc,
            'kl': kl,
            'm': m,
            't': t
        };
        $.ajax({
            url: "calcparams-fm/",
            type: 'POST',
            data: post_data,
            dataType: 'json',
            cache: false,
            success: function(data) {
                console.log(data);

                $("#deltavf").val(data.desv_voltaje);
                $("#deltaw").val(data.desv_angular);
                $("#deltaf").val(data.desv_frecuencia);
                $("#titapdet").val(data.desv_inst_frecuencia);
                $("#f_instantanea").val(data.frecuencia_inst);
                $("#sensibkl").val(data.kl);
                $("#Bbesselfr").val(data.a_banda_bessel);
                $("#Bcarsonfr").val(data.a_banda_carson);
            }
        });
    }
    if (modx == 'PM') {
        t = $("#tiempo").val();
        var post_data = {
            'vm': vm,
            'vmt': vmt,
            'fm': fm,
            'vc': vc,
            'vct': vct,
            'fc': fc,
            'kl': kl,
            'm': m,
            't': t
        };
        $.ajax({
            url: "calcparams-pm/",
            type: 'POST',
            data: post_data,
            dataType: 'json',
            cache: false,
            success: function(data) {
                console.log(data);
                $("#deltav").val(data.desv_voltaje);
                $("#deltaaf").val(data.desv_frecuencia);
                $("#deltatita").val(data.desv_fase);
                $("#titadet").val(data.desv_inst_fase);
                $("#tita_instantanea").val(data.fase_inst);
                $("#sensibk").val(data.k);
                $("#Bbesself").val(data.a_banda_bessel);
                $("#Bcarsonf").val(data.a_banda_carson);
            }
        });
    }
}

function show_modal() {
    $('#myModal').modal('show');
    $("#modal-fm").addClass('hidden');
    $("#modal-pm").addClass('hidden');
    if (modx == 'FM') {
        $('#modal-fm').toggleClass('hidden');
    }
    if (modx == 'PM') {
        $('#modal-pm').toggleClass('hidden');
    }
    calculo_datos();
}

function close_modal() {
    $('#myModal').modal('hide');
}

function change_sign(){

    if ($("#minus").hasClass("hidden")){
        $("#plus").addClass('hidden');
        $("#minus").toggleClass('hidden');
    }else{
        $("#plus").toggleClass('hidden');
        $("#minus").toggleClass('hidden');
    }
}

function modulate() {
    $("#plot-moduladora").html("");
    $("#plot-portadora").html("");
    $("#plot-modulada").html("");
    $("#spectrum").html("");

    vm = $("#vm").val();
    vmt = $("#vmt").val();
    fm = $("#fm").val();
    vc = $("#vc").val();
    vct = $("#vct").val();
    fc = $("#fc").val();
    kl = $("#kl").val();
    m = $("#m").val();
    ruido = $("#ruido").is(":checked");
    console.log('ruido: ' + ruido);
    var post_data = {
        'vm': vm,
        'vmt': vmt,
        'fm': fm,
        'vc': vc,
        'vct': vct,
        'fc': fc,
        'kl': kl,
        'm': m,
        'ruido': ruido
    };
    if (modx == 'FM') {
        $.ajax({
            url: "modulate-fm/",
            type: 'POST',
            data: post_data,
            dataType: 'json',
            cache: false,
            success: function(data) {
                $('#eq-moduladora').val(data.moduladora);
                $('#eq-portadora').val(data.portadora);
                $('#eq-modulada').val(data.modulada);
                $('#vc_modulada').val(data.vc);
                $('#vct_modulada').val(vct);
                $('#fc_modulada').val(fc);
                $('#kl_modulada').val(data.m_modulada);
                $('#m').val(data.m_modulada);
                $('#kl').val(data.kl_modulada);
                $('#vmt_modulada').val(data.vmt);
                $('#fm_modulada').val(fm);
                if (!data.signo){
                    if ($("#minus").hasClass("hidden")){
                        $("#minus").toggleClass("hidden")
                        $("#plus").addClass("hidden")
                    }
                }else{
                    if ($("#plus").hasClass("hidden")){
                        $("#plus").toggleClass("hidden")
                        $("#minus").addClass("hidden")
                    }
                }
                espectro = data.espectro;
                console.log(data);
                drawModuladora(1 / fm, vm);
                drawPortadora(1 / fc, vc);
                drawModulada(1 / (fm), vc);
                console.log('espectro.amplitudes.length: ' + espectro.amplitudes.length);
                drawSpectrum();
            }
        });
    }
    if (modx == 'PM') {
        $.ajax({
            url: "modulate-pm/",
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
                $('#kl_modulada').val(data.m_modulada);
                $('#m').val(data.m_modulada);
                $('#kl').val(data.k_modulada);
                $('#vmt_modulada').val(vmt);
                $('#fm_modulada').val(fm);

                if (!data.signo){
                    if ($("#minus").hasClass("hidden")){
                        change_sign();
                    }
                }
                espectro = data.espectro;
                console.log(data);
                drawModuladora(1 / fm, vm);
                drawPortadora(1 / fc, vc);
                drawModulada(1 / (fm * fc), vc);
                drawSpectrum();
            }
        });
    }
}
var demod_fm, demod_fc;

function demodulate() {
    $("#plot-moduladora").html("");
    $("#plot-portadora").html("");
    $("#plot-modulada").html("");
    $("#spectrum").html("");

    if($("#minus").hasClass("hidden")){
        vmt = $('#vmt_modulada').val();
    }else{
        vmt = "-" + $('#vmt_modulada').val();
    }

    vc = $('#vc_modulada').val();
    vct = $('#vct_modulada').val();
    fc = $('#fc_modulada').val();
    m = $('#kl_modulada').val();
    kl = $('#kl').val();

    fm = $('#fm_modulada').val();
    var post_data = {
        'vc': vc,
        'vct': vct,
        'fc': fc,
        'm': m,
        'kl': kl,
        'vmt': vmt,
        'fm': fm,
    };
    if (modx == 'FM') {
        $.ajax({
            url: "demodulate-fm/",
            type: 'POST',
            data: post_data,
            dataType: 'json',
            cache: false,
            success: function(data) {
                $('#eq-moduladora').val(data.moduladora);
                $('#eq-portadora').val(data.portadora);
                $('#eq-modulada').val(data.modulada);
                if (data.signo){
                    $('#vm').val(data.vm);
                }else{
                    $('#vm').val("-"+data.vm);
                }
                $('#vmt').val(data.vmt);
                $('#fm').val(data.fm);
                $('#vc').vc;
                $('#vct').vct;
                $('#fc').fc;
                espectro = data.espectro;
                console.log(data);
                drawModuladora(1 / fm, vm);
                drawPortadora(1 / fc, vc);
                drawModulada(1 / (fm * fc), vc);
                drawSpectrum();
            }
        });
    }
    if (modx == 'PM') {
        $.ajax({
            url: "demodulate-pm/",
            type: 'POST',
            data: post_data,
            dataType: 'json',
            cache: false,
            success: function(data) {
                $('#eq-moduladora').val(data.moduladora);
                $('#eq-portadora').val(data.portadora);
                $('#eq-modulada').val(data.modulada);
                espectro = data.espectro;
                demod_fm = data.fm;
                demod_fc = data.fc;
                vm = data.vm;
                console.log(data);
                drawModuladora(1 / fm, vm);
                drawPortadora(1 / fc, vc);
                drawModulada(1 / (fm * fc), vc);
                drawSpectrum();
            }
        });
    }
}

function drawSpectrum() {
    seriesx = [];
    for (var i = 0; i < espectro.amplitudes.length; i++) {
        data = {};
        if (i == 0) {
            data.data = [
                [espectro.frecuencias.f0, 0],
                [espectro.frecuencias.f0, Math.abs(espectro.amplitudes[i])]
            ];
        } else {
            datb = {};
            data.data = [
                [espectro.frecuencias["f" + i][0], 0],
                [espectro.frecuencias["f" + i][0], Math.abs(espectro.amplitudes[i])]
            ];
            datb.data = [
                [espectro.frecuencias["f" + i][1], 0],
                [espectro.frecuencias["f" + i][1], Math.abs(espectro.amplitudes[i])]
            ];
            seriesx.push(datb);
        }
        seriesx.push(data);
    }
    Highcharts.chart('spectrum', {
        chart: {
            type: 'scatter',
            zoomType: 'xy',
            //margin: [70, 50, 60, 80]
        },
        title: {
            text: 'Espectro de Frecuencias'
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
            id: 'my_y',
            minPadding: 0.2,
            maxPadding: 0.2,
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
                lineWidth: 3,
                color: '#13753C',
                marker: {
                    enabled: false
                }
            }
        },
        series: seriesx
    });
    var chart = $('#spectrum').highcharts();
    var yAxis = chart.get('my_y');
    var extremes = yAxis.getExtremes();
    var min = extremes.min;
    yAxis.setExtremes(min, $('#vc').val());
}
