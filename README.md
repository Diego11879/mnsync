# Descripción
Este simple script de python te permitirá monitorear de forma automática lo que ocurre en un directorio especifíco
para luego sincronizarlo con un segundo directorio.

# Uso
Deberas especificar en el archivo *main.py* en la variable *DIRECTORY_TO_WATCH* el directorio que deseas monitorear, 
luego deberás especificar en el directorio a sincronizar en la variable *SYNC_DIRECTORY*, que en este caso está fijado 
en un dispositivo externo montado en */mnt*.

# Ubicación de archivos
 - `99-mount-external-drive.rules`: Es una regla udev que debe ir en `/etc/udev/rules.d/`
 - `mount_external_drive.sh`: Es un script que monta un dispositivo de forma automática, este se activa mediante
   le regla udev anterior.
