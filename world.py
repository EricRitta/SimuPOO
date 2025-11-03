import random
from utils import Vector2
from particles import Particle, newParticle

class Chunk:
    def __init__(self, chunkPosition: Vector2, chunkSize: int = 16):
        self.CHUNK_SIZE = chunkSize
        self.Position = chunkPosition
        self.isActive = False
        self.particleCount = 0
    
        self.Active_Particles = set()
        self.GRID = [[None] * chunkSize for _ in range(chunkSize)]

    def _addParticle(self, particle: Particle, gridPosition: Vector2):
        grid_X = gridPosition.X
        grid_Y = gridPosition.Y
        if self.GRID[grid_Y][grid_X] == None:
            self.particleCount += 1

        self.GRID[grid_Y][grid_X] = particle
        self.isActive = True
        self.Active_Particles.add((grid_X, grid_Y))

    def _removeParticle(self, gridPosition: Vector2):
        grid_X = gridPosition.X
        grid_Y = gridPosition.Y
 
        self.particleCount -= 1
        self.GRID[grid_Y][grid_X] = None
        self.Active_Particles.discard((grid_X, grid_Y))

        if self.particleCount <= 0:
            self.particleCount = 0
            self.isActive = False

class World:
    def __init__(self, width: int = 500, heigth: int = 300, chunkSize: int = 16):
        # Arredonda para multiplo do chunk size
        actualWidth = ((width + chunkSize - 1) // chunkSize) * chunkSize
        actualHeigth = ((heigth + chunkSize - 1) // chunkSize) * chunkSize

        # Constantes
        self.WIDTH = actualWidth
        self.HEIGTH = actualHeigth
        self.CHUNK_SIZE = chunkSize

        # Quantidade de chunks
        self.Chunks_Quantity_X = self.WIDTH // self.CHUNK_SIZE
        self.Chunks_Quantity_Y = self.HEIGTH // self.CHUNK_SIZE

        # Geração dos chunks
        self.Current_Frame = 0
        self.Chunks = [[None] * self.Chunks_Quantity_X for _ in range(self.Chunks_Quantity_Y)]
        for chunk_Y in range(self.Chunks_Quantity_Y):
            for chunk_X in range(self.Chunks_Quantity_X):
                self.Chunks[chunk_Y][chunk_X] = Chunk(Vector2(chunk_X, chunk_Y), self.CHUNK_SIZE)

    def update_chunk(self, chunk: Chunk):
        # Coordenada Base
        basePos = Vector2(chunk.Position.X * self.CHUNK_SIZE, chunk.Position.Y * self.CHUNK_SIZE) 

        # Iteração de baixo para cima
        active_list = list(chunk.Active_Particles)
        random.shuffle(active_list)

        for grid_X, grid_Y in active_list:
            particle = chunk.GRID[grid_Y][grid_X]

            if particle is not None and particle.isActive:
                if particle.Current_Frame == self.Current_Frame: continue
                particle.Current_Frame = self.Current_Frame
                particle.update(self, basePos + Vector2(grid_X, grid_Y))
                particle.sleepAndActivateNeighbors(self, basePos + Vector2(grid_X, grid_Y))
                particle.movedThisFrame = False

                if not particle.isActive:
                    chunk.Active_Particles.discard((grid_X, grid_Y))
            
    def update(self):
        self.Current_Frame ^= 1
        
        for chunk_Y in range(self.Chunks_Quantity_Y - 1, -1, -1):
            for chunk_X in range(self.Chunks_Quantity_X):
                chunk = self.Chunks[chunk_Y][chunk_X]
                if chunk.isActive:
                    self.update_chunk(chunk)


    ### MÉTODOS BÁSICOS -----------------------------------------------------------------------------
    def worldPOS_TO_chunkPOS(self, globalPosition: Vector2) -> tuple[Vector2, Vector2]:
        chunk_Position = globalPosition // self.CHUNK_SIZE
        grid_Position = globalPosition % self.CHUNK_SIZE
        return chunk_Position, grid_Position

    def setParticle(self, particleName, position: Vector2):
        # Coordenada mundial para chunk
        chunkPos, gridPos = self.worldPOS_TO_chunkPOS(position)
        
        # Verifica se o chunk existe
        if 0 <= chunkPos.X < self.Chunks_Quantity_X and 0 <= chunkPos.Y < self.Chunks_Quantity_Y:
            chunk = self.Chunks[chunkPos.Y][chunkPos.X]

            # Remoção ou adição de particula
            if particleName is None:
                chunk._removeParticle(gridPos)
                self.wakeUpNeighbors(position, None)
            else:
                chunk._addParticle(newParticle(particleName), gridPos)

    def setInstancedParticle(self, particle: Particle, toPos: Vector2):
        # Coordenada mundial para chunk
        chunkPos, gridPos = self.worldPOS_TO_chunkPOS(toPos)
        
        # Verifica se o chunk existe
        if 0 <= chunkPos.X < self.Chunks_Quantity_X and 0 <= chunkPos.Y < self.Chunks_Quantity_Y:
            chunk = self.Chunks[chunkPos.Y][chunkPos.X]

            # Remoção ou adição de particula
            chunk._addParticle(particle, gridPos)

    def getParticle(self, position: Vector2) -> Particle:
        # Coordenada mundial para chunk
        chunkPos, gridPos = self.worldPOS_TO_chunkPOS(position)
        
        # Verifica se o chunk existe
        if 0 <= chunkPos.X < self.Chunks_Quantity_X and 0 <= chunkPos.Y < self.Chunks_Quantity_Y:
            return self.Chunks[chunkPos.Y][chunkPos.X].GRID[gridPos.Y][gridPos.X]
        return False
    ### -------------------------------------------------------------------------------------------------


    # MÉTODOS DAS PARTICULAS
    def killAndMove(self, fromPos: Vector2, toPos: Vector2) -> bool:
        particle = self.getParticle(fromPos)
        if not particle: return False

        self.setParticle(None, fromPos)
        self.setInstancedParticle(particle, toPos)
        return True
    
    def swapParticles(self, fromPos: Vector2, toPos: Vector2):
        particle1 = self.getParticle(fromPos)
        particle2 = self.getParticle(toPos)
        
        if particle1 is None or particle2 is None:
            return False
        
        # Remove ambas
        self.setParticle(None, fromPos)
        self.setParticle(None, toPos)
        
        # Coloca nas posições trocadas
        self.setInstancedParticle(particle2, fromPos)
        self.setInstancedParticle(particle1, toPos)
        return True
    
    def killAndReplace(self, replacedPos: Vector2, newParticleName: str):
        toRemoveParticle = self.getParticle(replacedPos)
        if not toRemoveParticle: return
        toReplaceParticle = newParticle(newParticleName)
        toReplaceParticle.Current_Frame = toRemoveParticle.Current_Frame

        self.setParticle(None, replacedPos)
        self.setInstancedParticle(toReplaceParticle, replacedPos)
    
    def wakeUpNeighbors(self, fromPos: Vector2, toPos: Vector2):
        # Offsets dos 8 vizinhos
        offsets = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]
        
        positions_to_activate = set()

        for dx, dy in offsets:
            positions_to_activate.add((fromPos.X + dx, fromPos.Y + dy))

        if toPos:
            for dx, dy in offsets:
                positions_to_activate.add((toPos.X + dx, toPos.Y + dy))

        for nx, ny in positions_to_activate:
            # Valida limites do mundo ANTES de calcular chunks
            if not (0 <= nx < self.WIDTH and 0 <= ny < self.HEIGTH):
                continue
            
            # Calcula chunk inline (evita chamada de função)
            chunk_x = nx // self.CHUNK_SIZE
            chunk_y = ny // self.CHUNK_SIZE
            grid_x = nx % self.CHUNK_SIZE
            grid_y = ny % self.CHUNK_SIZE
            
            # Acessa diretamente (já validamos limites)
            particle = self.Chunks[chunk_y][chunk_x].GRID[grid_y][grid_x]
            
            if particle is not None and not particle.isActive:
                particle.wokenByNeighbors = True
                particle._dead_frames = 0
                particle.isActive = True
                self.Chunks[chunk_y][chunk_x].Active_Particles.add((grid_x, grid_y))
