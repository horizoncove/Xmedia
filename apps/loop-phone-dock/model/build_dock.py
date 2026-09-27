"""Build the LOOP phone dock and export GLB + blend.

Run: blender --background --python apps/loop-phone-dock/model/build_dock.py
"""

from __future__ import annotations

import bpy
from pathlib import Path

OUT = Path(__file__).resolve().parent
MM = 0.001


def reset() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0


def mat(name: str, color: tuple[float, float, float, float], metallic: float = 0.0, rough: float = 0.45):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    return m


def box(name: str, size: tuple[float, float, float], loc: tuple[float, float, float], material) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(scale=True)
    obj.data.materials.append(material)
    return obj


def cyl(name: str, radius: float, depth: float, loc: tuple[float, float, float], material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(material)
    return obj


def build() -> None:
    reset()
    chassis = mat("Chassis", (0.09, 0.11, 0.13, 1), 0.6, 0.35)
    rail = mat("Rail", (0.55, 0.58, 0.62, 1), 0.85, 0.25)
    accent = mat("Accent", (0.0, 0.75, 0.85, 1), 0.2, 0.3)
    phone = mat("Phone", (0.02, 0.03, 0.04, 1), 0.4, 0.2)
    glass = mat("Glass", (0.15, 0.45, 0.55, 1), 0.1, 0.05)
    stylus = mat("Stylus", (0.95, 0.55, 0.2, 1), 0.1, 0.4)

    # Base plate 220 x 160 x 12 mm, phone stands toward +Y
    box("base", (0.22, 0.16, 0.012), (0, 0, 0.006), chassis)
    # Feet
    for i, (x, y) in enumerate(((-0.09, -0.06), (0.09, -0.06), (-0.09, 0.06), (0.09, 0.06))):
        cyl(f"foot_{i}", 0.008, 0.008, (x, y, -0.004), accent)

    # Open chassis rails along X (Y = ±0.07)
    for sign, tag in ((-1, "s"), (1, "n")):
        box(f"rail_y_{tag}", (0.20, 0.006, 0.006), (0, sign * 0.07, 0.02), rail)
    # Gantry beam along Y, parked at x=0
    box("gantry", (0.012, 0.15, 0.01), (0.0, 0, 0.03), rail)
    # Carriage
    box("carriage", (0.028, 0.028, 0.016), (0.0, 0.01, 0.042), accent)
    # Stylus down toward the phone plane
    cyl("stylus", 0.004, 0.045, (0.0, 0.01, 0.02), stylus)

    # Phone cradle at front (+Y)
    box("cradle", (0.09, 0.012, 0.07), (0, 0.078, 0.05), chassis)
    box("phone_body", (0.072, 0.008, 0.15), (0, 0.07, 0.11), phone)
    box("phone_glass", (0.064, 0.002, 0.132), (0, 0.075, 0.115), glass)

    # Camera mast behind the phone, looking down-ish
    box("mast", (0.012, 0.012, 0.16), (0.09, -0.04, 0.09), chassis)
    box("head", (0.04, 0.03, 0.02), (0.07, -0.01, 0.16), accent)
    cyl("lens", 0.008, 0.012, (0.05, 0.0, 0.16), glass, rot=(1.5708, 0, 1.2))

    # Camera
    bpy.ops.object.camera_add(location=(0.28, -0.32, 0.22), rotation=(1.15, 0, 0.7))
    cam = bpy.context.active_object
    bpy.context.scene.camera = cam
    bpy.ops.object.light_add(type="AREA", location=(0.2, -0.2, 0.35))
    light = bpy.context.active_object
    light.data.energy = 250

    blend_path = OUT / "loop-phone-dock.blend"
    glb_path = OUT / "loop-phone-dock.glb"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    bpy.ops.export_scene.gltf(filepath=str(glb_path), export_format="GLB")
    print(f"wrote {blend_path}")
    print(f"wrote {glb_path}")


if __name__ == "__main__":
    build()
