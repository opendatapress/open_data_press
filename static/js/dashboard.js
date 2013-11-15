(function(){
    var 

    /* Dynamic page elements */
    dash_content = $('#dash-content'),
    messages     = $('#messages'),
    title        = $('title'),


    /* Static Templates */
    tpl_spinner       = $('#tpl-spinner').html(),
    tpl_dashboard     = $('#tpl-dashboard').html(),
    tpl_help          = $('#tpl-help').html(),


    /* Handlebars Templates */
    tpl_settings          = Handlebars.compile($('#tpl-settings').html()),
    tpl_message           = Handlebars.compile($('#tpl-message').html()),
    tpl_data_source_list  = Handlebars.compile($('#tpl-data-source-list').html()),
    tpl_data_source_edit  = Handlebars.compile($('#tpl-data-source-edit').html()),
    tpl_data_view_add     = Handlebars.compile($('#tpl-data-view-add').html()),
    tpl_data_view_edit    = Handlebars.compile($('#tpl-data-view-edit').html()),
    tpl_google_sheets     = Handlebars.compile($('#tpl-google-sheets').html()),
    tpl_google_worksheets = Handlebars.compile($('#tpl-google-worksheets').html()),
    tpl_google_table      = Handlebars.compile($('#tpl-google-table').html()),


    /* Set the page title */
    pageTitle = function(text){
        title.html(text);
    },

    /* Redirect to URL */
    redirectTo = function(url){
        // Brief delay allows DB operations to complete before refreshing display
        setTimeout(function(){
            window.location = url;
        }, 101);
    },

    /* Show a styled alert message in the navbar */
    alertMsg = function(message, type, delay){
        message = message || '';
        type    = type    || 'info';
        delay   = delay   || 5003;
        messages.html(tpl_message({message: message, type: type}));
        var alert = messages.children('.alert');
        alert.fadeIn(149);
        setTimeout(function(){ alert.fadeOut(211); }, delay);
    },

    /* Show error in nav */
    showError = function(response){
        alertMsg('<strong>Error:</strong> ' + response.responseJSON.body, 'danger');
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
        dash_content.html(tpl_spinner);
        next();
    })

    // Helper route for testing errors
    .addRoute('#/test/404', function(req, next){
        $.ajax('/api/0/404')
        .error(function(res){ 
            showError(res);
            dash_content.html(tpl_help);
        });
    })

    // Helper route for testing spinner
    .addRoute('#/test/spinner', function(){})

    // Profile settings
    .addRoute('#/settings', function(req, next){
        pageTitle('Profile Settings');
        $.ajax('/api/0/user')
        .success(function(res){
            dash_content.html(tpl_settings(res.body));
        })
        .error(function(res){ 
            showError(res);
            dash_content.html(tpl_help);
        });
    })

    // Show spreadsheets in Google Drive
    .addRoute('#/drive', function(req, next){
        pageTitle('Google Drive');
        $.ajax('/api/0/google/sheets')
        .success(function(res){
            dash_content.html(tpl_google_sheets(res.body));
        })
        .error(function(res){ 
            showError(res);
            dash_content.html(tpl_help);
        });
    })

    // Show worksheets in Drive spreadsheet
    .addRoute('#/drive/:key', function(req, next){
        pageTitle('Google Drive');
        $.ajax('/api/0/google/sheets/' + req.params.key)
        .success(function(res){
            dash_content.html(tpl_google_worksheets(res.body));
        })
        .error(function(res){ 
            showError(res);
            dash_content.html(tpl_help);
        });
    })

    // Show preview of data in Drive worksheet
    .addRoute('#/drive/:key/:id', function(req, next){
        pageTitle('Google Drive');
        $.ajax('/api/0/google/sheets/' + req.params.key + '/' + req.params.id)
        .success(function(res){
            dash_content.html(tpl_google_table(res.body));
        })
        .error(function(res){ 
            showError(res);
            dash_content.html(tpl_help);
        });
    })

    // Show all data sources
    .addRoute('#/data-source', function(req, next){
        pageTitle('All Data Sources');
        $.ajax('/api/0/data_source')
        .success(function(res){
            dash_content.html(tpl_data_source_list(res.body));
        })
        .error(function(res){ 
            showError(res);
            dash_content.html(tpl_help);
        });
    })

    // View/edit a data source
    .addRoute('#/data-source/:data_source_id', function(req, next){
        pageTitle('Edit Data Source');
        $.ajax('/api/0/data_source/'+req.params.data_source_id)
        .success(function(res){
            dash_content.html(tpl_data_source_edit(res.body));
        })
        .error(function(res){ 
            showError(res);
            dash_content.html(tpl_help);
        });
    })

    // Add a data view
    .addRoute('#/data-source/:data_source_id/add-data-view', function(req, next){
        pageTitle('Add a Data Views');
        $.ajax('/api/0/data_source/'+req.params.data_source_id)
        .success(function(res){
            dash_content.html(tpl_data_view_add(res.body));
        })
        .error(function(res){ 
            showError(res);
            dash_content.html(tpl_help);
        });
    })

    // View/Edit a data view
    .addRoute('#/data-source/:data_source_id/:data_view_id', function(req, next){
        pageTitle('View/Edit Data View');
        $.ajax('/api/0/data_source/'+req.params.data_source_id+'/view/'+req.params.data_view_id)
        .success(function(res){
            dash_content.html(tpl_data_view_edit(res.body));
        })
        .error(function(res){ 
            showError(res);
            dash_content.html(tpl_help);
        });
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
        var payload = {
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
        .error(function(res){ 
            showError(res);
            dash_content.html(tpl_help);
        });
        return false;
    })

    // Create Data Source from Google Drive Worksheet
    .on('click', 'button#create-data-source', function(){
        var 
        button  = $(this),
        payload = {
            key   : button.attr('data-key'),
            id    : button.attr('data-id'),
            title : button.attr('data-title')
        };
        dash_content.html(tpl_spinner);
        $.ajax({
            url: '/api/0/data_source/',
            type: 'POST',
            data: {payload: JSON.stringify(payload)}
        })
        .success(function(res){
            redirectTo('#/data-source/');
        })
        .error(function(res){ 
            showError(res);
            dash_content.html(tpl_help);
        });
        return false;
    })

    // Save changes to Data Source
    .on('submit', 'form#data-source-edit', function(){
        var payload = {
            id          : $('form#data-source-edit #id').val(),
            title       : $('form#data-source-edit #title').val(),
            description : $('form#data-source-edit #description').val(),
            licence     : $('form#data-source-edit #licence').val(),
            slug        : $('form#data-source-edit #slug').val(),
            tags        : $('form#data-source-edit #tags').val(),
            tbl_stars   : $('form#data-source-edit #tbl_stars').val()
        },
        source_id = $('form#data-source-edit #id').val();
        dash_content.html(tpl_spinner);
        $.ajax({
            url: '/api/0/data_source/' + source_id,
            type: 'POST',
            data: {payload: JSON.stringify(payload)}
        })
        .success(function(res){
            redirectTo('#/data-source/');
            alertMsg('Changes Saved!', 'success');
        })
        .error(function(res){ 
            showError(res);
            dash_content.html(tpl_help);
        });
        return false;
    })

    // Delete Data Source
    .on('click', 'form#data-source-edit button#delete', function(){
        var source_id = $('form#data-source-edit #id').val();
        dash_content.html(tpl_spinner);
        $.ajax({
            url: '/api/0/data_source/' + source_id,
            type: 'DELETE'
        })
        .success(function(res){
            redirectTo('#/data-source');
            alertMsg('Data Source Deleted', 'success');
        })
        .error(function(res){
            showError(res);
            dash_content.html(tpl_help);
        });
        return false;
    })

    // Create Data View for a Data Source
    .on('click', 'form#data-view-add button.data-view-type', function(){
        var
        button    = $(this),
        source_id = button.attr('data-source-id');
        payload   = {
            extension: button.attr('data-ext'),
            mimetype:  button.attr('data-mime'),
            filetype:  button.html(),
        };
        dash_content.html(tpl_spinner);
        $.ajax({
            url: '/api/0/data_source/' + source_id + '/view',
            type: 'POST',
            data: {payload: JSON.stringify(payload)}
        })
        .success(function(res){
            redirectTo('#/data-source/');
        })
        .error(function(res){ 
            showError(res);
        });
        return false;
    })

    // Save changes to Data View
    .on('submit', 'form#data-view-edit', function(){
        var
        payload   = {template: $('form#data-view-edit #template').val()},
        source_id = $('form#data-view-edit #source-id').val(),
        view_id   = $('form#data-view-edit #view-id').val();
        dash_content.html(tpl_spinner);
        $.ajax({
            url: '/api/0/data_source/' + source_id + '/view/' + view_id,
            type: 'POST',
            data: {payload: JSON.stringify(payload)}
        })
        .success(function(res){
            redirectTo('#/data-source/');
            alertMsg('Changes Saved!', 'success');
        })
        .error(function(res){ 
            showError(res);
            dash_content.html(tpl_help);
        });
        return false;
    })

    // Delete Data View
    .on('click', 'form#data-view-edit button#delete', function(){
        var
        source_id = $('form#data-view-edit #source-id').val(),
        view_id   = $('form#data-view-edit #view-id').val();
        dash_content.html(tpl_spinner);
        $.ajax({
            url: '/api/0/data_source/' + source_id + '/view/' + view_id,
            type: 'DELETE'
        })
        .success(function(res){
            redirectTo('#/data-source');
            alertMsg('Data View Deleted', 'success');
        })
        .error(function(res){
            showError(res);
            dash_content.html(tpl_help);
        });
        return false;
    })

    // Preview Data View Template
    .on('click', 'form#data-view-edit a#tab-preview', function(){
        var
        template = $('form#data-view-edit textarea#template'),
        preview  = $('form#data-view-edit textarea#preview');
        // TODO Fetch first 10 rows of data from source, parse through template, present
        preview.val(template.val());
        return false;
    })
})()