\# SC-LAB-004 · Análisis SAST + DAST



\## Parte B · DAST con OWASP ZAP



\### 5.1 Inicio de la aplicación y verificación de conectividad



Para realizar el análisis dinámico de seguridad se inició la aplicación Flask mediante el siguiente comando:



&#x20;   python src/webapp.py



La aplicación inició correctamente en:



&#x20;   http://127.0.0.1:5000



Posteriormente, se verificó que un contenedor Docker pudiera comunicarse con la aplicación utilizando:



&#x20;   docker run --rm curlimages/curl http://host.docker.internal:5000



La prueba fue exitosa. El contenedor recibió como respuesta el contenido HTML de la aplicación SecureCampus Security Lab, confirmando que la aplicación era accesible desde Docker.



\---



\### 5.2 DAST Baseline



Se realizó un análisis pasivo utilizando OWASP ZAP Baseline con el siguiente comando:



&#x20;   docker run --rm -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://host.docker.internal:5000



El análisis obtuvo el siguiente resumen:



\- FAIL-NEW: 0

\- WARN-NEW: 7

\- INFO: 0

\- PASS: 60



\#### Hallazgos del Baseline



| Hallazgo | Regla | ¿Qué observa? | ¿Requiere análisis? |

|---|---:|---|---|

| Missing Anti-clickjacking Header | 10020 | Ausencia de una cabecera HTTP de protección contra ataques de clickjacking. | Sí |

| X-Content-Type-Options Header Missing | 10021 | Ausencia de la cabecera X-Content-Type-Options. | Sí |

| Server Leaks Version Information via "Server" HTTP Response Header Field | 10036 | El servidor puede exponer información de su versión mediante la cabecera HTTP Server. | Sí |

| Content Security Policy (CSP) Header Not Set | 10038 | No se encuentra configurada una política Content Security Policy para restringir las fuentes de contenido permitidas. | Sí |

| Storable and Cacheable Content | 10049 | Se detectó contenido que puede ser almacenado en caché. Se debe determinar si contiene información sensible. | Sí |

| Permissions Policy Header Not Set | 10063 | No se encuentra configurada la cabecera Permissions-Policy. | Sí |

| Cross-Origin-Resource-Policy Header Missing or Invalid | 90004 | La cabecera de política de recursos entre orígenes está ausente o no tiene una configuración válida. | Sí |



Los resultados WARN requieren análisis antes de considerarse vulnerabilidades confirmadas, debido a que su impacto depende del contexto y de la información manejada por la aplicación.



\---



\### 5.3 DAST Active Scan



Para realizar pruebas activas sobre la aplicación se ejecutó:



&#x20;   docker run --rm -t ghcr.io/zaproxy/zaproxy:stable zap-full-scan.py -t http://host.docker.internal:5000



El Active Scan obtuvo el siguiente resumen:



\- FAIL-NEW: 0

\- WARN-NEW: 10

\- INFO: 0

\- PASS: 131



Entre los resultados se identificó el hallazgo solicitado:



&#x20;   WARN-NEW: Cross Site Scripting (Reflected) \[40012] x 1



Endpoint afectado:



&#x20;   /buscar?nombre=...



Código de respuesta:



&#x20;   200 OK



\#### Hallazgo de XSS reflejado



| Campo | Resultado |

|---|---|

| Hallazgo | Cross Site Scripting (Reflected) |

| Regla de OWASP ZAP | 40012 |

| Endpoint | /buscar |

| Parámetro | nombre |

| Estado | WARN-NEW |

| Cantidad | 1 |

| Código HTTP | 200 OK |

| Requiere análisis | Sí |



ZAP detectó que el valor introducido mediante el parámetro `nombre` podía reflejarse en la respuesta HTML sin un escape adecuado. Esto permite que una entrada construida con contenido ejecutable pueda ser interpretada por el navegador, produciendo un posible XSS reflejado.



La respuesta obtenida fue `200 OK`. Este código únicamente indica que la petición HTTP fue procesada correctamente y no garantiza que el contenido generado sea seguro. Por lo tanto, una vulnerabilidad XSS puede estar presente aunque el servidor responda con código HTTP 200.



Además del XSS reflejado solicitado para esta sección, el Active Scan reportó otros hallazgos que requieren análisis, entre ellos Cross Site Scripting (DOM Based) \[40026] y Server Side Template Injection \[90035].

