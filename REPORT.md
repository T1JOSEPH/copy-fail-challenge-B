# Reporte Técnico — CVE-2026-31431 Copy Fail

## El bug y dónde está

El bug está en `crypto/algif_aead.c` en la función `_aead_recvmsg()`. En 2017 alguien optimizó el código para que la fuente (src) y el destino (dst) de una operación criptográfica compartan el mismo bloque de memoria. Parecía razonable para ahorrar recursos, pero resultó ser un error grave que permite escribir datos controlados en el page cache del kernel.

## Por qué escribir en dst[assoclen + cryptlen] es peligroso

Ese offset cae dentro del page cache de `/usr/bin/su`. El page cache es donde el kernel guarda en RAM el contenido de los archivos para no leerlos del disco cada vez. Al escribir ahí, cambias lo que el kernel cree que dice el archivo sin tocar el disco. Es como editar la memoria del sistema sin dejar huella en el almacenamiento físico.

## Por qué el exploit es silencioso

Nunca toca el disco. Si revisas el archivo `/usr/bin/su` con un antivirus o calculas su hash SHA256, verás el archivo original sin cambios. El exploit solo modifica la versión en RAM. Cuando el sistema ejecuta `su`, lo carga desde el page cache ya corrompido y ejecuta el código del atacante. Completamente invisible desde el disco.

## Conexión con lo visto en clase

En clase vimos el page cache, chmod, el bit setuid y los inodos. Todo aparece aquí. El bit setuid en `/usr/bin/su` es lo que permite obtener root al ejecutarlo — el kernel lo ejecuta como root automáticamente. Los inodos no cambian porque el archivo en disco es el mismo. El page cache es exactamente el mecanismo que el exploit abusa para lograr todo sin dejar rastro.

## Lo que aprendí

Lo más interesante es que ninguna pieza individual es obviamente un error. Reutilizar memoria para optimizar es razonable. Permitir operaciones crypto a usuarios normales via AF_ALG tiene sentido. Usar splice() para conectar descriptores es útil. Pero combinando las tres cosas en el orden correcto, cualquier usuario puede obtener root. Esto me enseñó que en seguridad no basta revisar cada componente por separado — hay que pensar en cómo interactúan entre sí. Un cambio "razonable" de 2017 estuvo dormido 9 años antes de ser descubierto.
