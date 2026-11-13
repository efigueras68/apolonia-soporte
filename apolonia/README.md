# Apolonia Soporte

Programa de soporte remoto de [Apolonia](https://apolonia.cloud), basado en
[RustDesk](https://github.com/rustdesk/rustdesk) 1.5.3 (licencia AGPL-3.0).

Cambios respecto a RustDesk (todos en esta carpeta y en `.github/workflows/apolonia-windows.yml`):

- Servidor propio de Apolonia (`soporte.apolonia.cloud`) y su clave pública, ya puestos de fábrica.
- Nombre «Apolonia Soporte» (`ApoloniaSoporte`), iconos y textos del ejecutable con la marca de Apolonia.
- Receta de compilación solo para Windows x64.

Los cambios se aplican al compilar con `apolonia/aplicar_marca.py`; el resto del código es el de
RustDesk sin modificar. El código fuente completo de cada versión distribuida está en este repositorio.
