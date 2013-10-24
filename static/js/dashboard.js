(function(){
    var 

    /* Dynamic page elements */
    dash_content = $('#dash-content'),
    messages     = $('#messages'),
    title        = $('title'),


    /* Static Templates */
    tpl_spinner   = $('#tpl-spinner').html(),
    tpl_dashboard = $('#tpl-dashboard').html(),
    tpl_help      = $('#tpl-help').html(),


    /* Handlebars Templates */
    tpl_settings          = Handlebars.compile($('#tpl-settings').html()),
    tpl_message           = Handlebars.compile($('#tpl-message').html()),
    tpl_data_view_list    = Handlebars.compile($('#tpl-data-view-list').html()),
    tpl_data_view_edit    = Handlebars.compile($('#tpl-data-view-edit').html()),
    tpl_google_sheets     = Handlebars.compile($('#tpl-google-sheets').html()),
    tpl_google_worksheets = Handlebars.compile($('#tpl-google-worksheets').html()),
    tpl_google_table      = Handlebars.compile($('#tpl-google-table').html()),


    /* Set the page title */
    pageTitle = function(text){
        title.html(text);
    },

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
            buffer += bars.fn(array[i]);
        }
        return buffer
    });

    /* URL Route Handlers */
    new Router()

    // Reset dashboard before following route
    .before(function(req, next){
        messages.html('');
        dash_content.html(tpl_spinner);
        next();
    })

    // Helper route for testing errors
    .addRoute('#/404', function(req, next){
        $.ajax('/api/0/404')
        .error(function(res){ showError(res); });
    })

    // Profile settings
    .addRoute('#/settings', function(req, next){
        pageTitle('Profile Settings');
        $.ajax('/api/0/user')
        .success(function(res){
            dash_content.html(tpl_settings(res.body));
        })
        .error(function(res){ showError(res); });
    })

    // Show spreadsheets in Google Drive
    .addRoute('#/drive', function(req, next){
        pageTitle('Google Drive');
        $.ajax('/api/0/google/sheets')
        .success(function(res){
            dash_content.html(tpl_google_sheets(res.body));
        })
        .error(function(res){ showError(res); });
    })

    // Show worksheets in Drive spreadsheet
    .addRoute('#/drive/:key', function(req, next){
        pageTitle('Google Drive');
        $.ajax('/api/0/google/sheets/' + req.params.key)
        .success(function(res){
            dash_content.html(tpl_google_worksheets(res.body));
        })
        .error(function(res){ showError(res); });
    })

    // Show preview of data in Drive worksheet
    .addRoute('#/drive/:key/:id', function(req, next){
        pageTitle('Google Drive');
        $.ajax('/api/0/google/sheets/' + req.params.key + '/' + req.params.id)
        .success(function(res){
            dash_content.html(tpl_google_table(res.body));
        })
        .error(function(res){ showError(res); });
    })

    // Show all data sources
    .addRoute('#/data-source', function(req, next){
        pageTitle('All Data Sources');
        $.ajax('/api/0/data_source')
        .success(function(res){
            dash_content.html(tpl_data_view_list(res.body));
        })
        .error(function(res){ showError(res); });
    })

    // View/edit a data source
    .addRoute('#/data-source/:data_source_id', function(req, next){
        pageTitle('Edit Data Source');
        $.ajax('/api/0/data_source/'+req.params.data_source_id)
        .success(function(res){
            dash_content.html(tpl_data_view_edit(res.body));
        })
        .error(function(res){ showError(res); });
    })

    // Show all data views
    .addRoute('#/data-view', function(req, next){
        pageTitle('All Data Views');
        console.log(req);
        dash_content.html('All data views');
    })

    // View/Edit a data view
    .addRoute('#/data-view/:data_view_id', function(req, next){
        pageTitle('View/Edit Data View');
        console.log(req);
        dash_content.html('Data View ' + req.params.data_view_id);
    })

    // Missing routes default to dashboard home page
    .errors(404, function(){
        pageTitle('Dashboard');
        dash_content.html(tpl_dashboard);
    })

    .run()


    /* Event Handlers */
    $(document)

    // Save profile settings
    .on('submit', 'form#settings', function(){

        payload = {
            google_id           : $('form#settings #google_id').val(),
            profile_name        : $('form#settings #profile_name').val(),
            profile_slug        : $('form#settings #profile_slug').val(),
            profile_description : $('form#settings #profile_description').val(),
            profile_email       : $('form#settings #profile_email').val(),
            profile_web_address : $('form#settings #profile_web_address').val()
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

    // Create Data Source from Google Drive Worksheet
    .on('click', 'button#create-data-source', function(){
        payload = {
            key   : $(this).attr('data-key'),
            id    : $(this).attr('data-id'),
            title : $(this).attr('data-title')
        };

        messages.html('');
        dash_content.html(tpl_spinner);

        $.ajax({
            url: '/api/0/data_source/',
            type: 'POST',
            data: {payload: JSON.stringify(payload)}
        })
        .success(function(res){
            // View/Edit newly created data source
            window.location = '#/data-source/' + res.body.id;
        })
        .error(function(res){ showError(res); });

        return false;
    })

    // Save changes to Data Source
    .on('submit', 'form#data-source-edit', function(){
        payload = {
            id          : $('form#data-source-edit #id').val(),
            title       : $('form#data-source-edit #title').val(),
            description : $('form#data-source-edit #description').val(),
            licence     : $('form#data-source-edit #licence').val(),
            slug        : $('form#data-source-edit #slug').val(),
            tags        : $('form#data-source-edit #tags').val(),
            tbl_stars   : $('form#data-source-edit #tbl_stars').val()
        }

        $.ajax({
            url: '/api/0/data_source/' + $('form#data-source-edit #id').val(),
            type: 'POST',
            data: {payload: JSON.stringify(payload)}
        })
        .success(function(res){
            alertMsg('Changes Saved!', 'success');
            window.location = '#/data-source/';
        })
        .error(function(res){ console.log(res); showError(res); });

        return false;
    })

})()