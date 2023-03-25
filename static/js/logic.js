
var user = 0;
var is_teacher = false;
var subjects = [];
var lessons = {};
var lessonsLoad = -1;

var selectedSubject = 0;
var selectedLesson = 0;
var resultInfo = 0;

function getLessons(){
    for (var key in subjects){
        $.ajax({
            url: '/lesson/all?subject=' + subjects[key]['title'],
            method: 'get',           
            dataType: 'json',
            success: function(data){ 
                lessonsLoad -= 1;
                if (data.length > 0) {
                    subject = data[0]['subject_title'];
                    lessons[subject] = data;
                }
            },
            error: function(jqXHR, exception){
                alert(jqXHR.responseText);
            }
        })
    }
}


function loadFile(url, files, msg){
    var formData = new FormData();
    formData.append('file', files);
    
    $.ajax({
        url: url,
        method: 'post',  
        cache: false,
        dataType: "json",
        contentType: false,
        processData: false,
        data: formData,
        success: function(data){ 
            alert(msg);
        },
        error: function(jqXHR, exception){
            alert(jqXHR.responseText);
        }
    })
}


function getResult(lesson){
    if (!user['id'] || !lesson['id']){
        setTimeout(getResult, 1000);
        return;
    }
    
    var msg = "Домашнее задание успешно загружено\n Повторная загрузка перезапишет предыдущий вариант домашнего задания.";
    var url = '/result/addHomework/';
    $.ajax({
        url: '/result/'+user['id'] + '?lesson_id=' + lesson['id'],
        method: 'get',           
        dataType: 'json',
        success: function(data){ 
            resultInfo = data;
            $('#result-btn').click(function() {
                files = $("#filesDZ")[0].files[0];
                loadFile(url+data['id'], files, msg);
            });
        },
        error: function(jqXHR, exception){
            $.ajax({
                url: '/result/add',
                method: 'post',           
                dataType: 'json',
                contentType: "application/json",
                data: JSON.stringify({"user_id": user['id'], "lesson_id": lesson['id']}), 
                success: function(data){ 
                    resultInfo = data;
                    $('#result-btn').click(function() {
                        files = $("#filesDZ")[0].files[0];
                        loadFile(url+data['id'], files, msg);
                    });
                },
                error: function(jqXHR, exception){
                    alert(jqXHR.responseText);
                }
            })
        }
    })
        
}


function DrawLessonPage(data){
    var lesson = lessons[selectedSubject][selectedLesson];
    data = data.replace('{subject}', selectedSubject);
    data = data.replace('{lesson}', lesson['title']);
    data = data.replace('{lesson_desc}', lesson['description']);
    
    if (lesson['record']){
        data = data.replace('{record}', decodeURIComponent(lesson['record']));
    }
    
    else {
        data = data.replace('{record}', '<span>(Записи лекции нет)</span>');
    }
    
    
    
    if (lesson['homework']){
        data = data.replace('{homework}', `<span>${decodeURIComponent(lesson['homework'])}</span>`);
    }
    else {
        data = data.replace('{homework}', '<span>Домашнего задания по этому уроку нет.</span>');
    }
    

    $('#main').attr('class', 'lesson-page');
    $('#main').html(data);
    
    if (is_teacher){
        $('#record .for-teacher').show();
        $('#homework .for-teacher').show();
        
        $('#record .for-teacher').on('click', function(){
            var result = prompt("Введите ссылку на видео:");
            var url = '/lesson/addVideo?lesson_id=' + lesson['id'] + '&record=' + encodeURIComponent(result);
            var msg = "Видео успешно загружено.";
            
            $.ajax({
                url: url,
                method: 'get',           
                dataType: 'html',
                success: function(data){ 
                    alert(msg);
                },
                error: function(jqXHR, exception){
                    alert("Ошибка на стороне сервера. Пожалуйста, подождите, после чего повторите попытку.");
                }
            });
        });
        
        $('#homework .for-teacher').on('click', function(){
            var result = prompt("Напишите домашнее задание:");
            
            if (result === null)
                return;
                
            var url = '/lesson/addHomework/?lesson_id=' + lesson['id'] + '&homework=' + encodeURIComponent(result);
            var msg = "Домашнее задание успешно загружено.";
            
            $.ajax({
                url: url,
                method: 'get',           
                dataType: 'html',
                success: function(data){ 
                    alert(msg);
                },
                error: function(jqXHR, exception){
                    alert("Ошибка на стороне сервера. Пожалуйста, подождите, после чего повторите попытку.");
                }
            });
        });
    }
    
    getResult(lesson);
    $('#back-btn').click(getSite);
}


