window.onload = () => {
    const host = window.location.origin
    window.ui = SwaggerUIBundle({
      url: `${host}/doc/`,
      dom_id: '#swagger-ui',
    });
  };