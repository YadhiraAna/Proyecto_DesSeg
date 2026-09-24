# SC-LAB-002

## Integrantes
- Ximena Becerrill Olivares  
- Yadhira Anadanely Benitez Millan  
- Pamela Espinoza Montiel  
- Sergio Yahir Hernandez Guerrero  

## Fecha
15 de septiembre de 2026  

---

## Caso
Un estudiante autenticado puede cambiar `/calificaciones/125` por `/calificaciones/126` y consultar calificaciones ajenas.

---

## Análisis por Fase

| Fase                 | ¿Qué debería hacerse? | Control / evidencia |
|------------------------|------------------------|---------------------|
| **Requisitos**         | Definir requerimientos negativos centrados en la opacidad de los identificadores de recursos públicos desde el inicio (exigir el uso de UUIDs o hashes en lugar de IDs secuenciales) para prevenir la enumeración horizontal. | Historias de usuario con criterios de aceptación explícitos sobre el aislamiento de datos y contratos de API (OpenAPI) libres de identificadores autoincrementables expuestos. |
| **Diseño**             | Establecer un patrón arquitectónico de autorización centralizada (ej. Policy-as-Code con OPA o un proxy de control a nivel de capa de datos) que desvincule la validación de propiedad del recurso de la lógica de negocio del controlador. | Diagrama de arquitectura y secuencia que ilustra la validación obligatoria del contexto de sesión frente al recurso solicitado antes de la persistencia. |
| **Desarrollo**         | Implementar referencias indirectas seguras (como Hashids) combinadas con middleware global de control de acceso, evitando delegar la validación de pertenencia a comprobaciones manuales y dispersas en el código. | Commit en GitHub con la implementación del filtro de autorización genérico y pruebas unitarias de aislamiento multi-usuario (Broken Object Level Authorization). |
| **Pruebas**            | Automatizar la detección de fallas de control de acceso mediante análisis estático de código (SAST con reglas personalizadas en Semgrep) enfocadas en rutas con parámetros dinámicos sin decoradores de seguridad. | Reporte automatizado en GitHub Actions de la ejecución de análisis estático y pruebas de integración orientadas a la mutación de parámetros de ruta. |
| **Despliegue**         | Configurar la pasarela de API (API Gateway) para aplicar políticas estrictas de inspección de claims en tokens JWT y reglas de limitación de tasa (Rate Limiting) orientadas a bloquear escaneos de endpoints. | Manifiesto o archivo de configuración versionado del API Gateway (ej. Kong/Nginx) y bitácora del pipeline de despliegue automatizado. |
| **Operación/Mantenimiento** | Implementar telemetría conductual y detección de anomalías basada en el análisis de ventanas deslizantes de acceso para identificar patrones automatizados de fuerza bruta o escaneo de IDs contiguos. | Dashboard de monitoreo de seguridad y reporte de incidentes simulados por patrones de consulta anómalos versionado en el repositorio. |

---

# Reto por equipo

## 1. Análisis de Escenarios (Controles Tempranos y Posteriores)

Analicen los cuatro escenarios. Para cada uno, propongan al menos un control temprano y un control posterior.

| Escenario | Situación |
| :--- | :--- |
| **A · Documentos** | Un estudiante intenta descargar el documento de otro usuario modificando un identificador. |
| **B · Token** | Un desarrollador intenta incluir un token dentro de un commit. |
| **C · Profesor** | Un profesor intenta modificar calificaciones de un grupo no asignado. |
| **D · Login** | Una cuenta registra 100 intentos fallidos de autenticación en 10 minutos. |

---

## Matriz de Requisitos por Fase

