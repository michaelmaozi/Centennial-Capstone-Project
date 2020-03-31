// refresh verification code
function refresh_captcha(event){
  $.get("/captcha/refresh/?"+Math.random(), function(result){
      $('#jsRefreshCode img.captcha').attr("src",result.image_url);
      $('#id_captcha_0').attr("value",result.key);
  });
  return false;
}

$('#jsRefreshCode img.captcha').on('click', function(){
  console.log('clicked');
  refresh_captcha();
});

// Send verification code to phone
$('#jsSendCode').on('click',function(){
  send_sms_code(this,$('#jsMobileTips'));
});

// send msg counting down ...
function show_send_sms(time){
  $('#jsSendCode').val(time+"seconds would send again");
  if(time<=0){
      clearTimeout(send_sms_time);
      $('#jsMobileTips').hide(500);
       $('#jsSendCode').val("sending...").removeAttr("disabled");
      return;
  }
  time--;
  send_sms_time = setTimeout("show_send_sms("+time+")", 1000);
}

function send_sms_code(sendBtn,tipsId){
  var $sendBtn = $(sendBtn),
      $tipsId = $(tipsId),
      $inpRegMobile = $("#jsRegMobile"),
      $inpRegCaptcha = $('#id_captcha_1'),
      verify = verifyDialogSubmit(
          [
              {id: '#jsRegMobile', tips: Dml.Msg.epPhone, errorTips: Dml.Msg.erPhone, regName: 'phone', require: true},
              {id: '#id_captcha_1', tips: Dml.Msg.epVerifyCode, errorTips: Dml.Msg.erVerifyCode, regName: 'verifyCode', require: true}
          ]
      );
  if(!verify){
      console.log("Not verify")
      return;
  }
  console.log("verified")
  $.ajax({
      cache: false,
      type: 'post',
      dataType:'json',
      url:"/send_sms/",
      data:{
          mobile:$inpRegMobile.val(),
          "captcha_1":$inpRegCaptcha.val(),
          "captcha_0":$('#id_captcha_0').val(),
      },
      async: true,
      beforeSend:function(XMLHttpRequest){
          $sendBtn.val("Sending...");
          $sendBtn.attr("disabled","disabled");
      },
      success: function(data){
          $sendBtn.removeAttr("disabled");
          $sendBtn.val("Code Sent");
          if(data.mobile){
              Dml.fun.showValidateError($inpRegMobile, data.mobile);
              refresh_captcha({"data":{"form_id":"jsRefreshCode"}});
          }else if(data.captcha){
              Dml.fun.showValidateError($inpRegCaptcha, data.captcha);
              refresh_captcha({"data":{"form_id":"jsRefreshCode"}});
          }else if(data.msg){
              Dml.fun.showValidateError($inpRegMobile, data.msg);
              $sendBtn.val("Resend...");
              refresh_captcha({"data":{"form_id":"jsRefreshCode"}});
          }else if(data.status == 'success'){
              Dml.fun.showErrorTips($tipsId, "Code sent");
              $sendBtn.attr("disabled","disabled");
              show_send_sms(60);
          }
      }
  });    
}

// generate Qrcode
$('#jsCreateQrCode').on('click',function(){
    var $username = $("#QRusername").val();
    var $password = $("#QRpassword").val();

    console.log($username);
    console.log($password);

    $.ajax({
        cache: false,
        type: 'post',
        dataType:'json',
        url:"/create_qrcode/",
        data:{
            username:$username,
            password:$password,
        },
      async: true,
      success: function(data){
        if ( data.status == 'success'){
            $(".QRimage").show();
            $(".QRsubmit").show();
            $("#jsCreateQrCode").hide();
            $("#QRcodeInput").show();

        }
      }
    })
});

// voice login
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;


$("#startToRecord").on('click', function(){
    $("#startToRecord").html("Recoding ...");
    let recognition = new window.SpeechRecognition();

    recognition.start();
    recognition.addEventListener('result', onSpeak);
    setTimeout(() => {
        recognition.stop();
        $("#startToRecord").html("Start Recording");
    }, 3000);
    
})

// Capture user speak
function onSpeak(e) {
  const msg = e.results[0][0].transcript;
  console.log(msg);
  writeMessage(msg)
}

// Write what user speaks
function writeMessage(msg) {
    $("#voice-secrect").val(msg);
}
 
