# Reporte Técnico — CVE-2026-31431 Copy Fail

## ¿Cuál es el bug y dónde está?

El bug está en el archivo `crypto/algif_aead.c`, específicamente en la función `_aead_recvmsg()`. Lo que pasa es que en 2017 alguien optimizó el código para que la fuente y el destino de una operación criptográfica sean el mismo bloque de memoria. En ese momento parecía una buena idea para ahorrar recursos, pero resultó ser un error grave porque permite escribir datos controlados en lugares donde no deberías poder escribir.

## ¿Por qué es peligroso escribir en dst[assoclen + cryptlen]?

Ese offset específico cae dentro del page cache de `/usr/bin/su`. El page cache es básicamente donde el kernel guarda en RAM el contenido de los archivos para no tener que leerlos del disco cada vez. Cuando escribes ahí, estás cambiando lo que el kernel cree que dice el archivo, sin tocar el disco para nada. Es como cambiar las notas del profesor en su memoria sin tocar el cuaderno físico.

## ¿Por qué el exploit es "silencioso"?

Porque nunca toca el disco. Si alguien revisa el archivo `/usr/bin/su` con un antivirus o calcula su hash, va a ver el archivo original sin ningún cambio. El exploit solo modifica la versión en RAM. Cuando el sistema ejecuta `su`, lo carga desde el page cache ya corrompido, y ahí es donde ejecuta el código del atacante. Literalmente invisible desde el disco.

## Conexión con lo que vimos en clase

En clase hablamos del page cache, de cómo funciona chmod, del bit setuid y de los inodos. Todo eso aparece aquí. El bit setuid en `/usr/bin/su` es lo que hace que ejecutarlo te dé privilegios de root. Los inodos no cambian porque el archivo en disco es el mismo. Y el page cache es exactamente el mecanismo que el exploit abusa para lograr todo esto sin dejar rastro.

## ¿Qué aprendí?

Lo que más me llamó la atención es que ninguna de las piezas individuales es obviamente un error. Alguien reutilizó memoria para optimizar — razonable. AF_ALG permite operaciones crypto a usuarios normales — tiene sentido. splice() conecta descriptores de archivos — útil. Pero cuando combinas las tres cosas en el orden correcto, cualquier usuario puede obtener root. Eso me enseñó que en seguridad no basta con revisar cada cosa por separado, hay que pensar en cómo interactúan entre sí.
