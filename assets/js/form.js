function alert(type, message) {
  return `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      <strong>${message}</strong>
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
  `
}

function onReCaptchaCheck(response) {
  var data = {
    'g-recaptcha-response': $('#g-recaptcha-response').val()
  };

  $.ajax({
    type: 'post',
    url: 'https://api.johnogrady.ie/verify',
    headers: {
      'Access-Control-Request-Method':'POST',
      'Access-Control-Request-Headers': 'Content-Type, Accept',
    },
    dataType: 'json',
    crossDomain: "true",
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(data),
    success: function(data) {
      $(`:input[type="submit"]`).prop('disabled', false);
    },
    error: function(data) {
      alert('warning', $.parseJSON(data))
    }
  });
}

$(function(){

  $('#contact-form').submit(function(event) {

    event.preventDefault();

    var data = {
      name: $('#name').val(),
      email: $('#email').val(),
      subject: $('#subject').val(),
      message: $('#message').val()
    }

    $.ajax({
      type: 'post',
      url: 'https://api.johnogrady.ie/contact',
      headers: {
        'Access-Control-Request-Method':'POST',
        'Access-Control-Request-Headers': 'Content-Type, Accept',
      },
      dataType: 'json',
      crossDomain: "true",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify(data),
      success: function(data) {
        $('#form-output').html(alert('success', 'Thank you for your message.  I\'ll be in touch soon'));
      },
      error: function(data) {
        $('#form-output').html(alert('warning', 'There was an error sending your message.  Try again.'));
      }
    }).done(function (data) {
      $('#contact-form').trigger('reset');
      grecaptcha.reset()
    });
  });
});
