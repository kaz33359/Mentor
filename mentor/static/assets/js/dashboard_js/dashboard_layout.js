$(function () {



// ------------------------------------------------------- //
  // Sidebar Functionality
  // ------------------------------------------------------ //
  $('.sidebar-toggle').on('click', function () {
      $(this).toggleClass('active');

      $('#sidebar').toggleClass('shrinked');
      $('.page-content').toggleClass('active');
      $(document).trigger('sidebarChanged');

      if ($('.sidebar-toggle').hasClass('active')) {
          $('.navbar-brand .brand-sm').addClass('visible');
          $('.navbar-brand .brand-big').removeClass('visible');
          $(this).find('i').attr('class', 'fa fa-long-arrow-right');
      } else {
          $('.navbar-brand .brand-sm').removeClass('visible');
          $('.navbar-brand .brand-big').addClass('visible');
          $(this).find('i').attr('class', 'fa fa-long-arrow-left');
      }
  });


  // ------------------------------------------------------- //
    // Footer
    // ------------------------------------------------------ //

    var pageContent = $('.page-content');

    $(document).on('sidebarChanged', function () {
        adjustFooter();
    });

    $(window).on('resize', function(){
        adjustFooter();
    })

    function adjustFooter() {
        var footerBlockHeight = $('.footer__block').outerHeight();
        pageContent.css('padding-bottom', footerBlockHeight + 'px');
    }

    // ------------------------------------------------------- //
    // Material Inputs
    // ------------------------------------------------------ //

    var materialInputs = $('input.input-material');

    // activate labels for prefilled values
    materialInputs.filter(function() { return $(this).val() !== ""; }).siblings('.label-material').addClass('active');

    // move label on focus
    materialInputs.on('focus', function () {
        $(this).siblings('.label-material').addClass('active');
    });

    // remove/keep label on blur
    materialInputs.on('blur', function () {
        $(this).siblings('.label-material').removeClass('active');

        if ($(this).val() !== '') {
            $(this).siblings('.label-material').addClass('active');
        } else {
            $(this).siblings('.label-material').removeClass('active');
        }
    });

});
