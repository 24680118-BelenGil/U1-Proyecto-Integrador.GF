import bpy
import math

# 1. LIMPIEZA ABSOLUTA
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 2. FUNCIÓN PARA CREAR MATERIALES
def crear_material(nombre, r, g, b):
    mat = bpy.data.materials.new(name=nombre)
    mat.diffuse_color = (r, g, b, 1.0)
    return mat

# 3. MATERIALES
mat_base = crear_material("GrisOscuro", 0.1, 0.1, 0.1)
mat_acento = crear_material("Neon", 0.0, 0.8, 1.0)

# 4. PARÁMETROS
largo = 60
punto_curva = 15
amplitud = 6
suavizado = 15

fps = 1000
duracion_seg = 1
total_frames = fps * duracion_seg

# 5. CREACIÓN DE BLOQUES
for i in range(largo):

    n = max(0, i - punto_curva)
    entrada_suave = min(1.0, n / suavizado)
    offset_curva = math.sin(n * 0.3) * amplitud * entrada_suave
    pos_y = i * 2

    # ----- Bloque Izquierdo -----
    bpy.ops.mesh.primitive_cube_add(location=(-3 + offset_curva, pos_y, 1))
    obj = bpy.context.active_object
    obj.data.materials.append(mat_base if i % 2 == 0 else mat_acento)

    if i % 2 != 0:
        obj.scale.z = 1.5

    # ----- Bloque Derecho -----
    bpy.ops.mesh.primitive_cube_add(location=(3 + offset_curva, pos_y, 1))
    bpy.context.active_object.data.materials.append(mat_base)

# 6. CONFIGURAR CÁMARA
bpy.ops.object.camera_add()
camara = bpy.context.active_object
camara.rotation_euler = (math.radians(85), 0, 0)

# 7. ANIMACIÓN MANUAL (KEYFRAMES)
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = total_frames

for f in range(1, total_frames + 1):

    i_anim = (f / total_frames) * (largo - 1)

    n_anim = max(0, i_anim - punto_curva)
    entrada_anim = min(1.0, n_anim / suavizado)
    offset_anim = math.sin(n_anim * 0.3) * amplitud * entrada_anim

    camara.location.x = offset_anim
    camara.location.y = i_anim * 2
    camara.location.z = 1.8

    camara.keyframe_insert(data_path="location", frame=f)

# 8. SUELO Y LUCES
bpy.ops.mesh.primitive_plane_add(location=(0, largo, 0))
bpy.context.active_object.scale = (20, largo + 10, 1)

# Luz principal
bpy.ops.object.light_add(type='POINT', location=(0, 10, 15))
luz = bpy.context.active_object
luz.data.energy = 10000

# Luz extra al final
bpy.ops.object.light_add(type='POINT', location=(0, largo * 2, 10))
bpy.context.active_object.data.energy = 5000
# 9. VOLVER AL FRAME 1
bpy.context.scene.frame_set(1)
