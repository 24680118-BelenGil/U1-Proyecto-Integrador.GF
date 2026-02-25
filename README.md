# Escenario Procedural 
## Planteamiento
Implementar transformaciones tridimensionales (traslación y escalamiento) y el modelo de color RGB mediante scripting en Blender, con el fin de diseñar un túnel curvo formado por cubos y un suelo. La estructura se generará mediante posicionamiento progresivo en el espacio y variaciones de escala, mientras que la cámara será animada para recorrer el interior del túnel siguiendo la trayectoria curva, integrando conceptos de geometría 3D y animación procedural.

## Desarrollo
### Paqueterias
```python
import bpy
import math
```
* **import bpy:** Módulo oficial de Blender que permite controlar el programa mediante Python.
* **import math:** Biblioteca estándar de Python, se usa para realizar cálculos matemáticos avanzados.

### Limpieza
```python
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
```
Prepara la escena para crear las figuras 3D y la cámara.
La primera línea de código selecciona todo objecto que este en el escenario y el segundo elimina lo seleccionado.

### Creación de materiales
Primero definimos una función crear los materiales que tendra como características un nombre y la escala de color RGB.
```python
def crear_material(nombre, r, g, b):
    mat = bpy.data.materials.new(name=nombre)
    mat.diffuse_color = (r, g, b, 1.0)
    return mat
```
* **mat = bpy.data.materials.new(name=nombre):** Crea el material con el nombre indicado.
* **mat.diffuse_color = (r, g, b, 1.0):** Asigna el color.
* **return mat:** Devuelve el material creado.

Ahora creamos, llamando al función anterior, definimos su nombre y color.
```python
mat_base = crear_material("GrisOscuro", 0.1, 0.1, 0.1)
mat_acento = crear_material("Neon", 0.0, 0.8, 1.0)
```
Finalmente definimos los parámetro del material, cámara y curva.
```python
largo = 60
punto_curva = 15
amplitud = 6
suavizado = 15

fps = 1000
duracion_seg = 1
total_frames = fps * duracion_seg
```
* **largo:** Cantidad de bloques del túnel.
* **punto_curva:** Desde qué bloque empieza la curva.
* **amplitud:** Qué tan grande será la curva.
* **suavizado:** Hace que la curva aparezca gradualmente.
* **fps:** Frames por segundo.
* **duracion_seg:** Duración de la animación en segundos.
* **total_frames:** Total de cuadros (1000).
### Bloques
Para crear los bloques usamos el bucle *for*, así en lugar de escribir una linea por cada bloque que desemos crear, el bucle se reperita segun el parámetro largo.
```python
for i in range(largo):

    n = max(0, i - punto_curva)
    entrada_suave = min(1.0, n / suavizado)
    offset_curva = math.sin(n * 0.3) * amplitud * entrada_suave
    pos_y = i * 2

    # ----- Bloque Derecho -----
    bpy.ops.mesh.primitive_cube_add(location=(3 + offset_curva, pos_y, 1))
    bpy.context.active_object.data.materials.append(mat_base)
```
* **n = max(0, i - punto_curva):** Evita que la curva empiece antes del bloque 15.
* **entrada_suave = min(1.0, n / suavizado):** Hace que la curva aumente progresivamente.
* **offset_curva = math.sin(n * 0.3) * amplitud * entrada_suave:** Calcula el desplazamiento lateral usando seno.
* **pos_y = i * 2:** Separa los bloques 2 unidades en eje Y.
```python
    bpy.ops.mesh.primitive_cube_add(location=(-3 + offset_curva, pos_y, 1))
    obj = bpy.context.active_object
    obj.data.materials.append(mat_base if i % 2 == 0 else mat_acento)    
```
*Bloque izquierdo*
* **bpy.ops.mesh.primitive_cube_add(location=(-3 + offset_curva, pos_y, 1)):** Crea un cubo en posición izquierda con curva.
* **obj = bpy.context.active_object:** Guarda el cubo recién creado.
* **obj.data.materials.append(mat_base if i % 2 == 0 else mat_acento):** Asigna material gris si es par, neón si es impar.
```python
 if i % 2 != 0:
        obj.scale.z = 1.5  
```
En este *if* define que si el bloque es impar lo hace mas alto.
```python
    bpy.ops.mesh.primitive_cube_add(location=(3 + offset_curva, pos_y, 1))
    bpy.context.active_object.data.materials.append(mat_base) 
```
*Bloque derecho*
* **bpy.ops.mesh.primitive_cube_add(location=(3 + offset_curva, pos_y, 1)):** Crea cubo en lado derecho.
* **bpy.context.active_object.data.materials.append(mat_base):** Le asigna material gris.
### Cámara
```python
bpy.ops.object.camera_add()
camara = bpy.context.active_object
camara.rotation_euler = (math.radians(85), 0, 0)
```
En este fragmento primero creamos la cámara, despues la guardamos  y por último definimos su inclinación.
### Animación
```python
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = total_frames
```
Definimos en que frame inicia la animación (1) y cuando termina ,segun el parámetro anteriormente definido.
```python
for f in range(1, total_frames + 1):

    i_anim = (f / total_frames) * (largo - 1)

    n_anim = max(0, i_anim - punto_curva)
    entrada_anim = min(1.0, n_anim / suavizado)
    offset_anim = math.sin(n_anim * 0.3) * amplitud * entrada_anim

    camara.location.x = offset_anim
    camara.location.y = i_anim * 2
    camara.location.z = 1.8

    camara.keyframe_insert(data_path="location", frame=f)
```
### Suelo y luces
```python
bpy.ops.mesh.primitive_plane_add(location=(0, largo, 0))
bpy.context.active_object.scale = (20, largo + 10, 1)
```
```python
bpy.ops.object.light_add(type='POINT', location=(0, 10, 15))
luz = bpy.context.active_object
luz.data.energy = 10000
```
```python
bpy.ops.object.light_add(type='POINT', location=(0, largo * 2, 10))
bpy.context.active_object.data.energy = 5000
```
```python
bpy.context.scene.frame_set(1)
```
## Resultado
