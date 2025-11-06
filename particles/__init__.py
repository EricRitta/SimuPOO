import importlib
import inspect
from pathlib import Path
from particles.base.particle import Particle

def _discover_particles():
    particles_dict = {}
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
                    
        except (ImportError, AttributeError):
            continue
    
    return particles_dict

ParticlesIDs = _discover_particles()
def newParticle(name: str, *args, **kwargs):
    if name not in ParticlesIDs:
        raise ValueError(f"Partícula {name} não existe.")
    return ParticlesIDs[name](*args, **kwargs)

__all__ = ["Particle", "newParticle", "ParticlesIDs"]
