# SC-LAB-009 | Registro de evidencias

**Equipo:** Yadhira Anadanely Benitez Millan, Ximena Becerril Olivares, Pamela Espinoza Montiel, Sergio Yahir Hernandez Guerrero
**Grupo:** __________  **Fecha:** __________

> Los campos marcados con **[COMPLETAR]** deben llenarse con los resultados reales de tu ejecución. No inventes cifras.

## Tabla de resultados

| Control | Comando / ubicación | Resultado (aprobado / hallazgo / no ejecutado) | Explicación y evidencia |
|---|---|---|---|
| Pruebas | `python -m pytest -q` | **[COMPLETAR]** | Se ejecutaron **[N]** pruebas: **[N]** aprobadas y **[N]** fallidas, en **[N]** segundos. Las pruebas verifican el comportamiento de la aplicación: inicio y cierre de sesión, token CSRF, permisos por rol (profesor, estudiante) y validación de calificaciones. Evidencia A. |
| SAST | `python -m bandit -r src -ll -ii` | **[COMPLETAR]** | **[Sin hallazgos: "Bandit no reportó problemas de severidad y confianza media/alta en la carpeta src." / Con hallazgos: archivo, línea, gravedad, confianza y recomendación.]** Evidencia B. |
| Dependencias | `python -m pip_audit -r requirements.txt` | **[COMPLETAR]** | **[Sin vulnerabilidades conocidas / o paquete afectado, versión instalada, identificador del aviso y versión corregida que propone la herramienta.]** Evidencia C. |
| CI en GitHub | Pestaña Actions | **[COMPLETAR]** | **[Si se ejecutó: estado de los trabajos `security` y `container` y pasos exitosos o fallidos. Si no: "no ejecutado; se revisó localmente el archivo security.yml".]** Evidencias D y E. |
| Imagen / Trivy | Trabajo container | **[COMPLETAR]** | **[Si se ejecutó: resultado del build y del escaneo. Si no: "no ejecutado; se revisaron Dockerfile y compose.yaml".]** Evidencias F y G. |

## Evidencia A: pytest

Captura del comando `python -m pytest -q` y su resumen final.

![Evidencia A - pytest](capturas/A_pytest.png)

**Pregunta: ¿qué verifica una prueba automatizada que no necesariamente verifica un analizador estático?**
Una prueba automatizada ejecuta la aplicación y comprueba su comportamiento real: por ejemplo, que un estudiante no pueda consultar la calificación de otro o que una calificación de 150 sea rechazada. Un analizador estático solo lee el código sin ejecutarlo y busca patrones inseguros, por lo que no puede confirmar que la lógica de negocio funcione como se espera.

## Evidencia B: Bandit (SAST)

Captura del resultado de `python -m bandit -r src -ll -ii`.

![Evidencia B - Bandit](capturas/B_bandit.png)

**Registro de hallazgos** (llenar solo si Bandit reportó advertencias; no modificar el código):

