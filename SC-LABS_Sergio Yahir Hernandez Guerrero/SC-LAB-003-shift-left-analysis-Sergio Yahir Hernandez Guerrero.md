# SC-LAB-003 · Costo de Corrección y Shift Left

**Equipo / Integrantes:** _Ximena Becerril Olivares,Yadhira Anadanely Benitez Millan Pamela Espinoza Montiel Sergio Yahir Hernandez Guerrero_
**Fecha:** _21/09/2026_
**Pregunta guía:** ¿Qué cambia cuando un problema de seguridad se descubre en Requisitos, Desarrollo, Pruebas o Producción?

---

## 1. Idea central

Mientras más tarde se descubre un problema de seguridad, normalmente más artefactos (requisitos, diseño, código, pruebas, documentación), decisiones, despliegues y personas se ven afectados. En este análisis no se usan multiplicadores universales de costo: se describe de forma **cualitativa** qué hay que rehacer.

Dos conceptos que se mantienen separados a lo largo del documento:

- **Origen:** la etapa donde nació la omisión o el error.
- **Descubrimiento:** la etapa donde el problema se detecta.

**Shift Left** significa mover *ciertas* actividades de seguridad hacia etapas más tempranas, **no** hacer toda la seguridad al inicio. La seguridad debe mantenerse durante todo el ciclo de vida, incluida la operación.

---

## 2. Caso guiado · Recuperación de contraseña (RF-010)

> RF-010: «SecureCampus deberá permitir al usuario recuperar su contraseña». El enlace generado dura 7 días y puede reutilizarse varias veces.

| Pregunta | Respuesta del equipo |
| --- | --- |
| ¿Dónde se originó principalmente la omisión? | En **Requisitos**. RF-010 describe solo la función («recuperar contraseña») y no define condiciones de seguridad: cuánto debe durar el enlace, si es de un solo uso, cómo se genera o qué ocurre al usarlo. El diseño y el código simplemente implementaron lo que el requisito dejó abierto (7 días y reutilizable). |
| ¿Dónde podría descubrirse? | Idealmente en **Requisitos** (revisión de requisitos o modelado de amenazas) y en **Diseño** (revisión del flujo de recuperación). Si no, en **Desarrollo** (revisión de código o análisis estático), en **Pruebas** (pruebas de seguridad o pentest) o, en el peor caso, en **Producción** (cuenta comprometida o incidente reportado). |
| ¿Qué artefactos habría que cambiar si se descubre en pruebas? | Requisito RF-010 y sus criterios de aceptación; diseño del flujo y del modelo de datos del token (expiración, estado «usado», hash); código de generación, validación e invalidación del token; plantilla del correo; casos de prueba funcionales y de seguridad; pruebas de regresión; documentación y trazabilidad; y un nuevo ciclo de build y liberación. |
| ¿Qué requisitos/criterios de seguridad faltaron? | Expiración corta (por ejemplo 15 a 30 minutos); **un solo uso** (el enlace se invalida al usarse); invalidar enlaces anteriores al solicitar uno nuevo; token aleatorio generado con fuente criptográficamente segura y suficientemente largo; almacenar solo el hash del token; mensaje genérico que no revele si el correo existe (evita enumeración de usuarios); límite de intentos y de solicitudes (rate limiting); notificar al usuario por correo cuando cambia su contraseña; cerrar sesiones activas tras el cambio; aplicar la política de contraseñas a la nueva clave; registro de auditoría del proceso. |
| ¿Qué moverían a la izquierda? | Definir **criterios de aceptación de seguridad** dentro del propio requisito; hacer **modelado de amenazas / casos de abuso** («¿qué pasa si alguien obtiene el enlace?»); usar una lista de verificación de requisitos seguros (por ejemplo OWASP ASVS) durante la revisión de requisitos; y diseñar **pruebas negativas** (reutilizar un enlace, usar uno expirado) desde el diseño, antes de escribir código. |

---

## 3. Reto integral · tres situaciones

