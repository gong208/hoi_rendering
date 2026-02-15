import bpy
import math
from mathutils import Vector

class Camera:
    def __init__(self, *, first_root, mode, is_mesh=True):
        cam = bpy.data.objects['Camera']
        self.camera = cam
        self.mode = mode

        # Reasonable defaults; we'll overwrite via set_orbit
        cam.data.lens = 85
        cam.location = Vector((0.0, 0.0, 10.0 if is_mesh else 5.2))
        cam.rotation_euler = (1.04, 0.0, -math.pi/2 + 0.43)

        # Track initial root (not critical with orbit, but kept for compatibility)
        self._root = Vector((first_root[0], first_root[1], 0.0))

        # Orbit params (filled by set_orbit)
        self._center = Vector((0.0, 0.0, 0.0))
        self._radius = 10.0
        self._height = cam.location.z
        self._theta0 = 0.0 

    def set_orbit(self, *, center, radius, height, lens=85, start_deg=0.0):
        """
        center: np.array([cx, 0, cz]) in your coords -> Blender (X, Y).
        start_deg: where on the circle to start (CCW). e.g., 90 means 'north'.
        """
        self._center = Vector((float(center[0]), float(center[2]), 0.0))
        self._radius = float(radius)
        self._height = float(height)
        self._theta0 = math.radians(float(start_deg))   # <— store CCW offset
        self.camera.data.lens = lens

        # place at starting angle
        self.orbit(0.0)

    def _look_at_center(self):
        # Convert center (x,y,0 in our XY plane) to 3D target at floor height (Z=0)
        target = Vector((self._center.x, self._center.y, 0.0))
        direction = (target - self.camera.location).normalized()
        # In Blender, camera looks along -Z with Y up
        self.camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    def orbit(self, theta):
        """theta: additional CCW angle (radians) from the starting angle."""
        cx, cy = self._center.x, self._center.y
        a = theta + self._theta0                 # <— apply starting offset
        x = cx + self._radius * math.cos(a)
        y = cy + self._radius * math.sin(a)
        self.camera.location.x = x
        self.camera.location.y = y
        self.camera.location.z = self._height
        self._look_at_center()

    # Kept to avoid breaking other calls; not used now
    def update(self, newroot, ratio=1):
        # No-op when orbiting; you can still call orbit(...) each frame
        pass
