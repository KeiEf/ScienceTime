{% load static %}

          <!-- Bootstrap core JavaScript -->
          <script src="{% static 'website/jquery/jquery.min.js' %}"></script>
          <script src="{% static 'website/bootstrap/js/bootstrap.bundle.min.js' %}"></script>
          <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>
      
          <!-- Additional Scripts -->
          <script src="{% static 'website/js/custom.js' %}"></script>
          <script src="{% static 'website/js/owl.js' %}"></script>
          <script src="{% static 'website/js/slick.js' %}"></script>
          <script src="{% static 'website/js/isotope.js' %}"></script>
          <script src="{% static 'website/js/accordions.js' %}"></script>
          <script src="{% static 'website/js/jquery.min.js' %}"></script> 
          <script src="{% static 'website/js/wow.min.js' %}"></script> 
          <script src="{% static 'website/js/bootstrap.min.js' %}"></script> 
          <script src="{% static 'website/js/slick.min.js' %}"></script> 
          <script src="{% static 'website/js/jquery.li-scroller.1.0.js' %}"></script> 
          <script src="{% static 'website/js/jquery.newsTicker.min.js' %}"></script> 
          <script src="{% static 'website/js/jquery.fancybox.pack.js' %}"></script> 

      
          <script language = "text/Javascript"> 
            cleared[0] = cleared[1] = cleared[2] = 0; //set a cleared flag for each field
            function clearField(t){                   //declaring the array outside of the
            if(! cleared[t.id]){                      // function makes it static and global
                cleared[t.id] = 1;  // you could use true and false, but that's more typing
                t.value='';         // with more chance of typos
                t.style.color='#fff';
                }
            }
          </script>