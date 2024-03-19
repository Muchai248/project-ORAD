(function ($) {
    "use strict";

    // Function to close opened dropdowns
    function closeDropdowns() {
        var sidebar = $('#sidebar');
        var dropdowns = sidebar.find('.left-menu-dropdown');

        // Hide dropdowns
        dropdowns.css({
            'opacity': 0,
            'left': '0'
        });
    }

    /*----------------------------
     jQuery MeanMenu
    ------------------------------ */
    jQuery('nav#dropdown').meanmenu();

    /*----------------------------
     jQuery myTab
    ------------------------------ */
    $('#myTab a').on('click', function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

    $('#myTab3 a').on('click', function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

    $('#myTab4 a').on('click', function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

    $('#myTabedu1 a').on('click', function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

    $('#single-product-tab a').on('click', function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

    $('[data-toggle="tooltip"]').tooltip();

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
        // Close opened dropdowns when sidebar is closed
        if (!$('#sidebar').hasClass('active')) {
            closeDropdowns();
        }
    });

    // Collapse ibox function
    $('#sidebar ul li').on('click', function () {
        var button = $(this).find('i.fa.indicator-mn');
        button.toggleClass('fa-plus').toggleClass('fa-minus');
    });

    /*-----------------------------
     Menu Stick
    ---------------------------------*/
    $(".sicker-menu").sticky({topSpacing:0});

    $('#sidebarCollapse').on('click', function () {
        $("body").toggleClass("mini-navbar");
        SmoothlyMenu();
        // Close opened dropdowns when sidebar is closed
        if ($("body").hasClass("mini-navbar")) {
            closeDropdowns();
        }
    });

    $(document).on('click', '.header-right-menu .dropdown-menu', function (e) {
        e.stopPropagation();
    });

    /*----------------------------
     wow js active
    ------------------------------ */
    new WOW().init();

    /*----------------------------
     owl active
    ------------------------------ */
    $("#owl-demo").owlCarousel({
        autoPlay: false,
        slideSpeed:2000,
        pagination:false,
        navigation:true,
        items : 4,
        navigationText:["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
        itemsDesktop : [1199,4],
        itemsDesktopSmall : [980,3],
        itemsTablet: [768,2],
        itemsMobile : [479,1],
    });

    /*--------------------------
     scrollUp
    ---------------------------- */
    $.scrollUp({
        scrollText: '<i class="fa fa-angle-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    });

    /*--------------------------
     left-side nav
    ---------------------------- */
})(jQuery);

// new js for the 
// $(document).ready(function() {
//     $('#registerBtn').click(function() {
//         var formData = {
//             'fullname': $('#fullname').val(),
//             'email': $('#email').val(),
//             'password': $('#password').val(),
//             'confirm_password': $('#confirm_password').val(),
//         };

//         $.ajax({
//             type: 'POST',
//             url: '/signup/',  // Update with your actual endpoint URL
//             data: formData,
//             dataType: 'json',  // Expect JSON response
//             success: function(data) {
//                 console.log('Registration successful:', data);
//                 // Handle success response, e.g., redirect to login page
//                 window.location.href = '/login/'; // Example redirection to login page
//             },
//             error: function(xhr, textStatus, errorThrown) {
//                 console.log('Registration failed:', errorThrown);
//                 // Handle error response, e.g., display error message
//                 $('#error-message').text('Registration failed: ' + errorThrown);
//             }
//         });
//     });
// });

// function fetchData(endpoint) {
//     fetch(endpoint)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(data => {
//             console.log('Data:', data);
//             // Process data as needed
//         })
//         .catch(error => {
//             console.error('Error:', error.message);
//         });
// }

// // Get references to menu items
// var myFiles = document.getElementById('myFiles');
// var teamFolder = document.getElementById('teamFolder');
// var references = document.getElementById('references');
// var documents = document.getElementById('documents');

// // Add event listeners to menu items
// myFiles.addEventListener('click', function(event) {
//     event.preventDefault();
//     fetchData('/my-files-endpoint');
// });

// teamFolder.addEventListener('click', function(event) {
//     event.preventDefault();
//     fetchData('/team-folder-endpoint');
// });

// references.addEventListener('click', function(event) {
//     event.preventDefault();
//     fetchData('/references-endpoint');
// });

// documents.addEventListener('click', function(event) {
//     event.preventDefault();
//     fetchData('/documents-endpoint');
// });

// // Define a function to fetch and render documents
// document.addEventListener('DOMContentLoaded', function() {
//     fetchPosts();
// });

// function fetchAndRenderPosts() {
//     fetch('/api/posts/fetch/')
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(data => {
//             // Render posts in the UI
//             renderPosts(data);
//         })
//         .catch(error => {
//             console.error('Error:', error.message);
//         });
// }
// Define default data
// function fetchPosts() {
//     fetch('http://localhost:8000/fetch/')
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(data => {
//             if (data && data.length > 0) {
//                 renderPosts(data);
//             } else {
//                 console.log('No posts found.');
//             }
//         })
//         .catch(error => {
//             console.error('Error fetching posts:', error);
//         });
// }


