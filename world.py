import random
import utils
from utils import Vector2
from particles import Particle, newParticle

class Chunk:
    def __init__(self, chunkPosition: Vector2, chunkSize: int = 16):
        self.CHUNK_SIZE = chunkSize
        self.Position = chunkPosition
        self.isActive = False
        self.particleCount = 0
    
        self.Active_Particles = set()
        self.Entropy_Affected = set()
        self.GRID = [[utils.AMBIENT_TEMPERATURE] * chunkSize for _ in range(chunkSize)]

    def _addParticle(self, particle: Particle, gridPosition: Vector2):
        grid_X = gridPosition.X
        grid_Y = gridPosition.Y
        if isinstance(self.GRID[grid_Y][grid_X], (int, float)):
            self.particleCount += 1

        self.GRID[grid_Y][grid_X] = particle
        self.isActive = True
        self.Active_Particles.add((grid_X, grid_Y))

    def _removeParticle(self, gridPosition: Vector2):
        grid_X = gridPosition.X
        grid_Y = gridPosition.Y
        
        if not isinstance(self.GRID[grid_Y][grid_X], (int, float)):
            self.particleCount -= 1
            self.GRID[grid_Y][grid_X] = utils.AMBIENT_TEMPERATURE
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

        self.MAX_TEMPERATURE = 2000.0
        self.MIN_TEMPERATURE = -273.0
        self.TEMP_ACTIVATION_THRESHOLD = 10.0

        self.AIR_HEAT_CAPACITY = 4.0
        self.AIR_HEAT_CONDUCTIVITY = 0.1
        self.AIR_HEAT_DISPERSION_START = 200.0
        self.AIR_COOLING_RATE = 0.01

        # Quantidade de chunks
        self.Chunks_Quantity_X = self.WIDTH // self.CHUNK_SIZE
        self.Chunks_Quantity_Y = self.HEIGTH // self.CHUNK_SIZE

        # Geração dos chunks
        self.Running = True
        self.Current_Frame = 0
        self.Chunks = [[None] * self.Chunks_Quantity_X for _ in range(self.Chunks_Quantity_Y)]
        for chunk_Y in range(self.Chunks_Quantity_Y):
            for chunk_X in range(self.Chunks_Quantity_X):
                self.Chunks[chunk_Y][chunk_X] = Chunk(Vector2(chunk_X, chunk_Y), self.CHUNK_SIZE)

    def update_chunk(self, chunk: Chunk):
        # Coordenada Base
        basePos = Vector2(chunk.Position.X * self.CHUNK_SIZE, chunk.Position.Y * self.CHUNK_SIZE) 

        # Iteração aleaória
        active_list = list(chunk.Active_Particles)
        random.shuffle(active_list)

        for grid_X, grid_Y in active_list:
            particle = chunk.GRID[grid_Y][grid_X]

            if not isinstance(particle, (int, float)) and particle.isActive:
                if particle.Current_Frame == self.Current_Frame: continue
                particle.Current_Frame = self.Current_Frame
                particle.update(self, basePos + Vector2(grid_X, grid_Y))
                particle.sleepAndActivateNeighbors(self, basePos + Vector2(grid_X, grid_Y))
                particle.movedThisFrame = False

                if not particle.isActive:
                    chunk.Active_Particles.discard((grid_X, grid_Y))
            
    def update(self):
        if not self.Running: return
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
                particle = newParticle(particleName)
                chunk._addParticle(particle, gridPos)
                if abs(particle.Temperature - utils.AMBIENT_TEMPERATURE) > self.TEMP_ACTIVATION_THRESHOLD:
                    chunk.Entropy_Affected.add((gridPos.X, gridPos.Y))
                    self.wakeUpHeatNeighbors(position)

    def setInstancedParticle(self, particle: Particle, toPos: Vector2):
        # Coordenada mundial para chunk
        chunkPos, gridPos = self.worldPOS_TO_chunkPOS(toPos)
        
        # Verifica se o chunk existe
        if 0 <= chunkPos.X < self.Chunks_Quantity_X and 0 <= chunkPos.Y < self.Chunks_Quantity_Y:
            chunk = self.Chunks[chunkPos.Y][chunkPos.X]

            # Remoção ou adição de particula
            chunk._addParticle(particle, gridPos)
            if abs(particle.Temperature - utils.AMBIENT_TEMPERATURE) > self.TEMP_ACTIVATION_THRESHOLD:
                chunk.Entropy_Affected.add((gridPos.X, gridPos.Y))
                self.wakeUpHeatNeighbors(toPos)

    def getParticle(self, position: Vector2) -> Particle:
        # Coordenada mundial para chunk
        chunkPos, gridPos = self.worldPOS_TO_chunkPOS(position)
        
        # Verifica se o chunk existe
        if 0 <= chunkPos.X < self.Chunks_Quantity_X and 0 <= chunkPos.Y < self.Chunks_Quantity_Y:
            particle = self.Chunks[chunkPos.Y][chunkPos.X].GRID[gridPos.Y][gridPos.X]
            return None if isinstance(particle, (int, float)) else particle
        return False
    ### -------------------------------------------------------------------------------------------------


    ### MÉTODOS DAS PARTICULAS --------------------------------------------------------------------------
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
    
    def createParticleInstance(self, particleName: str) -> Particle:
        if not particleName:
            raise ValueError(f"createParticleInstance chamada sem nome da particula.")
        return newParticle(particleName)

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
            if not (0 <= nx < self.WIDTH and 0 <= ny < self.HEIGTH):
                continue
            
            chunk_x = nx // self.CHUNK_SIZE
            chunk_y = ny // self.CHUNK_SIZE
            grid_x = nx % self.CHUNK_SIZE
            grid_y = ny % self.CHUNK_SIZE
            
            particle = self.Chunks[chunk_y][chunk_x].GRID[grid_y][grid_x]
            
            if not isinstance(particle, (int, float)) and not particle.isActive:
                particle.wokenByNeighbors = True
                particle._dead_frames = 0
                particle.isActive = True
                self.Chunks[chunk_y][chunk_x].Active_Particles.add((grid_x, grid_y))

    #-----------------------------------------------------------------------------------------------------


    
    # MÉTODO DA TEMPERATURA
    def wakeUpHeatNeighbors(self, position: Vector2):
        offsets = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]
        
        for dx, dy in offsets:
            nx = position.X + dx
            ny = position.Y + dy
            
            if not (0 <= nx < self.WIDTH and 0 <= ny < self.HEIGTH):
                continue
            
            chunk_x = nx // self.CHUNK_SIZE
            chunk_y = ny // self.CHUNK_SIZE
            grid_x = nx % self.CHUNK_SIZE
            grid_y = ny % self.CHUNK_SIZE
            
            self.Chunks[chunk_y][chunk_x].Entropy_Affected.add((grid_x, grid_y))
    
    def updateHeat(self):
        for chunk_Y in range(self.Chunks_Quantity_Y - 1, -1, -1):
            for chunk_X in range(self.Chunks_Quantity_X):
                chunk: Chunk = self.Chunks[chunk_Y][chunk_X]
                if len(chunk.Entropy_Affected) > 0:
                    
                    # Coordenada Base
                    base_X = chunk.Position.X * self.CHUNK_SIZE
                    base_Y = chunk.Position.Y * self.CHUNK_SIZE
                    
                    # copia o entry affect para não fazer merda no original
                    entropy_list = list(chunk.Entropy_Affected)
                    
                    for grid_X, grid_Y in entropy_list:
                        world_X = base_X + grid_X
                        world_Y = base_Y + grid_Y
                        position = Vector2(world_X, world_Y)
                        
                        self.disperseHeat(position)
                        
                        cell = chunk.GRID[grid_Y][grid_X]
                        current_temp = utils.AMBIENT_TEMPERATURE
                        
                        if isinstance(cell, (int, float)):
                            current_temp = cell
                            # sistema para o ar esfriar sozinho
                            if current_temp < self.AIR_HEAT_DISPERSION_START:
                                temp_diff = current_temp - utils.AMBIENT_TEMPERATURE
                                cooling = temp_diff * self.AIR_COOLING_RATE
                                new_temp = current_temp - cooling
                                chunk.GRID[grid_Y][grid_X] = new_temp
                                current_temp = new_temp
                        else:
                            current_temp = cell.Temperature
                        
                        # Remove do Entropy_Affected se estabilizou
                        if abs(current_temp - utils.AMBIENT_TEMPERATURE) < self.TEMP_ACTIVATION_THRESHOLD:
                            chunk.Entropy_Affected.discard((grid_X, grid_Y))

    def disperseHeat(self, position: Vector2):
        """Dispersa o calor de uma célula para seus vizinhos"""
        chunk_x = position.X // self.CHUNK_SIZE
        chunk_y = position.Y // self.CHUNK_SIZE
        grid_x = position.X % self.CHUNK_SIZE
        grid_y = position.Y % self.CHUNK_SIZE
        
        cell = self.Chunks[chunk_y][chunk_x].GRID[grid_y][grid_x]
        
        # Propriedades térmicas da célula atual
        current_temp = utils.AMBIENT_TEMPERATURE
        heat_capacity = self.AIR_HEAT_CAPACITY
        conductivity = self.AIR_HEAT_CONDUCTIVITY
        
        if isinstance(cell, (int, float)):
            current_temp = cell
        else:
            current_temp = cell.Temperature
            heat_capacity = cell.HEAT_CAPACITY
            conductivity = cell.HEAT_CONDUCTIVITY
        
        # Offset dos vizinhos
        offsets = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]
        
        temp_sum = 0
        count = 0
        
        # Média das temperaturas dos vizinhos
        for dx, dy in offsets:
            nx = position.X + dx
            ny = position.Y + dy
            
            if not (0 <= nx < self.WIDTH and 0 <= ny < self.HEIGTH):
                continue
            
            # Calcula posição inline
            n_chunk_x = nx // self.CHUNK_SIZE
            n_chunk_y = ny // self.CHUNK_SIZE
            n_grid_x = nx % self.CHUNK_SIZE
            n_grid_y = ny % self.CHUNK_SIZE
            
            neighbor = self.Chunks[n_chunk_y][n_chunk_x].GRID[n_grid_y][n_grid_x]
            
            neighbor_temp = utils.AMBIENT_TEMPERATURE
            if isinstance(neighbor, (int, float)):
                neighbor_temp = neighbor
            else:
                neighbor_temp = neighbor.Temperature
            
            temp_sum += neighbor_temp
            count += 1
        
        # Aplicação da mudança de temperatura
        if count > 0:
            avg_temp = temp_sum / count
            temp_difference = avg_temp - current_temp
            
            heat_change = temp_difference * conductivity / heat_capacity
            new_temp = current_temp + heat_change
            
            # Clamp da temperatura
            new_temp = max(self.MIN_TEMPERATURE, min(self.MAX_TEMPERATURE, new_temp))
            
            # Aplica a nova temperatura
            if isinstance(cell, (int, float)):
                self.Chunks[chunk_y][chunk_x].GRID[grid_y][grid_x] = new_temp
            else:
                cell.Temperature = new_temp
                cell.tempChanged(self, position)
            
            # Se a temperatura mudou significativamente, ativa os vizinhos também
            if abs(new_temp - current_temp) > self.TEMP_ACTIVATION_THRESHOLD * 0.5:
                self.wakeUpHeatNeighbors(position)
