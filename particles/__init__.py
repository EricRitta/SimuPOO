from particles.base.particle import Particle
from particles.sand import Sand
from particles.water import Water
from particles.metal import Metal
from particles.mud import Mud

ParticlesIDs = {
    "Sand": Sand,
    "Water": Water,
    "Metal": Metal,
    "Mud": Mud,
}

def newParticle(name, *args, **kwargs):
    if name not in ParticlesIDs:
        raise ValueError(f"Particula {name} não existe.")
    return ParticlesIDs[name](*args, **kwargs)

__all__ = ["Particle", "newParticle"]
