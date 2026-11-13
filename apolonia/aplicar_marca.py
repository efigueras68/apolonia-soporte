#!/usr/bin/env python3
"""
Apolonia Soporte: aplica la marca y el servidor propio sobre RustDesk antes de compilar.

Se ejecuta en la receta de GitHub (.github/workflows/apolonia-windows.yml) justo después de
descargar el código. Cada cambio comprueba que el texto original existe exactamente una vez:
si RustDesk cambia algo en una versión nueva, la compilación se para aquí en lugar de publicar
un programa a medias (por ejemplo, con la marca pero apuntando al servidor de RustDesk).

Cambios:
  - Servidor de ID/relé y clave pública: soporte.apolonia.cloud (servidor propio de Apolonia).
  - Nombre de la aplicación: ApoloniaSoporte (sin espacios: se usa en servicios y carpetas).
    Al no llamarse «RustDesk», el programa no busca actualizaciones de RustDesk (is_custom_client).
  - Textos del ejecutable (empresa, descripción, producto) e iconos.

Código basado en RustDesk (https://github.com/rustdesk/rustdesk), licencia AGPL-3.0.
"""
import os
import shutil
import sys

SERVIDOR = "soporte.apolonia.cloud"
CLAVE = "8dBgNpeTVBK2wmYPObfujIchS0+x4WFWUA+VS+y5ULY="
NOMBRE_APP = "ApoloniaSoporte"
NOMBRE_VISIBLE = "Apolonia Soporte"
EMPRESA = "Apolonia"
COPYRIGHT = "Apolonia. Basado en RustDesk (AGPL-3.0), Purslane Tech Pte. Ltd."

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARCA = os.path.join(RAIZ, "apolonia", "marca")


def reemplazar(ruta, cambios):
    ruta = os.path.join(RAIZ, ruta)
    with open(ruta, "r", encoding="utf-8", newline="") as f:
        texto = f.read()
    for viejo, nuevo in cambios:
        n = texto.count(viejo)
        if n != 1:
            sys.exit(f"ERROR en {ruta}: se esperaba 1 vez y aparece {n} veces:\n  {viejo}")
        texto = texto.replace(viejo, nuevo)
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write(texto)
    print(f"ok  {ruta} ({len(cambios)} cambios)")


def copiar(origen, destino):
    o = os.path.join(MARCA, origen)
    d = os.path.join(RAIZ, destino)
    if not os.path.exists(d):
        sys.exit(f"ERROR: no existe el fichero a sustituir {d}")
    shutil.copyfile(o, d)
    print(f"ok  icono {destino}")


reemplazar("libs/hbb_common/src/config.rs", [
    ('pub const RENDEZVOUS_SERVERS: &[&str] = &["rs-ny.rustdesk.com"];',
     f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{SERVIDOR}"];'),
    ('pub const RS_PUB_KEY: &str = "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=";',
     f'pub const RS_PUB_KEY: &str = "{CLAVE}";'),
    ('pub static ref APP_NAME: RwLock<String> = RwLock::new("RustDesk".to_owned());',
     f'pub static ref APP_NAME: RwLock<String> = RwLock::new("{NOMBRE_APP}".to_owned());'),
])

reemplazar("flutter/windows/runner/Runner.rc", [
    ('VALUE "CompanyName", "Purslane Tech Pte. Ltd." "\\0"', f'VALUE "CompanyName", "{EMPRESA}" "\\0"'),
    ('VALUE "FileDescription", "RustDesk Remote Desktop" "\\0"', f'VALUE "FileDescription", "{NOMBRE_VISIBLE}" "\\0"'),
    ('VALUE "LegalCopyright", "Copyright © 2026 Purslane Tech Pte. Ltd. All rights reserved." "\\0"',
     f'VALUE "LegalCopyright", "{COPYRIGHT}" "\\0"'),
    ('VALUE "ProductName", "RustDesk" "\\0"', f'VALUE "ProductName", "{NOMBRE_VISIBLE}" "\\0"'),
])

reemplazar("Cargo.toml", [
    ('LegalCopyright = "Copyright © 2026 Purslane Tech Pte. Ltd. All rights reserved."', f'LegalCopyright = "{COPYRIGHT}"'),
    ('ProductName = "RustDesk"', f'ProductName = "{NOMBRE_VISIBLE}"'),
    ('FileDescription = "RustDesk Remote Desktop"', f'FileDescription = "{NOMBRE_VISIBLE}"'),
])

copiar("icon.ico", "res/icon.ico")
copiar("tray-icon.ico", "res/tray-icon.ico")
copiar("icon.png", "res/icon.png")
copiar("32x32.png", "res/32x32.png")
copiar("64x64.png", "res/64x64.png")
copiar("128x128.png", "res/128x128.png")
copiar("128x128@2x.png", "res/128x128@2x.png")
copiar("icon.ico", "flutter/windows/runner/resources/app_icon.ico")
copiar("icon.svg", "flutter/assets/icon.svg")

print("Marca Apolonia Soporte aplicada.")
