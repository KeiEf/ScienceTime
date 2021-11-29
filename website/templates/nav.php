<nav class="navbar navbar-expand-lg">
    <div class="container">
      <a class="navbar-brand" href="{% url 'index' %}"><h2><i>ScienceTime</i></h2></a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarResponsive">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <a class="nav-link" href="{% url 'index' %}">Home
              <span class="sr-only">(current)</span>
            </a>
          </li> 
          <li class="nav-item">
            <a class="nav-link" href="{% url 'posts' %}">ニュース & コラム</a>
          </li>
          <!--Merch-->
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
               サイエンスグッズ
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
              <li><a class="dropdown-item" href="{% url 'products' %}">全ジャンル</a></li>
              <li><a class="dropdown-item" href="{% url 'genre' 'fashion' %}">ファッション</a></li>              
              <li><a class="dropdown-item" href="{% url 'genre' 'toy' %}">おもちゃ</a></li>
              <li><a class="dropdown-item" href="{% url 'genre' 'merch' %}">雑貨 他</a></li>
            </ul>
          </li>

          <li class="nav-item">
            <a class="nav-link" href="#">レクチャー</a>
          </li>

          <li class="nav-item">
            <a class="nav-link" href="https://afterschoolbbs.herokuapp.com/" target="_blank">掲示板</a>
          </li>

        </ul>
      </div>
    </div>
  </nav>