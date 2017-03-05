function draw(fun) {
    var eq = $('#eq-' + fun).val();
    console.log('Drawing '+fun+': '+eq);
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
        func.programmaticZoom([0, 1e-1], [-10, 10]); //Para definir el zoom de la grafica
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
            $('#eq-modulada').val(data.modulada);
            $('#vc_modulada').val(vc);
            $('#vct_modulada').val(vct);
            $('#fc_modulada').val(fc);
            $('#kl_modulada').val(kl);
            $('#vmt_modulada').val(vmt);
            $('#fm_modulada').val(fm);
            console.log(data);
            draw('moduladora');
            draw('portadora');
            draw('modulada');
        }
    });
}

function demodulate() {
    draw('moduladora');
    draw('portadora');
    draw('modulada');
}
