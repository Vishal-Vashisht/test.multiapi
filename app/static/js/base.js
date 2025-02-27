$(document).ready(function () {
    $("#Log-out-btn").click(function() {
      token = sessionStorage.getItem("access_token")
      if (token){
        sessionStorage.removeItem("access_token")
      }
      document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      window.location.href = '/'
      
    });
  });