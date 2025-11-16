import importlib
import inspect
from pathlib import Path
from particles.base.particle import Particle

def _discover_particles():
    particles_dict = {}
    particles_info = {}
    particles_dir = Path(__file__).parent
    
    for file_path in particles_dir.glob("*.py"):
        if file_path.name.startswith("_"):
            continue
        module_name = file_path.stem
        
        try:
            module = importlib.import_module(f"particles.{module_name}")
            
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, Particle) and obj is not Particle:
                    particles_dict[name] = obj
                    
                    particles_info[name] = {
                        "NAME": getattr(obj, "NAME"),
                        "CONCRETE": getattr(obj, "CONCRETE", False),
                        "IMAGE_NAME": getattr(obj, "IMAGE_NAME", name),
                        "IMAGE_COLOR": getattr(obj, "IMAGE_COLOR"),
                        "DESCRIPTION": getattr(obj, "DESCRIPTION"),
                    }
                    
        except (ImportError, AttributeError):
            continue

    particles_dict = dict(sorted(
        particles_dict.items(), 
        key=lambda x: getattr(x[1], "ORDER", 999)
    ))
    particles_info = dict(sorted(
        particles_info.items(),
        key=lambda x: getattr(particles_dict[x[0]], "ORDER", 999)
    ))

    return particles_dict, particles_info

ParticlesIDs, ParticlesInfo = _discover_particles()
def newParticle(name: str, *args, **kwargs):
    if name not in ParticlesIDs:
        raise ValueError(f"Partícula {name} não existe.")
    return ParticlesIDs[name](*args, **kwargs)

__all__ = ["Particle", "newParticle", "ParticlesIDs", "ParticlesInfo"]
