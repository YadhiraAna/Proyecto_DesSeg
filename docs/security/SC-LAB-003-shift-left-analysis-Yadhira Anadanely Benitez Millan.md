# SC-LAB-003 · Análisis Shift Left

## Integrantes

* Ximena Becerrill Olivares
* Yadhira Anadanely Benitez Millan
* Pamela Espinoza Montiel
* Sergio Yahir Hernandez Guerrero

## Fecha

28 de septiembre de 2026

---

## Idea central del equipo

Un problema de seguridad es como una **gotera**: si se detecta cuando apenas se dibuja el plano, se corrige con un borrador; si se detecta cuando ya vivimos en la casa, hay que romper paredes, mover muebles y avisar a los vecinos. Shift Left **no significa** "hacer toda la seguridad al inicio", sino **hacer la pregunta correcta en el momento correcto** y seguir vigilando después.

---

## 3. Caso guiado · Recuperación de contraseña (RF-010)

> RF-010: «SecureCampus deberá permitir al usuario recuperar su contraseña». El enlace generado dura 7 días y puede reutilizarse varias veces.

| Pregunta | Respuesta del equipo |
|---|---|
| ¿Dónde se originó principalmente la omisión? | En **Requisitos**. Lo interesante es que no se "olvidó" nada: el requisito **sí dice** que dura 7 días y se reutiliza. O sea, el error no es un bug del código, es una **decisión mal pensada escrita en el requisito**. Nadie se preguntó "¿cómo abusaría de esto un atacante?". |
| ¿Dónde podría descubrirse? | En cualquier etapa, pero con distinta dificultad. En Requisitos/Diseño con una revisión de "casos de abuso"; en Desarrollo con revisión de código; en Pruebas solo si alguien prueba específicamente reutilizar el enlace; en Producción, cuando alguien ya robó una cuenta. Ojo: las pruebas funcionales normales **pasarían en verde** porque el sistema hace exactamente lo que pedía el requisito. |
| ¿Qué artefactos habría que cambiar si se descubre en pruebas? | El requisito RF-010, el diseño del flujo de recuperación, la tabla/modelo donde se guarda el token (agregar expiración y estado "usado"), el código que genera y valida el enlace, los casos de prueba, la documentación y el texto del correo enviado al usuario. Además hay que volver a probar y volver a desplegar. |
| ¿Qué requisitos/criterios de seguridad faltaron? | (1) El enlace debe expirar en poco tiempo (por ejemplo, 15 a 30 minutos). (2) El enlace debe ser de **un solo uso**. (3) El token debe ser aleatorio e impredecible. (4) Al pedir uno nuevo, el anterior se invalida. (5) Límite de intentos y solicitudes. (6) El mensaje al usuario no debe revelar si el correo existe. (7) Avisar por correo cuando la contraseña cambie. |
| ¿Qué moverían a la izquierda? | Una **sesión corta de "¿cómo lo abusaría?"** al escribir el requisito, y una lista de criterios de aceptación de seguridad. También agregar desde el inicio una prueba automática que intente usar el mismo enlace dos veces. |

---

## 4. Reto integral · tres situaciones

| Caso | Origen | Descubrimiento | Retrabajo/impacto | Actividad Shift Left | Control posterior |
|---|---|---|---|---|---|
| **A · Administrador** | Requisitos: se escribió "consultar calificaciones" sin decir **quién**, **cuándo** ni **bajo qué condiciones**. Además se mezclaron consultar y modificar como si fueran lo mismo. | Al final del proyecto, cuando se aclara que necesitan permisos distintos. | Hay que separar roles y permisos, cambiar el diseño de autorización, modificar endpoints y pantallas, repetir pruebas de acceso y revisar qué datos ya fueron vistos o cambiados por personas sin autorización. | Definir una **matriz de roles y permisos** al escribir requisitos (rol, acción, condición). Cada requisito de acceso debe decir quién sí y quién no. | Pruebas de autorización automatizadas, registros de auditoría (quién consultó/modificó qué) y revisión periódica de permisos. |
| **B · Upload** | Requisitos y Diseño: se aceptan archivos sin definir tipo, tamaño, nombre ni dónde se guardan. | Idealmente en revisión de requisitos; en el peor caso en Producción, cuando alguien sube un archivo malicioso o llena el disco. | Cambiar el diseño de almacenamiento, agregar validaciones, renombrar archivos, mover archivos fuera de la carpeta pública, agregar escaneo de malware, actualizar pruebas y migrar los archivos ya subidos. | Definir **reglas de subida** desde el requisito: tipos permitidos, tamaño máximo, nombre generado por el sistema, almacenamiento aislado y sin ejecución. | Escaneo antivirus, límites de espacio, monitoreo de subidas raras y pruebas periódicas con archivos "trampa". |
| **C · Dependencia** | Ninguno de los errores fue del equipo al inicio: la biblioteca estaba limpia. El fallo de proceso fue **no tener quién vigilara** las dependencias después. | 8 meses después se publica la vulnerabilidad y **pasan 2 meses más** sin que nadie la detecte. | Identificar dónde se usa la biblioteca, actualizarla, probar que nada se rompa, redesplegar y revisar si hubo explotación durante esos 2 meses de exposición. | Llevar un **inventario de dependencias** (SBOM), fijar versiones, activar escaneo automático en el pipeline y asignar un responsable. | Alertas automáticas de nuevas vulnerabilidades, revisión periódica, plan de actualización urgente y monitoreo en producción. |

