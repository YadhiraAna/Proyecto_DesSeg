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

| Fase                  | ¿Qué debería hacerse? | Control / evidencia |
|------------------------|------------------------|---------------------|
| **Requisitos**         | Definir requerimientos negativos centrados en la opacidad de los identificadores de recursos públicos desde el inicio (exigir el uso de UUIDs o hashes en lugar de IDs secuenciales) para prevenir la enumeración horizontal. | Historias de usuario con criterios de aceptación explícitos sobre el aislamiento de datos y contratos de API (OpenAPI) libres de identificadores autoincrementables expuestos. |
| **Diseño**             | Establecer un patrón arquitectónico de autorización centralizada (ej. Policy-as-Code con OPA o un proxy de control a nivel de capa de datos) que desvincule la validación de propiedad del recurso de la lógica de negocio del controlador. | Diagrama de arquitectura y secuencia que ilustra la validación obligatoria del contexto de sesión frente al recurso solicitado antes de la persistencia. |
| **Desarrollo**         | Implementar referencias indirectas seguras (como Hashids) combinadas con middleware global de control de acceso, evitando delegar la validación de pertenencia a comprobaciones manuales y dispersas en el código. | Commit en GitHub con la implementación del filtro de autorización genérico y pruebas unitarias de aislamiento multi-usuario (Broken Object Level Authorization). |
| **Pruebas**            | Automatizar la detección de fallas de control de acceso mediante análisis estático de código (SAST con reglas personalizadas en Semgrep) enfocadas en rutas con parámetros dinámicos sin decoradores de seguridad. | Reporte automatizado en GitHub Actions de la ejecución de análisis estático y pruebas de integración orientadas a la mutación de parámetros de ruta. |
| **Despliegue**         | Configurar la pasarela de API (API Gateway) para aplicar políticas estrictas de inspección de claims en tokens JWT y reglas de limitación de tasa (Rate Limiting) orientadas a bloquear escaneos de endpoints. | Manifiesto o archivo de configuración versionado del API Gateway (ej. Kong/Nginx) y bitácora del pipeline de despliegue automatizado. |
| **Operación/Mantenimiento** | Implementar telemetría conductual y detección de anomalías basada en el análisis de ventanas deslizantes de acceso para identificar patrones automatizados de fuerza bruta o escaneo de IDs contiguos. | Dashboard de monitoreo de seguridad y reporte de incidentes simulados por patrones de consulta anómalos versionado en el repositorio. |
