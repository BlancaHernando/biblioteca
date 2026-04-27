# Dailys del proyecto 📅

---

### 07/04/2026
- **¿Qué hicimos?** Nos descargamos el proyecto y lo abrimos por primera vez en PyCharm. A continuación leimos las explicaciones para entender qué había que hacer.
- **¿Algún problema?** A algunas integrantes del grupo no les permite conectar github con pycharm, ni si quiere unirse como colaboradoras en el proyecto. 

---

### 08/04/2026
- **¿Qué hice?** Leimos mas detalladamente el proyecto. Vimos que habia una serie de pasos los cuales decidimos ir siguiendo, empezando por el punto de Aprobado. Asimismo, tambien vimos que leía de un CSV en cada petición, lo cual era ineficiente.
- **¿Algún problema?** No entendiamos muy bien por donde empezar. 

---

### 08/04/2026
- **¿Qué hice?** En primer lugar, añadimos las librerias que necesitamos en el fichero requirements.txt. Además, creamos un nuevo fichero llamado database.py, esto crea y configura la conexión a la base de datos.

- **¿Algún problema?** Nos faltó poner los imports por lo que nos daba error y nos decía que create_engine, no estaba definido. 

---

### 08/04/2026
- **¿Qué hice?** A continuación, creamos un nuevo fichero, que llamamos models.py, aquí definimos las tablas de las bases de datos como clases. Creando las clases: libro, usuario, prestamo.
- **¿Algún problema?** nos dio error porque no teniamos sqalchemy instalado, para solucionarlo, unicamente hicimos pip.install sqalchemy en la terminal y con esto lo solucionamos. 

---

### 09/04/2026
- **¿Qué hice?** modificamos el server.py para que use la base de datos. 
- **¿Algún problema?** nos daba error porque no habiamos instalado FastApi ni tampoco Pandas, de nuevo realizamos un pip.install en la terminal y de esta manera lo solucionamos. Ademas, otro de los errores fue que la puerta 8000 ya la habiamos usado anteriormente y no sabiamos que cada programa usa una diferente para no pisarse con los demás. 

---

### 10/04/2026
- **¿Qué hice?** Ahora creamos dentro de fastapi , un nuevo fichero llamado test para ver si estos funcionaban. 
- **¿Algún problema?** Tambien, nos volvio a dar un error porque en este caso pytest no estaba instalado, por lo que de nuevo lo instalamos en la terminal. Además cometimos el error de darle directamente al play verde lo que hacia que nos diesen errores continuamente. 

---

### 10/04/2026
- **¿Qué hice?** realizamos los commits para guardar todos los ficheros nuevos que habiamos creado para completar el nivel aprobado y los cambios realizados. 
- **¿Algún problema?** No tuvimos ningun problema

---

### 15/04/2026
- **¿Qué hice?** Una vez completamos el nivel aprobado, pasamos al nivel notable. Primero, comenzamos por las excepciones personalizadas, para ello, creamos un fichero nuevo llamado exceptions.py dentro de fastapi. 
- **¿Algún problema?** cometiamos el error de ejecutarlo cuando aun no habiamos acabado, por lo tanto nos daba error y pensabamos que todo estaba mal.
---

### 15/04/2026
- **¿Qué hice?** Después, dentro de exceptions, definimos 4 clases de error: LibroNoEncontrado, LibroNoDisponible, UsuarioNoEncontrado y EmailDuplicado. A continuación, creamos una carpeta nueva llamada routers, dentro creamos a su vez 4 ficheros diferentes (init, libros, prestamos, usuarios) 
- **¿Algún problema?** no

---
### 15/04/2026
- **¿Qué hice?** Creamos los routers porque queríamos tener el código más ordenado, separando cada grupo de endpoints en su propio fichero en vez de tenerlos todos mezclados.
- **¿Algún problema?** no
---
### 16/04/2026
- **¿Qué hice?** Ahora pasamos al segundo punto de notable que eran los loggings. Modificamos el fichero server.py. Añadimos en cada router al principio logger= logging... y fuimos poniendo mensajes dentro de cada función.  (logger.info, logger.warning y logger.error). Movimos todos los endpoints que estaban en server.py a su fichero correspondiente.
- **¿Algún problema?** tuvimos algunos problemas, por un lado la version de fastapi, no nos funcionaba y tuvimos que utilizar lifespan y por otro lado, se nos olvido crear el fichero de init.py y nos daba todo error. Además, se nos olvidó separar los modelos PYDANTIC que estaban menzclados en el fichero server.py por ello, tuvimos que crear otro fichero llamado schemas para tenerlo todo mucho mas ordenado. 
---
### 18/04/2026
- **¿Qué hice?** Finalmente, para acabar el nivel notable, nos pedian mejorar el rendimiento. Las páginas 1_List_Books.py y 3_Usuarios.py muestran listas de datos que vienen de la API, por eso les pusimos caché. 
- **¿Algún problema?** no 
---
### 20/04/2026
- **¿Qué hice?** Ahora pasamos al nivel sobresaliente. El primer punto era utilizar decoradores propios. Por lo tanto, en primer lugar, creamos dentro de fastapi un nuevo fichero llamado decorators.py. Dentro, definimos un decorador llamado log.tiempo que basicamente mide cuanto tarda en ejecutarse cada función y lo va anotando en log. Lo pusimos encima de los endpoints de libros para que cada vez que alguien pida los libros, se anote cuánto ha tardado.
- **¿Algún problema?** En un principio, no sabiamos lo que eran los decoradores.
---
### 22/04/2026
- **¿Qué hice?** Seguimos con los properties y generadores. Para ello, de nuevo, creamos un nuevo fichero, services.py, dentro de fastapi. Después creamos una clase (dentro de services.py) llamada libroservice, con tres cosas. Por un lado con property, creamos, disponible y no disponible. Por otro lado, usamos yield (otro de los puntos requeridos). De esta forma, nos devolvia los libros de dos en dos, poco a poco, en vez de cargarlos todos a la vez. Esto es mucho mas eficiente, especialmente cuando tenemos muchos datos. 
- **¿Algún problema?** no teniamos nidea de como funcionaba el yield, ni donde implementarlo. 
---
### 24/04/2026
- **¿Qué hice?** Para acabar ya con la parte de sobresaliente, fuimos al punto de context manager, donde se nos pedia usar un with. Para ello, añadimos dentro de database.py, una funcion nueva llamada get_bd. Gracias a ella, podemos usar with para abrir la base de datos y cuando termina, se cierra automaticamente. Concretamente esto, lo usamos en server.py cuando la app empieza a funcionar y carga los libros del CSV.
- **¿Algún problema?** no
---