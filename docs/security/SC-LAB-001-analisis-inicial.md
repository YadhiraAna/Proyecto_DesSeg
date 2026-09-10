# SC-LAB-001  
## INTEGRANTES
- Ximena Becerrill Olivares
- Yadhira Anadanely Benitez Millan
- Pamela Espinoza Montiel
- Sergio Yahir Hernandez Guerrero
##  Fecha
10 de septiembre de 2026
1. **¿Una amenaza y una vulnerabilidad son lo mismo? Explica con un ejemplo de SecureCampus.** Una amenaza y una vulnerabilidad no son lo mismo, ya que la amenaza es la persona o situación que podría causar el problema, mientras que la vulnerabilidad es el hueco que hace posible que ese problema realmente pase, por ejemplo en SecureCampus la amenaza sería un estudiante que por curiosidad cambia el número en la dirección web de su perfil para ver el de alguien más, y la vulnerabilidad sería que el sistema no revisa si ese perfil en verdad le pertenece antes de mostrárselo, porque aunque alguien quiera hacerlo, si el sistema estuviera bien hecho no lograría nada.
2. **¿Puede existir una vulnerabilidad aunque todavía nadie la haya explotado?**
Sí puede existir una vulnerabilidad aunque nadie la haya explotado todavía, ya que si los documentos se pueden descargar sin que el sistema revise si son tuyos, ese problema existe desde que se hizo esa parte del sistema, aunque nadie lo haya usado para ver algo que no le corresponde, porque el riesgo está ahí desde antes de que alguien lo aproveche.
3. **¿Un usuario autenticado está automáticamente autorizado para cualquier recurso?**
No está automáticamente autorizado para cualquier recurso, ya que una cosa es que el sistema sepa quién eres porque iniciaste sesión, y otra muy distinta es que te deje ver o hacer lo que sea, así que aunque María sí entró bien a su cuenta, eso no significa que deba poder ver la información de otro estudiante solo por cambiar un número en la dirección. 
4. **¿Qué control de los propuestos debería definirse desde requisitos o diseño?**
¿Por qué? Revisar que cada cosa que alguien pide en verdad le pertenezca antes de mostrársela, porque si esto se deja para el final hay que ir revisando parte por parte del sistema para agregarlo y es fácil que se les pase alguna, mientras que si se piensa desde el diseño queda como una regla que se aplica en todos lados desde el principio. 
5. **¿Qué activo consideran más crítico y por qué?**
El activo que consideramos más crítico es la información personal de los estudiantes, como sus perfiles y documentos, ya que es la más fácil de exponer según lo que vimos en los ejemplos, y porque si se filtra afecta la confianza de la gente en el sistema y hasta podría traer problemas legales para la escuela.

## Matriz
 
| Elemento       | Respuesta del equipo | Justificación |
|----------------|----------------------|---------------|
| **Activo**     | Información de perfiles de estudiantes (datos personales, académicos). | Es el recurso con valor que debe protegerse: identidad y datos sensibles de cada alumno. |
| **Amenaza**    | Usuario malintencionado que intenta acceder a información de otros estudiantes. | El actor aprovecha debilidades del sistema para obtener datos que no le corresponden. |
| **Vulnerabilidad** | Falta de validación de permisos en el acceso a perfiles (Insecure Direct Object Reference). | El sistema permite consultar cualquier perfil cambiando el identificador en la URL, sin verificar si el usuario tiene autorización. |
| **Ataque**     | Manipulación de la URL para acceder a perfiles ajenos. | Acción concreta: María cambia `/perfil/125` por `/perfil/126` y obtiene información de otro estudiante. |
| **Impacto**    | Exposición de datos personales y académicos de estudiantes. | Se compromete la confidencialidad y privacidad, lo que puede generar problemas legales y reputacionales. |
| **Riesgo**     | Alto: probabilidad elevada de explotación y consecuencias críticas. | La vulnerabilidad es fácil de explotar y el impacto es severo (violación de datos). |
| **Control**    | Validación de permisos en cada consulta, uso de tokens de sesión, pruebas de seguridad (OWASP). | Medidas que previenen el acceso indebido: verificar que el usuario autenticado solo pueda ver su propio perfil. |
