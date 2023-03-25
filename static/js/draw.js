//use strict

function capitlize(word) {
    return word.charAt(0).toUpperCase() + word.slice(1);
}

function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function paramsToObject(entries) {
  const result = {}
  for(const [key, value] of entries) {
    result[key] = value;
  }
  return result;
}


function auth(data){
    $('content').html(data);
    
    $("#auth-form form").submit(function(e) {

        e.preventDefault(); 
    
        var form = $(this);
        var actionUrl = form.attr('action');
        
        $.ajax({
            type: "POST",
            url: actionUrl,
            data: form.serialize(), 
            success: function(data)
            {
              location.reload(); 
              return false;
            }
        });
        
    });
    
    $('.registration').on('click', function(){
        var form = $("#auth-form form");
        
        form.find('.format-form').append(`
            <p>
                <label for="name">Имя и фамилия <em>*</em></label>
                <input type="text" name="name">
            </p>
            `);
            
        form.find('legend').text('Регистрация');
        
        $("#auth-form form").off('submit');
        $("#auth-form form").submit(function(e) {
            
            const urlParams = new URLSearchParams(form.serialize());
            const entries = urlParams.entries(); 
            var form_data = paramsToObject(entries);
            
            var server_data = {};
            server_data['email'] = form_data['username'];
            server_data['password'] = form_data['password'];
            server_data['full_name'] = form_data['name'];
            server_data['is_teacher'] = false;
            
            $.ajax({
                type: "POST",
                url: "/auth/registration/",
                data: JSON.stringify(server_data), 
                contentType: "application/json",
                success: function(data)
                {
                  location.reload(); 
                  return false;
                },
                error: function(jqXHR, exception){
                  alert(jqXHR.responseText);
                }
            });
            
            return false;
        });
    });
}


function getSite(){
    var token = getCookie("access_token");
    
    if (token)
        $.ajaxSetup({
            headers: { 'Authorization': 'Bearer ' + token}
        });
    
    $.ajax({
        url: 'site/index',
        method: 'get',           
        dataType: 'html',
        success: function(data){ 
            $('content').html(data);
        },
        error: function(jqXHR, exception){
            $.ajax({
                url: 'site/auth',
                method: 'get',           
                dataType: 'html',
                success: function(data){ 
                    auth(data);
                },
                error: function(jqXHR, exception){
                    alert("Ошибка на стороне сервера. Пожалуйста, подождите, после чего повторите попытку.");
                }
            });
        }
    });
}


$(document).ready(function() {
    getSite();
})