| Caso | Origen | Descubrimiento | Retrabajo/impacto | Actividad Shift Left | Control posterior |
| --- | --- | --- | --- | --- | --- |
| **A · Administrador** | **Requisitos.** El requisito habla de «consultar calificaciones» sin decir quién puede hacerlo ni bajo qué condiciones. No se analizó la separación de funciones: ver una calificación y cambiarla son capacidades con riesgos distintos. | **Tardío**: ocurre cuando alguien aclara al final que consultar y modificar necesitan permisos diferentes. Lo normal es que salga en pruebas de aceptación o en una validación con el área usuaria; pudo salir en la primera revisión del requisito. | Redefinir roles y actualizar historias de usuario y criterios de aceptación; cambiar las reglas de autorización en la API y en la interfaz (por ejemplo, ocultar o bloquear las acciones de edición); ajustar la base de datos y la asignación de permisos; crear pruebas por cada rol; actualizar manuales y capacitar a usuarios. Si ya estuviera en producción, habría que auditar qué cambios se hicieron con permisos indebidos. | Taller de revisión de requisitos con el área de negocio; historias de usuario con escenarios por rol («Dado un rol de solo lectura, cuando intenta modificar, entonces se rechaza»); modelado de amenazas centrado en escalada de privilegios y acceso a datos de otros usuarios; checklist de control de acceso (OWASP ASVS). | Pruebas automáticas de autorización por rol dentro del CI; bitácora de auditoría de quién consulta y quién modifica calificaciones; revisión periódica de qué usuarios tienen qué permisos; alertas ante modificaciones masivas o fuera de horario. |
| **B · Upload** | **Requisitos, arrastrado al Diseño.** Se pensó solo en «permitir subir archivos» y se asumió que un usuario autenticado es confiable. Nadie definió tipo, tamaño, nombre ni dónde se guarda. | Podría detectarse en la revisión del diseño o del modelado de amenazas; si no, con análisis estático, pruebas de penetración o incluso en producción (archivo malicioso, disco lleno, nombres de archivo que intentan salir de la carpeta). | Escribir el requisito completo; validar en el servidor el tipo real del archivo (no solo la extensión); guardar los archivos en un almacenamiento privado, fuera del alcance directo desde la web; generar nombres aleatorios; añadir límites de tamaño y análisis antimalware; manejar errores sin revelar detalles internos; probar con archivos maliciosos. En producción se suma revisar y purgar lo ya subido y revisar registros. | Criterios de aceptación concretos («solo PDF e imágenes, máximo X MB, nombre generado por el sistema, almacenamiento privado»); casos de abuso escritos desde el inicio (subir un script, un archivo gigante, un nombre con `../`); revisión de diseño antes de programar; reglas de análisis estático para detectar manejo inseguro de archivos. | Escaneo antimalware continuo; monitoreo del volumen y tamaño de las cargas con alertas por comportamiento anómalo; pruebas de penetración periódicas; política de retención y limpieza de archivos. |
| **C · Dependencia** | **Decisión de incorporar un componente externo sin gobierno de dependencias.** La biblioteca estaba limpia cuando se eligió; la falla es nueva y ajena al equipo. Lo que faltó fue un inventario y un responsable que vigilara ese componente. | **En operación**, unos 10 meses después de incorporarla (8 hasta que se publicó la falla + 2 sin que nadie la viera). El retraso no se debe a lo difícil de detectarla, sino a que **no había monitoreo**. | Encontrar dónde se usa la biblioteca (incluyendo dependencias indirectas); evaluar si la falla es realmente explotable en nuestro sistema; actualizar o reemplazar; hacer pruebas de regresión; liberar una corrección urgente; revisar registros de los 2 meses de exposición por si hubo explotación; comunicar a los responsables. | Inventario de componentes (SBOM); análisis de composición de software (SCA) en cada pull request; política de dependencias aprobadas; archivo de bloqueo de versiones; Dependabot activado desde el primer día; pruebas de regresión suficientes para actualizar sin miedo. | Alertas continuas de vulnerabilidades con un responsable asignado; tiempos máximos de corrección según severidad (una crítica se atiende en días, no en meses); revisión periódica y retiro de dependencias obsoletas; plan de respuesta a incidentes. |

---

## 4. Escalera de costo cualitativa · Caso B (Upload)

| Momento | ¿Qué habría que corregir/revisar? | Costo/retrabajo: Bajo/Medio/Alto + por qué |
| --- | --- | --- |
| **Requisitos** | Solo el texto del requisito y sus criterios de aceptación (tipos permitidos, tamaño, nombre, almacenamiento). | **Bajo.** No existe diseño ni código; se corrige un documento y participan pocas personas. |
| **Diseño** | Diagrama y decisiones de almacenamiento, flujo de carga, modelo de datos, componentes de validación. | **Bajo a Medio.** Hay que rehacer diseño y avisar al equipo, pero todavía no hay código construido. |
| **Desarrollo** | Implementar validaciones, renombrado, límites y almacenamiento seguro; ajustar el código ya escrito; pruebas unitarias. | **Medio.** Hay retrabajo de código y pruebas, aunque el alcance sigue acotado a pocos módulos. |
| **Pruebas** | Requisito, diseño y código; volver a ejecutar pruebas funcionales y de regresión; rehacer el plan de pruebas; posible retraso de la liberación. | **Alto.** Se toca casi todo lo anterior a la vez, se repiten ciclos de prueba y se afectan fechas y personas. |
| **Producción** | Todo lo anterior más despliegue de emergencia; revisar y limpiar archivos ya subidos; analizar si hubo abuso; comunicación a usuarios; posible incidente formal. | **Alto (el mayor).** Además del retrabajo técnico hay impacto en usuarios y datos reales, respuesta a incidentes y posible daño de reputación o incumplimiento normativo. |