function drawLessons(){
    if (lessonsLoad > 0){
        setTimeout(drawLessons, 1000);
        return;
    }
    
    var li = $(this);
    
    if (li.attr('data-open') == '1'){
        li.attr('data-open', 0);
        li.find('li').remove();
        return;
    }
        
    var subject = li.attr('subject');
    
    selectedSubject = subject;
    
    if (!lessons[subject])
        return
        
    var selectLessons = lessons[subject];
    
    li.find('li').remove();
    
    for (var i in selectLessons){
        var lesson = selectLessons[i];
        
        var new_li = $(`<li>${lesson['title']}</li>`);
        
        new_li.on('click', function(){
            selectedLesson = $(this).index() - 1;
            
            var main = $('#main');
            var lesson = $(this);
            main.empty();
            main.append('<img src="static/images/load.gif" id="loading">');
            $.ajax({
                url: 'site/lesson',
                method: 'get',           
                dataType: 'html',
                success: function(data){ 
                    DrawLessonPage(data);
                },
                error: function(jqXHR, exception){
                    alert("Ошибка на стороне сервера. Пожалуйста, подождите, после чего повторите попытку.");
                }
            });
        });
        
        li.append(new_li);
        li.attr('data-open', 1);
    }
    
}



function drawSubjects(){
    $.ajax({
        url: '/subject/all',
        method: 'get',           
        dataType: 'json',
        success: function(data){ 
            subjects = data;
            
            //$('#main').html(data); 
            
            lessonsLoad = subjects.length;
            getLessons();
            
            var ul = $("<ul></ul>");
            for (var key in subjects){
                var subject = subjects[key];
                var li = $('<li class="subject"></li>');
                li.html(subject['title'] + ' <span>' + subject['description'] + '</span>');
                li.attr('subject', subject['title']);
                
                li.on('click', drawLessons);
                if (is_teacher && li.find('button').length == 0) {
                    var btn = $('<button>Добавить урок</button>');
                    li.append(btn);
                    btn.click(function(){
                        var createWindow = $('#create-new');
                        createWindow.find('h2').text('Создать новый урок');
                        var inputs = createWindow.find('.input-new');
                        inputs.empty();
                        inputs.append('<label for="title">Название *</label><input name="title">');
                        inputs.append('<label for="description">Описание</label><input name="description">');
                        
                        var select = $('<select name="subject"></select>');
                        
                        for (var i in subjects){
                            select.append(`<option value="${subjects[i]['title']}">${subjects[i]['title']}</option>`);
                        }
                        
                        inputs.append('<label for="subject">Предмет *</label>');
                        inputs.append(select);
                        
                        $('.background-create').show();
                        createWindow.show();
                        
                        createWindow.find('button').click(function() {
                            //Создаем новый урок на сервере
                            var title = createWindow.find('input[name="title"]').val();
                            var description = createWindow.find('input[name="description"]').val();
                            var subject = createWindow.find('select[name="subject"]').val();
                            
                            if (!title || !subject){
                                alert('Вы не заполнили одно из обязательных полей');
                                return;
                            }
                            $.ajax({
                                url: '/lesson/add',
                                method: 'post',           
                                dataType: 'json',
                                contentType: "application/json",
                                data: JSON.stringify({"title": title, "description": description, "subject_title": subject}), 
                                success: function(data){ 
                                    alert('Успешно');
                                    location.reload(); 
                                },
                                error: function(jqXHR, exception){
                                    alert('Что-то пошло не так\n');
                                }
                            })
                            
                            $('.background-create').hide();
                            createWindow.hide();
                        });
                        
                        $('.background-create').click(function(){
                            $('.background-create').hide();
                            createWindow.hide();
                        });
                        
                    });
                }
                ul.append(li);
            }
            
            if (is_teacher){
                var btn = $('<button>Добавить предмент</button>');
                $('#subjectsTable').append(btn);
                
                btn.click(function(){
                    var createWindow = $('#create-new');
                    createWindow.find('h2').text('Создать новый предмет');
                    var inputs = createWindow.find('.input-new');
                    inputs.empty();
                    inputs.append('<label for="title">Название *</label><input name="title">');
                    inputs.append('<label for="description">Описание</label><input name="description">');
                    
                    $('.background-create').show();
                    createWindow.show();
                    
                    createWindow.find('button').click(function() {
                        //Создаем новый предмет на сервере
                        var title = createWindow.find('input[name="title"]').val();
                        var description = createWindow.find('input[name="description"]').val();
                        
                        if (!title){
                            alert('Вы не заполнили одно из обязательных полей');
                            return;
                        }
                        $.ajax({
                            url: '/subject/add',
                            method: 'post',           
                            dataType: 'json',
                            contentType: "application/json",
                            data: JSON.stringify({"title": title, "description": description}), 
                            success: function(data){ 
                                alert('Успешно');
                                location.reload(); 
                            },
                            error: function(jqXHR, exception){
                                alert('Что-то пошло не так\n');
                            }
                        })
                        
                        $('.background-create').hide();
                        createWindow.hide();
                    });
                    
                    $('.background-create').click(function(){
                        $('.background-create').hide();
                        createWindow.hide();
                    });
                    
                });
            }
                
            $('#subjectsTable').append(ul);
        },
        error: function(jqXHR, exception){
            alert(jqXHR.responseText);
        }
    })
}



$.ajax({
    url: '/auth/users/me/',
    method: 'get',           
    dataType: 'json',
    success: function(data){ 
        user = data;
        var username = user['full_name'];
        
        if (user['is_teacher']){
            is_teacher = user['is_teacher'];
            username += ' (учитель)';
            
        }
            
        $('#user').text(username);
        $('#user').show();
    },
    error: function(jqXHR, exception){
        alert(jqXHR.responseText);
    }
})


drawSubjects();