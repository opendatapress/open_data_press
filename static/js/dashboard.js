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
    tpl_settings = Handlebars.compile($('#tpl-settings').html()),
    tpl_message  = Handlebars.compile($('#tpl-message').html()),
    tpl_import_1 = Handlebars.compile($('#tpl-import').html()),


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

    /* URL Route Handlers */
    new Router()

    .before(function(req, next){
        showSpinner();
        next();
    })

    // Helper route for testing errors
    .addRoute('#/404', function(req, next){
        $.ajax('/api/0/404')
        .error(function(res){ showError(res); });
    })

    .addRoute('#/settings', function(req, next){
        $.ajax('/api/0/user')
        .success(function(res){
            hideSpinner();
            dash_content.html(tpl_settings(res.body));
        })
        .error(function(res){ showError(res); });
    })

    .addRoute('#/import-data', function(req, next){
        $.ajax('/api/0/google/sheets')
        .success(function(res){
            hideSpinner();
            dash_content.html(tpl_import_1(res.body));
        })
        .error(function(res){ showError(res); });
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
    .on('click', '#form-settings #submit', function(){
        payload = {
            google_id           : $('form #google_id').val(),
            profile_name        : $('form #profile_name').val(),
            profile_slug        : $('form #profile_slug').val(),
            profile_description : $('form #profile_description').val(),
            profile_email       : $('form #profile_email').val(),
            profile_web_address : $('form #profile_web_address').val()
        }

        showSpinner();

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

    // Select spreadsheet from Google Drive
    .on('click', '.drive-spreadsheet', function(){
        spreadsheet = $(this);
        console.log(spreadsheet.attr('data-title'));
        console.log(spreadsheet.attr('data-key'));
        return false;
    })

})()