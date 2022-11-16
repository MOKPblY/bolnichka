$(document).ready(function () {

          $('table ul li a').click(function (evt) {
              evt.preventDefault();
              // создаем AJAX-вызов
              $.ajax({
                  type: "GET",
                  data: {}, // данные не нужны, отправим по ссылке
                  url: $(this).attr('href'),
                  // если успешно, то
                  success: function (pat_info) {
                      console.log(pat_info)
                      $('#details h3').text(pat_info.fio)
                      $('#ds').text(pat_info.diag)
                      $('#oper').text(pat_info.oper)
                      $('#op_date').text(pat_info.op_date)

                  },
                  // если ошибка, то
                  error: function (response) {
                      // предупредим об ошибке
                      console.log(response.responseJSON.errors)
                  }
              });
              return false;
          });

      });