> Nota: los niveles son cualitativos y orientativos. No representan multiplicadores fijos de costo.

---

## 5. Pregunta con truco conceptual · Dependencias

**¿Puede Shift Left ayudar con una vulnerabilidad que todavía no existía públicamente cuando desarrollamos?**

**Respuesta:** No puede **evitar** que esa vulnerabilidad exista ni detectarla en el momento del desarrollo, porque todavía no era conocida. Lo que sí puede hacer es **dejar preparado al equipo** para detectarla rápido y corregirla con poco esfuerzo cuando aparezca. Desde antes se puede preparar:

- **Inventario de dependencias (SBOM)**, para saber qué componentes y versiones usamos y dónde.
- **Análisis de composición de software (SCA)** integrado al pipeline de CI/CD, para revisar continuamente contra vulnerabilidades nuevas.
- **Alertas automáticas** (por ejemplo Dependabot y GitHub Security Advisories) y un responsable asignado para atenderlas.
- **Versiones fijadas y archivo de bloqueo**, para que las actualizaciones sean controladas y reproducibles.
- **Criterios para elegir dependencias**: bibliotecas mantenidas, con buena reputación, y solo las necesarias (menos dependencias significa menos superficie de ataque).
- **Pruebas de regresión automatizadas**, que permiten actualizar o reemplazar una biblioteca con confianza y rapidez.
- **Diseño que limite el impacto** (aislamiento, mínimo privilegio, capas de defensa) y que facilite reemplazar una biblioteca sin reescribir todo.
- **Proceso de gestión de parches y plan de respuesta a incidentes**, con tiempos objetivo según severidad.

En el Caso C, el problema no fue que la vulnerabilidad apareciera, sino que **nadie la vigiló durante 2 meses**. Esa parte sí se pudo haber preparado con anticipación.

---

## 6. Reflexión

**¿Shift Left elimina la necesidad de seguridad en operación?**
No. Shift Left mueve *algunas* actividades a etapas tempranas para reducir errores y retrabajo, pero no sustituye la seguridad continua. En operación siguen siendo necesarios el monitoreo, la gestión de vulnerabilidades y parches (como en el Caso C), el control de accesos, la configuración segura, los registros de auditoría y la respuesta a incidentes. Hay riesgos que solo aparecen después de liberar el sistema.

**¿Por qué una funcionalidad puede cumplir su requisito funcional y seguir siendo insegura?**
Porque un requisito funcional describe **qué debe hacer** el sistema, no **qué debe impedir**. Las pruebas funcionales suelen comprobar el camino esperado. En RF-010 la recuperación de contraseña funciona: envía el enlace y permite cambiar la clave. Aun así es insegura porque el enlace dura 7 días y se reutiliza. Lo mismo ocurre en el Caso B: el upload «funciona», pero acepta cualquier archivo. Por eso los requisitos deben incluir criterios de seguridad explícitos y pruebas negativas.

**¿Qué decisión de su equipo habría sido más barata de corregir antes?**
_(Borrador: adaptar a la experiencia real de su equipo.)_
Definir desde el inicio la **matriz de roles y permisos** (quién puede consultar y quién puede modificar). Corregirla en la etapa de requisitos habría costado solo actualizar un documento y sus criterios de aceptación. Descubrirla en pruebas implica cambiar el requisito, el diseño de autorización, el código de varios módulos y repetir las pruebas.

---

## 7. Conclusión

La diferencia clave entre **origen** y **descubrimiento** explica el costo: cuanto mayor es la distancia entre ambos, más artefactos y personas se ven afectados. Shift Left reduce esa distancia para los problemas que se pueden prevenir desde el diseño (requisitos incompletos, control de acceso, cargas de archivos), y prepara al equipo para los que no se pueden prevenir (nuevas vulnerabilidades en dependencias). Pero no reemplaza la seguridad continua en operación.
