# Angel & Troy CRUD App

Aplicación Flask con CRUD de productos, PostgreSQL y despliegue automatizado en Docker Swarm con Traefik.

## Características

- CRUD completo de productos
- PostgreSQL como base de datos
- PgAdmin disponible en `pgangeltroy.byronrm.com`
- App pública en `angeltroy.byronrm.com`
- Despliegue automático por GitHub Actions
- Stack de Docker compatible con Traefik y red `traefik-public`

## Archivos clave

- `app.py` - aplicación Flask
- `Dockerfile` - imagen de aplicación
- `stack.yml` - stack para Docker Swarm con Traefik
- `.github/workflows/deploy.yml` - CI/CD para construir imagen e implementar en VPS

## Variables de entorno usadas

- `GHCR_TOKEN` - token para publicar imagen en GitHub Container Registry
- `VPS_HOST`, `VPS_USER`, `VPS_PASSWORD`, `VPS_SSH_PORT` - credenciales SSH hacia el VPS

## Uso

1. Configura los secretos en el repositorio GitHub.
2. Empuja cambios a la rama `main`.
3. El workflow construye la imagen, la publica a GHCR y despliega el stack en el VPS.
4. Accede a `angeltroy.byronrm.com` para la app y `pgangeltroy.byronrm.com` para pgAdmin.

## Notas

- El servicio `portainerat.byronrm.com` se gestiona desde Portainer si ya existe en tu VPS.
- Cambia `FLASK_SECRET_KEY` y credenciales de PostgreSQL antes de producción.
cacalo