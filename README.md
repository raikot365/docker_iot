#  Tema claro y oscuro

Se realiza la implementación, mediante una opción desplegable, de la selección del tema (claro y oscuro) en la barra de navegación superior para que sea accesible en todas las páginas del sitio. Es accesible solo para usuarios que iniciaron sesión. El tema por defecto es el claro.

Para la implementación se utilizó el atributo "data-bs-theme" que permite cambiar los modos en el elemento <html> de manera global o en un componente y elemento especifico ([Documentación de Bootstrap](https://getbootstrap.com/docs/5.3/customize/color-modes/)). En ese caso se utilizó el atributo dentro de la etiqueta <body data-bs-theme="ligth or dark">, donde se realizó una lógica con jinja para seleccionar el tema.

Dentro del archivo layout.html, desde donde extienden las demas vistas, se implementó un menú desplegable dentro del <nav>, donde estan presentes las opciones "claro" y "oscuro". Cada una de estas funciones llama a la función *change_theme(tema)* mediante el evento onclick, pasando como parámetro el tema conrrespondiente. Esta función tiene una clausula, donde si el tema seleccionado es el actual, la función retorna sin hacer nada. Por el contrario, si es distinto se aplica el cambio y se hace un fetch a la ruta "change_theme", la cual actualiza el tema en la variable correspondiente a la sesión.