| Archivo | Línea | Gravedad | Confianza | Recomendación |
|---|---|---|---|---|
| [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

**Interpretación:** [COMPLETAR: qué significa el resultado y qué alcance tiene. Recuerda que `-ll` y `-ii` filtran hallazgos de severidad y confianza bajas.]

## Evidencia C: pip-audit (SCA)

Captura del resultado de `python -m pip_audit -r requirements.txt`.

![Evidencia C - pip-audit](capturas/C_pip_audit.png)

**Registro de vulnerabilidades** (llenar solo si hubo avisos):

| Paquete | Versión instalada | Aviso (ID) | Versión corregida |
|---|---|---|---|
| [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

**Interpretación:** [COMPLETAR: si hubo error de conectividad, indicarlo; un error de red no significa cero vulnerabilidades.]

## Evidencia D: pipeline de GitHub Actions (archivo YAML)

Captura del archivo `.github/workflows/security.yml` abierto en Visual Studio Code.

![Evidencia D - security.yml](capturas/D_pipeline_yaml.png)

**Explicación con nuestras palabras del orden de los controles:**

- **Cuándo inicia:** con un `push`, un `pull_request` o una ejecución manual (`workflow_dispatch`).
- **Trabajo `security`** (equipo Linux de GitHub, `ubuntu-latest`): descarga el repositorio, prepara Python 3.12, instala dependencias y ejecuta en este orden pytest, Bandit y pip-audit. Si un paso falla, los siguientes no se ejecutan.
- **Trabajo `container`:** descarga el repositorio, construye la imagen Docker y la escanea con Trivy. No depende de `security`, por lo que corre en paralelo.
- **`exit-code: '1'`:** hace que un hallazgo HIGH o CRITICAL marque el trabajo como fallido. Con `ignore-unfixed: true` se ignoran las vulnerabilidades que aún no tienen corrección publicada.

## Evidencia E: GitHub Actions ejecutándose (opcional)

Captura de la pestaña Actions con los trabajos `security` y `container`. Si no se realizó, escribir "no ejecutado".

![Evidencia E - GitHub Actions](capturas/E_github_actions.png)

**Observaciones:** [COMPLETAR: pasos exitosos, fallidos o pendientes; si hubo un hallazgo, registrarlo.]

## Evidencia F: construcción de la imagen Docker (opcional)

Captura de `docker build -t securecampus:lab009 .` y `docker images`. Si no tienes Docker, escribir "no ejecutado".

![Evidencia F - Docker build](capturas/F_docker_build.png)

Construir la imagen correctamente **no demuestra** que esté libre de vulnerabilidades; para eso se usa Trivy.

## Evidencia G: configuración de seguridad de Docker (ruta sin Docker o complemento)

Captura de `Dockerfile` y `compose.yaml` con las medidas resaltadas.

![Evidencia G - Dockerfile y compose](capturas/G_dockerfile_compose.png)

| Medida | Archivo | Para qué sirve |
|---|---|---|
| `USER scapp` | Dockerfile | La aplicación corre con un usuario sin privilegios de administrador; si se compromete, el daño es menor. |
| `read_only: true` | compose.yaml | El sistema de archivos del contenedor es de solo lectura, lo que impide que un atacante modifique archivos (solo `/data` y `/tmp` son escribibles). |
| `cap_drop: ALL` | compose.yaml | Elimina todas las capacidades especiales de Linux que la aplicación no necesita. |
| `127.0.0.1:5000:8000` | compose.yaml | El puerto solo es accesible desde el propio equipo, no desde la red. |

## Reflexión

1. **¿Qué control impide integrar un cambio con pruebas fallidas?**
   El paso de pytest del pipeline: si alguna prueba falla, el trabajo `security` termina en rojo y el cambio no debe aprobarse hasta investigar la causa.

2. **¿En qué se diferencia SAST de auditar dependencias?**
   SAST (Bandit) analiza el código que escribimos nosotros en busca de patrones potencialmente inseguros. La auditoría de dependencias (pip-audit) revisa las bibliotecas de terceros contra vulnerabilidades ya publicadas.

3. **¿Por qué un pipeline que aparece en verde no garantiza seguridad absoluta?**
   Porque cada herramienta tiene un alcance limitado: no detectan fallas de lógica de negocio ni vulnerabilidades desconocidas, y los resultados cambian con el tiempo, ya que las dependencias están en rangos de versión y no fijadas.

4. **¿Qué harías al detectar una vulnerabilidad crítica en una imagen?**
   No publicar la aplicación, identificar el paquete afectado, actualizar la imagen base o la dependencia, reconstruir la imagen, volver a escanear y documentar el hallazgo. Si no existe corrección, evaluar si la vulnerabilidad es explotable en nuestro caso.

## Conclusión del equipo (6 a 10 líneas)

[COMPLETAR con los resultados reales. Debe mencionar: qué controles se ejecutaron y con qué resultado (con cifras), la diferencia entre pytest, Bandit, pip-audit y Trivy, qué se aprendió del pipeline y qué haría el equipo ante un aviso crítico antes de publicar.]
