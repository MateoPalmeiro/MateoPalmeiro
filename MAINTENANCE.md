# Mantenimiento del perfil

## Componentes

| Componente | Origen | Actualización |
| --- | --- | --- |
| README y libro de visitas | Este repositorio, issue #1 | Al crear, editar o borrar comentarios; también manual |
| Serpiente | `snake.yml`, rama `snake` | Diaria y al publicar en `main` |
| Métricas detalladas | `metrics.yml`, `github-metrics.svg` | Diaria; necesita `METRICS_TOKEN` |
| Gráfico de actividad | `activity.yml`, `scripts/activity.py`, `activity.svg` | Dos veces al día; usa el token automático de Actions |
| Estadísticas, lenguajes y repos destacados | Despliegue `github-readme-stats1-pi.vercel.app` | Caché por defecto de seis horas tras desplegar la corrección |
| Trofeos | Despliegue `github-profile-trophy1-six.vercel.app` | Varias capas de caché: datos, servidor, CDN y proxy de GitHub |
| Racha | `streak-stats.demolab.com` | Servicio externo |
| Visitas, estrellas y seguidores | Komarev y Custom Icon Badges | Servicios externos |
| Spotify | `btk.pythonanywhere.com` | Pendiente de reactivar; bloque conservado en comentario HTML |

Los horarios de Actions no garantizan una ejecución puntual. Las imágenes también pueden permanecer en la caché del proxy de GitHub. Los commits totales, las contribuciones y los puntos de trofeos usan criterios distintos y no tienen por qué coincidir. El parámetro `count_private` no se procesa en la versión actual de las tarjetas; la cobertura depende del token del servicio y de las consultas que implementa.

El gráfico muestra 31 días en UTC y los datos que GitHub permite consultar con el token de la ejecución. No requiere copiar un token personal ni publicar nombres de repositorios privados. Si falla la consulta, el workflow falla y conserva la última imagen válida.

## Incidencias detectadas el 18 de octubre de 2026

- El antiguo gráfico externo devolvía HTTP 402, `DEPLOYMENT_DISABLED`. Se sustituye por el gráfico generado aquí.
- Spotify devolvía HTTP 404 con la página `Coming Soon: PythonAnywhere`, en lugar de una imagen. Un cliente también rechazó el certificado TLS; hay que volver a validar HTTPS al restaurar la aplicación.
- Las tarjetas guardaban por defecto las estadísticas durante un día, los lenguajes durante seis y los repos destacados durante diez. La corrección en el servicio reduce los tres valores a seis horas. Una variable `CACHE_SECONDS` configurada en Vercel prevalece sobre estos valores. El servicio puede servir contenido antiguo mientras revalida.
- El libro de visitas solo escuchaba comentarios nuevos. Ahora contempla ediciones y borrados, filtra bots y escapa el texto antes de insertarlo.
- Métricas y serpiente tenían ejecuciones diarias correctas. Los demás widgets devolvieron imágenes válidas al comprobarlos con curl.

## Acción manual: Spotify

1. Accede a la cuenta que administra `btk.pythonanywhere.com` y abre **Web**. Comprueba si la aplicación está desactivada o ha caducado; reactívala si procede y recárgala.
2. Si no arranca, revisa sus logs y la configuración de la aplicación. El código de este servicio no se encontró entre los repositorios de la cuenta revisada.
3. Comprueba que `https://btk.pythonanywhere.com?spin=true&theme=dark&eq_color=39FF14` devuelve una imagen válida por HTTPS y que `/link` redirige al destino esperado. Si falla la autorización de Spotify, renueva esa autorización desde la aplicación sin publicar credenciales.
4. Cuando funcione, elimina los delimitadores del comentario HTML que rodea el bloque Spotify en `README.md`.

## Si las tarjetas siguen desactualizadas

En Vercel, comprueba que el dominio de producción apunta al último commit del repositorio del servicio. Revisa `CACHE_SECONDS`: elimínala para usar los valores del código o configúrala como `21600`. Redespliega producción si el despliegue automático no se realiza. No publiques valores de `PAT_1`, `GITHUB_TOKEN1` ni otros secretos.

Para regenerar el gráfico, la serpiente, las métricas o el libro de visitas, abre **Actions**, selecciona el workflow correspondiente y utiliza **Run workflow**. Ante un fallo, consulta el log antes de cambiar tokens.
