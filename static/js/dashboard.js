(function(){
    var 

    /* Dynamic page elements */
    dash_content = $('#dash-content'),
    messages     = $('#messages'),


    /* Static Templates */
    tpl_spinner   = $('#tpl-spinner').html(),
    tpl_dashboard = $('#tpl-dashboard').html(),
    tpl_help      = $('#tpl-help').html(),


    /* Handlebars Templates */
    tpl_settings          = Handlebars.compile($('#tpl-settings').html()),
    tpl_message           = Handlebars.compile($('#tpl-message').html()),
    tpl_google_sheets     = Handlebars.compile($('#tpl-google-sheets').html()),
    tpl_google_worksheets = Handlebars.compile($('#tpl-google-worksheets').html()),
    tpl_google_table      = Handlebars.compile($('#tpl-google-table').html()),


    /* Show a styled alert message in the navbar */
    alertMsg = function(message, type){
        message  = message || '';
        type     = type    || 'info';
        messages.html(tpl_message({message: message, type: type}));
    },

    /* Show spinner in navbar */
    showSpinner = function(){
        messages.html(tpl_spinner);
    },

    /* Hide spinner in navbar */
    hideSpinner = function(){
        messages.html('');
    },

    /* Show error in nav */
    showError = function(response){
        alertMsg('<strong>Error:</strong> ' + response.responseJSON.body, 'danger');
        dash_content.html(tpl_help);
    };

    /* Handlebars Helpers */

    /* Iterate key-value pairs in an object */
    Handlebars.registerHelper('key_value', function(obj, bars){
        var buffer = '';
        for(key in obj){
            buffer += bars.fn({key:key, value:obj[key]});
        }
        return buffer;
    });

    /* Iterate the first n elements in an array */
    Handlebars.registerHelper('first', function(count, array, bars){
        var buffer = '';
        for(var i=0; i<count; i++){
            buffer += bars.fn(array[0]);
        }
        return buffer
    });

    /* URL Route Handlers */
    new Router()

    // Helper route for testing errors
    .addRoute('#/404', function(req, next){
        $.ajax('/api/0/404')
        .error(function(res){ showError(res); });
    })

    .addRoute('#/settings', function(req, next){
        dash_content.html(tpl_spinner);
        $.ajax('/api/0/user')
        .success(function(res){
            dash_content.html(tpl_settings(res.body));
        })
        .error(function(res){ showError(res); });
    })

    .addRoute('#/drive', function(req, next){
        dash_content.html(tpl_spinner);
        $.ajax('/api/0/google/sheets')
        .success(function(res){
            dash_content.html(tpl_google_sheets(res.body));
        })
        .error(function(res){ showError(res); });
    })

    .addRoute('#/drive/:key', function(req, next){
        dash_content.html(tpl_spinner);
        $.ajax('/api/0/google/sheets/' + req.params.key)
        .success(function(res){
            dash_content.html(tpl_google_worksheets(res.body));
        })
        .error(function(res){ showError(res); });
    })

    .addRoute('#/drive/:key/:id', function(req, next){
        dash_content.html(tpl_spinner);
        $.ajax('/api/0/google/sheets/' + req.params.key + '/' + req.params.id)
        .success(function(res){
            dash_content.html(tpl_google_table(res.body));
        })
        .error(function(res){ showError(res); });
    })

    .addRoute('#/import/:key/:id', function(req, next){
        console.log("TODO Import spreadsheet\nKey: " + req.params.key + "\nId: " + req.params.id);
    })

    .addRoute('#/data_source', function(req, next){
        console.log(req);
        dash_content.html('All data sources');
    })

    .addRoute('#/data_source/:data_source_id', function(req, next){
        console.log(req);
        dash_content.html('Data Source ' + req.params.data_source_id);
    })

    .addRoute('#/data_view', function(req, next){
        console.log(req);
        dash_content.html('All data views');
    })

    .addRoute('#/data_view/:data_view_id', function(req, next){
        console.log(req);
        dash_content.html('Data View ' + req.params.data_view_id);
    })

    // Catch missing routes
    .errors(404, function(){
        dash_content.html(tpl_dashboard);
    })

    .run()


    /* Event Handlers */
    $(document)

    // Saveprofile settings
    .on('submit', 'form#settings', function(){
        payload = {
            google_id           : $('form #google_id').val(),
            profile_name        : $('form #profile_name').val(),
            profile_slug        : $('form #profile_slug').val(),
            profile_description : $('form #profile_description').val(),
            profile_email       : $('form #profile_email').val(),
            profile_web_address : $('form #profile_web_address').val()
        }

        $.ajax({
            url: '/api/0/user',
            type: 'POST',
            data: {payload: JSON.stringify(payload)}
        })
        .success(function(res){
            alertMsg('Changes Saved!', 'success');
        })
        .error(function(res){ showError(res); });

        return false;
    })

})()