| Esc. | Requisitos | Diseño | Desarrollo | Pruebas | Despliegue | Operación |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **A** | Definir política de bloqueo de cuentas y límites de intentos de autenticación | Diseñar el endpoint de descarga con verificación obligatoria de propiedad (ownership check) antes de servir el archivo, separada de la lógica de negocio | Implementar middleware de autorización que valide `usuario_actual.id == documento.propietario_id` en cada solicitud; usar UUIDs en vez de IDs secuenciales | Pruebas de integración que intenten acceder a documentos de otro usuario (BOLA/IDOR); SAST buscando rutas de descarga sin decorador de autorización | Configurar el API Gateway para registrar y limitar solicitudes repetitivas a rutas de descarga con parámetros variables | Monitorear patrones de acceso secuencial a IDs de documentos (posible enumeración) y generar alertas |
| **B** | Política de manejo de secretos: ningún credential/token en código fuente, uso obligatorio de variables de entorno o vault | Definir arquitectura de gestión de secretos (ej. HashiCorp Vault, AWS Secrets Manager, GitHub Secrets) desde el diseño del sistema | Configurar `.gitignore` para archivos de configuración sensibles; usar plantillas `.env.example` sin valores reales | Pre-commit hooks y escaneo automático de secretos (ej. Gitleaks, TruffleHog) antes de permitir el commit | Escaneo de secretos como gate obligatorio en el pipeline de CI/CD (bloquear el build si se detecta un token) | Rotación inmediata de cualquier credential expuesto detectado; auditoría periódica del historial del repositorio |
| **C** | Definir matriz de roles y permisos: qué grupos/cursos puede modificar cada profesor (RBAC) | Diseñar modelo de autorización basado en la relación profesor-grupo, verificada en cada operación de escritura sobre calificaciones | Implementar verificación de asignación (`profesor.grupos.contains(grupo_id)`) antes de permitir modificar calificaciones | Pruebas funcionales que verifiquen que un profesor no puede modificar grupos ajenos; pruebas de escalación de privilegios horizontal/vertical | Validar que las políticas de autorización estén activas en el entorno de producción antes del release (checklist de despliegue) | Auditoría de cambios de calificaciones con registro de quién modificó qué grupo, para detectar accesos indebidos a posteriori |
| **D** | Definir política de bloqueo de cuentas y límites de intentos de autenticación | Diseñar mecanismo de rate limiting y bloqueo progresivo (ej. exponential backoff) a nivel de servicio de autenticación | Implementar contador de intentos fallidos, bloqueo temporal de cuenta y CAPTCHA tras N intentos | Pruebas automatizadas que simulen fuerza bruta y verifiquen que el bloqueo se activa correctamente | Configurar reglas de rate limiting en el API Gateway/WAF para la ruta de login | Alertas en tiempo real ante picos de intentos fallidos; dashboard de monitoreo de autenticación con detección de anomalías |

---

## 7. Clasificación conceptual

Elijan dos decisiones de su mapa y expliquen cuál concepto representa mejor cada una.

| Decisión | Secure SDLC / By Design / By Default / Shift Left | Justificación |
| :--- | :--- | :--- |
| **1.** Usar UUIDs en vez de IDs secuenciales desde el diseño de la base de datos | **Security by Design** | La decisión estructural se toma en el diseño del sistema, no se agrega después; cambia la arquitectura misma para que sea segura por construcción. |
| **2.** Bloqueo de cuenta tras intentos fallidos activado desde el primer despliegue (configuración predeterminada, sin que el admin tenga que activarlo) | **Security by Default** | El sistema viene "seguro por defecto": el usuario/administrador no necesita configurar nada adicional para tener protección básica. |

---

## 8. Reflexión

*   **¿Qué riesgo de SC-LAB-001 necesitó controles en más fases?**  
    Normalmente el riesgo de control de acceso roto (IDOR/BOLA) es el que más fases toca, porque requiere prevención en requisitos y diseño, implementación correcta en desarrollo, verificación en pruebas, configuración en despliegue y monitoreo en operación — ningún control aislado lo cubre completamente.

*   **¿Qué habría ocurrido si el equipo hubiera esperado hasta pruebas?**  
    El costo de corregir sería mucho mayor (rediseño de arquitectura de autorización, posible refactor de la base de datos si los IDs ya están expuestos), y existiría una ventana de exposición real si el sistema ya estuviera en producción.

*   **¿Qué control depende de una regla de negocio y cuál puede automatizarse?**  
    La verificación de "qué grupo pertenece a qué profesor" depende de una regla de negocio (debe definirla el equipo funcional); en cambio, el escaneo de secretos, el SAST y el rate limiting pueden automatizarse completamente en el pipeline.
