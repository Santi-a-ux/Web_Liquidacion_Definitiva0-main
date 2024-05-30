# Calculadora de Liquidación de Empleados

Este es un programa Python que permite calcular la liquidación de empleados, teniendo en cuenta diferentes factores como el salario, días trabajados, vacaciones, indemnizaciones, cesantías, entre otros. El programa ofrece una interfaz web para facilitar el ingreso de datos y la visualización de resultados.

## Características

1. Calcula la liquidación de empleados basada en:
   - Salario mensual
   - Días trabajados
   - Indemnización
   - Vacaciones
   - Cesantías
   - Intereses sobre cesantías
   - Prima de servicios
   - Retención en la fuente
2. Muestra la información detallada de la liquidación.
3. Permite agregar, consultar y eliminar usuarios y sus liquidaciones.
4. Proporciona una interfaz web amigable.

## Requisitos del Sistema

- Python 3.x instalado.
- Flask para la interfaz web [`pip install flask`]
- SQLite para la base de datos (incluido en Python)

## Uso

1. Clona este repositorio en tu máquina local:
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio
    ```

2. Instala las dependencias necesarias:
    ```bash
    pip install flask
    ```

3. Inicializa la base de datos:
    ```
    Coloca las credenciales de tu base de datos
    ```

4. Ejecuta la aplicación web:
    ```bash
    python app.py
    ```

5. Abre tu navegador web y ve a la dirección que aparece en la consola (por defecto, `http://127.0.0.1:5000/`).

## Funcionamiento

### Agregar Usuario

1. Navega a `http://127.0.0.1:5000/agregar_usuario`.
2. Llena el formulario con la información del usuario.
3. Haz clic en "Agregar Usuario".
4. Si el usuario se agrega correctamente, verás un mensaje de confirmación en la página.

### Agregar Liquidación

1. Navega a `http://127.0.0.1:5000/agregar_liquidacion`.
2. Llena el formulario con la información de la liquidación.
3. Haz clic en "Agregar Liquidacion".
4. Si la liquidación se agrega correctamente, verás un mensaje de confirmación con el total a pagar y serás redirigido a la página principal.

### Consultar Usuario

1. Navega a `http://127.0.0.1:5000/consultar_usuario`.
2. Ingresa el ID del usuario que deseas consultar.
3. Haz clic en "Consulta".
4. Si el usuario existe, verás su información y la de su liquidación.

### Eliminar Usuario

1. Navega a `http://127.0.0.1:5000/eliminar_usuario`.
2. Ingresa el ID del usuario que deseas eliminar.
3. Haz clic en "Eliminar".
4. Si el usuario se elimina correctamente, verás un mensaje de confirmación.
5. Tener en cuenta que el usuario no podra ser eliminado si aun no se ha eliminado su liquidación.

### Eliminar Liquidación

1. Navega a `http://127.0.0.1:5000/eliminar_liquidacion`.
2. Ingresa el ID de la liquidación que deseas eliminar.
3. Haz clic en "Eliminar".
4. Si la liquidación se elimina correctamente, verás un mensaje de confirmación.

## Pruebas Unitarias

Para ejecutar las pruebas unitarias, utiliza el siguiente comando en el directorio raíz:

```bash
python -m unittest discover tests mirar si funciona
```
## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para obtener más detalles.

## Desarrolladores encargados 
- David Rivera Masmela
- Santiago Gutierrez Correa