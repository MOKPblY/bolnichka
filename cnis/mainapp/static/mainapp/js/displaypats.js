$(document).ready(function () {

          $('#docslist input[type="checkbox"]').click(function (evt) {
              var doc_id = $(this).attr('id');
              var pats_to_inv = $('tbody ul li').filter(function() {
                return $(this).hasClass(doc_id);
              });
              $(pats_to_inv).toggleClass('invisible');


              return true;
          });

      });