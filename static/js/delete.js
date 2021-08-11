$(document).ready(function () {
    $(".delete_education_class").on('click',function() {
        var id=$(this).data("id")
        var token = '{{csrf_token}}';
        $.ajax({
            // headers: { "X-CSRFToken": token },
            type: 'GET',
            url: '/deleteeducation/'+id+'/',
            data: {
                'data':"None",
            },
            success: function (json) {
                window.location.reload(true);
            }
        })
    })
  });
  $(document).ready(function () {
      $(".delete_skills_class").on('click',function() {
          var id=$(this).data("id")
          var token = '{{csrf_token}}';
          $.ajax({
              type: 'GET',
              url : '/deleteskill/'+id+'/',
              data :{
                  'data': "None",
              },
              success: function (json) {
                  window.location.reload(true);
              }
          })
      })
  });
  $(document).ready(function () {
      $(".delete_hobbies_class").on('click',function() {
          var id=$(this).data("id")
          var token = '{{csrf_token}}';
          $.ajax({
              type: 'GET',
              url : '/deletehobbie/'+id+'/',
              data :{
                  'data': "None",
              },
              success: function (json) {
                  window.location.reload(true);
              }
          })
      })
  });
  $(document).ready(function () {
      $(".delete_experience_class").on('click',function() {
          var id=$(this).data("id")
          var token = '{{csrf_token}}';
          $.ajax({
              type: 'GET',
              url : '/deleteexperience/'+id+'/',
              data :{
                  'data': "None",
              },
              success: function (json) {
                  window.location.reload(true);
              }
          })
      })
  });
  $(document).ready(function () {
      $(".delete_worksamples_class").on('click',function() {
          var id=$(this).data("id")
          var token = '{{csrf_token}}';
          $.ajax({
              type: 'GET',
              url : '/deleteworksamples/'+id+'/',
              data :{
                  'data': "None",
              },
              success: function (json) {
                  window.location.reload(true);
              }
          })
      })
  });
  $(document).ready(function () {
      $(".delete_achievements_class").on('click',function() {
          var id=$(this).data("id")
          var token = '{{csrf_token}}';
          $.ajax({
              type: 'GET',
              url : '/deleteachievements/'+id+'/',
              data :{
                  'data': "None",
              },
              success: function (json) {
                  window.location.reload(true);
              }
          })
      })
  });
  $(document).ready(function () {
      $(".delete_certificate_class").on('click',function() {
          var id=$(this).data("id")
          var token = '{{csrf_token}}';
          $.ajax({
              type: 'GET',
              url : '/deletecertificate/'+id+'/',
              data :{
                  'data': "None",
              },
              success: function (json) {
                  window.location.reload(true);
              }
          })
      })
  });