var token=null ;
function getToken (){
    if (token==null){
        token= localStorage.getItem("cv_token")
    }
    return token;
}

jQuery(document).ready(function(){
	jQuery('.skillbar').each(function(){
		jQuery(this).find('.skillbar-bar').animate({
			width:jQuery(this).attr('data-percent')
		},6000);
	});

	$('#hideme').click(function() {
    	// Elegxos gia ta username, email, password
    	
    	$('.reg1').addClass('hidden')
    	$('.createprofile').removeClass('hidden')
    	$('.createprofile').addClass('nothidden')
	});


$('#edit_btn').click(function edit() {
    	$('.input_edit').addClass('makeVisible')
    	$('.info').addClass('makeHidden')
    	$('#edit_btn').html('Save')
    	
    	$('#edit_btn').click(function savechanges(){
    		var name = $("#name").val(); 
    		var surname = $('#surname').val();
    		var description = $('#description').val();
    		var birthdate = $('#birthdate').val();
    		var website = $('#website').val();
    		var address = $('#address').val();
    		var telephone =$('#telephone').val();
    		var token = localStorage.getItem("cv_token")
    		$.ajax ({
    			url:'/api/edit_profile',
    			data: 
    			{
    				name:name,
    				surname:surname,
    				description:description,
    				birthdate:birthdate,
    				website:website,
    				address:address,
    				telephone:telephone,
    				token:token 
    			},
    			method:'POST',
    			success:function(response){
    				var response = JSON.parse(response); 
    				console.log("Success")
                	window.location.href = response["profile_url"] + '?token=' + token; //pername san parametro kai to token
    			},
    			error: function(error){
    				console.log("Failed")
    			}
    		});
    	});


	});

    


    $("#drop-area").on('dragenter', function (e){
    e.preventDefault();
    $(this).css('background', '#BBD5B8');
    });

    $("#drop-area").on('dragover', function (e){
    e.preventDefault();
    });

    $("#drop-area").on('drop', function (e){
    $(this).css('background', '#D8F9D3');
    e.preventDefault();
    var image = e.originalEvent.dataTransfer.files;
    uploadImage(image);
    });

});

function uploadImage(image) {
    var data = new FormData();
    data.append('newimage', image[0]);
    data.append('token', getToken());
    $.ajax({
    url: "/api/changeImage",
    data: data,
    type:'POST',
    contentType:false,
    cache: false,
    processData: false,

    success: function(data){
        $('#drop-area').append(data);
        location.reload();

    }});
}

function viewUser(user_id){
    $.ajax({
        url:'/api/viewUser',
        data: 
        {
            user_id:user_id,
            token: getToken()
        },
        method:'POST',
        success:function(response){
            var response = JSON.parse(response); 
            window.location.href = response["profile_url"];
        }
    })
}

function deleteUser(user_id){
    console.log("deleting user ",user_id);
    $.ajax ({
        url:'/api/deleteuser',
        data: 
        {
            user_id:user_id,
            token: getToken()
        },
        method:'DELETE',
        success:function(response){
            location.reload();
        }
    })
}

var _user_id;
function createAccount(){
    $(".error_msg").text("")
    $.ajax ({
        url:'/api/register',
        data: $('form#account').serialize(),
        method:'POST',
        datatype:'json',
        success:function(response){
            response = JSON.parse(response);
            if(response.errors) {
                var errors = response.errors;
                for(var keyError in errors) {
                    $('div#'+keyError).append(errors[keyError]);
                }
            }
            else {
                console.log(response)
                _user_id=response['user_id']
                $('.reg1').addClass('hidden')
                $('.createprofile').removeClass('hidden')
                $('.createprofile').addClass('nothidden')
            }
        }
    })
}

function showWheather(){
        console.log("Weather")
        $('#weather').addClass('makeVisibleW')
        $('#weather').removeClass('makeHidden')
        $('#show_weather').html("Hide")
        $('#show_weather').click(function hideWeather(){
            console.log("HIDE ME")
            $('#weather').addClass('makeHidden')
            $('#weather').removeClass('makeVisibleW')
            $('#show_weather').html("Weather")
    });
}
    


function createProfile(){
    $(".error_msg").text("")
    // var data = $('form#profile').serializeArray()
    // data.push({"name": "user_id", "value" : _user_id});
    var name = $("input[name=name]").val(); 
    var surname = $('input[name=surname]').val();
    var description = $('input[name=description]').val();
    var birthdate = $('input[name=birthdate]').val();
    var website = $('input[name=website]').val();
    var address = $('input[name=address]').val();
    var telephone =$('input[name=telephone]').val();
    console.log(name);
    $.ajax ({
        url:'/api/createProfile',
        data: {
            name:name,
            surname:surname,
            description:description,
            birthdate:birthdate,
            website:website,
            address:address,
            telephone:telephone,
            user_id:_user_id
        },
        method:'POST',
        success:function(response){
            response = JSON.parse(response);
            if(response.errors) {
                var errors = response.errors;
                for(var keyError in errors) {
                    $('div#'+keyError).append(errors[keyError]);
                }
            }
            else {
                window.location.href = "/login";
            }
        }
    })
}

function login(){
        $(".error_msg").text("")
        var email =  $("input[name=email]").val(); 
        var password =  $("input[name=password]").val(); 
        //if(email == '')
        $.ajax({
            url: '/api/login',
            data: {email: email, password: password},
            method: 'POST',

            success: function(response) {
                var response = JSON.parse(response);
                 //json.dumps einai morfi arxeiou  opote prepei na ta kanw parse 
                if(Object.keys(response.errors).length> 0) {
                    var errors = response.errors;
                    for(var keyError in errors) {
                    $('div#'+keyError).append(errors[keyError]);
                    }
                }
                else {
                console.log(email ,password)
                var token = response["token"]
                localStorage.setItem("cv_token", token);
                window.location.href =response["profile_url"] + '?token=' + token; //pername san parametro kai to token
                }
            }
        })
    }

function sendMessageTo(user_id) 
{
   
    var message = $("#msg-inp-"+user_id).val();
    console.log("Message ",message);
    $.ajax({
        url:'api/sendMessage',
        data:
        {
            message:message,
            user_id:user_id,
            token: getToken()
        },
        method:'POST',
        success:function(response) {
            var response = JSON.parse(response); 
            console.log(response);
            location.reload();
        }
    }) 
}