---

## 5. Escalera de costo cualitativa

**Caso elegido: RF-010 · Recuperación de contraseña**

| Momento | ¿Qué habría que corregir/revisar? | Costo/retrabajo: Bajo/Medio/Alto + por qué |
|---|---|---|
| **Requisitos** | Solo el texto del requisito: cambiar "7 días y reutilizable" por "15 minutos y un solo uso", y agregar criterios de aceptación. | **Bajo.** Es cambiar una línea. Todavía no hay diseño, código ni pruebas que dependan de eso. |
| **Diseño** | El diagrama del flujo de recuperación y el modelo de datos del token (agregar expiración y estado). | **Bajo.** Se ajustan diagramas y decisiones; aún no hay código escrito que rehacer. |
| **Desarrollo** | El código que genera y valida el token, la base de datos, las validaciones y las pruebas unitarias que ya se escribieron con el comportamiento incorrecto. | **Medio.** Hay código y pruebas que corregir, pero el equipo tiene el contexto fresco y todavía nada está en manos de usuarios. |
| **Pruebas** | Requisito, diseño, código, base de datos, casos de prueba, documentación y correos; además repetir pruebas de regresión. | **Medio-Alto → se marca Alto.** Hay que tocar muchos artefactos a la vez y se retrasa la entrega. Además, las pruebas pudieron "pasar" con el comportamiento incorrecto porque era lo que pedía el requisito. |
| **Producción** | Todo lo anterior, más: redesplegar, invalidar todos los enlaces ya emitidos, revisar bitácoras por posibles cuentas robadas, avisar a usuarios afectados, atender soporte y posible daño a la confianza. | **Alto.** Ya hay usuarios y datos involucrados; el problema deja de ser solo técnico y se vuelve operativo y de reputación. |

> Nota: no usamos multiplicadores de costo (como "10x" o "100x"), porque no son universales. Lo que sí es consistente es que **entre más tarde, más cosas y más personas se ven afectadas**.

---

## 6. Pregunta con truco conceptual · Dependencias

**¿Puede Shift Left ayudar con una vulnerabilidad que todavía no existía públicamente cuando desarrollamos?**

**Respuesta:** No puede *evitar* que la vulnerabilidad aparezca, porque nadie puede prevenir algo que aún no se descubre. Pero **sí puede preparar al equipo para reaccionar rápido y con menos daño**. Es como no poder evitar que llueva, pero sí tener paraguas, techo revisado y saber dónde están las goteras.

Lo que sí se puede preparar desde antes:

* **Inventario de dependencias (SBOM):** saber qué bibliotecas usamos y en qué versión, para no buscar a ciegas cuando salga el aviso.
* **Escaneo automático continuo** en el pipeline (no solo una vez al agregar la biblioteca).
* **Versiones fijas y archivos lock**, para saber exactamente qué se desplegó.
* **Usar menos dependencias**: menos bibliotecas, menos puertas de entrada.
* **Responsable asignado y política de actualización** (por ejemplo, críticas en X días).
* **Pruebas automáticas sólidas**, para poder actualizar rápido sin miedo a romper todo.
* **Pipeline de despliegue ágil**, para poder redesplegar el mismo día.
* **Plan de respuesta a incidentes** y monitoreo en producción.

Esto conecta con el **Caso C**: el problema de esos 2 meses no fue técnico, fue que **nadie estaba mirando**.

---

## 7. Reflexión

**¿Shift Left elimina la necesidad de seguridad en operación?**

No. Shift Left mueve *algunas* actividades hacia antes, pero la seguridad debe mantenerse durante todo el ciclo. Hay cosas que solo aparecen en operación: nuevas vulnerabilidades (como el Caso C), configuraciones incorrectas, ataques reales y comportamiento inesperado de usuarios. Shift Left reduce los problemas; no sustituye el monitoreo ni la respuesta a incidentes.

**¿Por qué una funcionalidad puede cumplir su requisito funcional y seguir siendo insegura?**

Porque el requisito funcional dice **qué debe hacer** el sistema, no **qué no debe permitir**. En RF-010 el sistema recupera contraseñas correctamente, pero el enlace dura 7 días y se puede reutilizar. Todo funciona "como se pidió" y aun así es inseguro. Por eso hacen falta requisitos y criterios de seguridad, no solo funcionales.

**¿Qué decisión de su equipo habría sido más barata de corregir antes?**

Definir desde el inicio los **criterios de aceptación de seguridad** de los requisitos (expiración, un solo uso, permisos por rol, reglas de archivos). Escribir esas condiciones cuesta minutos al redactar el requisito; corregirlas ya en pruebas o producción implica rehacer diseño, código, pruebas y despliegue.

---

## Flujo de evidencia seguido

1. `git status`
2. `git diff`
3. `git add docs/security/SC-LAB-003-shift-left-analysis.md`
4. `git diff --staged`
5. `git commit -m "docs: agrega análisis Shift Left SC-LAB-003"`
6. `git push`
7. Verificar el archivo en GitHub