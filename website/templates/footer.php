{% load static %}

<div class="footer_top">
      <div class="row">
        <div class="col-lg-4 col-md-4 col-sm-4">
          <div class="footer_widget wow fadeInLeftBig">
          <h2>Navigation</h2>
            <ul class="tag_nav">
              <li><a href="{% url 'index' %}">Home</a></li>
              <li><a href="#">About</a></li>              
              <li><a href="{% url 'posts' %}">News and Columns</a></li>
              <li><a href="{% url 'products' %}">Science Items</a></li>
            </ul>
          </div>
        </div>
        <div class="col-lg-4 col-md-4 col-sm-4">
          <div class="footer_widget wow fadeInDown">
          <h2>Contact</h2>
            <ul class="tag_nav">
              <li><a href="{% url 'contact_form' %}">Inquiry</a></li>
            </ul>
          </div>
        </div>
        <div class="col-lg-4 col-md-4 col-sm-4">
          <div class="footer_widget wow fadeInRightBig">
          <h2>Policy</h2>
            <ul class="tag_nav">
              <li><a href="#">Policy</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="footer_bottom">
      <p class="copyright">Copyright &copy; 2021 ScienceTime</a></p>
    </div>
