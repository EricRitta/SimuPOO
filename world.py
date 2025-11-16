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

        self.MAX_AIR_TEMPERATURE = utils.MAX_CELL_TEMPERATURE
        self.MIN_AIR_TEMPERATURE = utils.MIN_CELL_TEMPERATURE
        self.TEMP_ACTIVATION_THRESHOLD = 10.0
        self.AIR_HEAT_CAPACITY = 4.0
        self.AIR_HEAT_CONDUCTIVITY = 0.1
        self.AIR_HEAT_DISPERSION_START = 200.0
        self.AIR_COOLING_RATE = 0.01

        # Coordenadas e Chunks
        self.NEIGHBOR_OFFSETS = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]
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
        self.Current_Frame ^= 1
        
        for chunk_Y in range(self.Chunks_Quantity_Y - 1, -1, -1):
            for chunk_X in range(self.Chunks_Quantity_X):
                chunk: Chunk = self.Chunks[chunk_Y][chunk_X]
                if chunk.isActive:
                    self.update_chunk(chunk)

    def reset(self):
        self.Current_Frame = 0
        
        # Reseta todos os chunks
        for chunk_Y in range(self.Chunks_Quantity_Y):
            for chunk_X in range(self.Chunks_Quantity_X):
                chunk: Chunk = self.Chunks[chunk_Y][chunk_X]
                
                chunk.Active_Particles.clear()
                chunk.Entropy_Affected.clear()
                chunk.GRID = [[utils.AMBIENT_TEMPERATURE] * self.CHUNK_SIZE for _ in range(self.CHUNK_SIZE)]
                chunk.isActive = False
                chunk.particleCount = 0

    ### MÉTODOS BÁSICOS -----------------------------------------------------------------------------
    def worldPOS_TO_chunkPOS(self, globalPosition: Vector2) -> tuple[Vector2, Vector2]:        
        x = globalPosition.X
        y = globalPosition.Y
        
        chunk_X = x // self.CHUNK_SIZE
        chunk_Y = y // self.CHUNK_SIZE
        grid_X = x % self.CHUNK_SIZE
        grid_Y = y % self.CHUNK_SIZE
        
        return Vector2(chunk_X, chunk_Y), Vector2(grid_X, grid_Y)

    def setParticle(self, particleName, position: Vector2, wakeUpWhenNone: bool = False):
        # Coordenada mundial para chunk
        chunkPos, gridPos = self.worldPOS_TO_chunkPOS(position)
        
        # Verifica se o chunk existe
        if 0 <= chunkPos.X < self.Chunks_Quantity_X and 0 <= chunkPos.Y < self.Chunks_Quantity_Y:
            chunk: Chunk = self.Chunks[chunkPos.Y][chunkPos.X]

            # Remoção ou adição de particula
            if particleName is None:
                chunk._removeParticle(gridPos)
                if wakeUpWhenNone:
                    self.wakeUpNeighbors(position)
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
            chunk: Chunk = self.Chunks[chunkPos.Y][chunkPos.X]

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
        self.wakeUpNeighbors(fromPos)
        self.wakeUpNeighbors(toPos)
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

        # Acorda todo mundo, hora de trabalhar
        self.wakeUpNeighbors(fromPos)
        self.wakeUpNeighbors(toPos)
        return True
    
    def killAndReplace(self, replacedPos: Vector2, newParticleName: str):
        toRemoveParticle = self.getParticle(replacedPos)
        if not toRemoveParticle: return
        toReplaceParticle = newParticle(newParticleName)
        toReplaceParticle.Current_Frame = toRemoveParticle.Current_Frame

        self.setParticle(None, replacedPos)
        self.setInstancedParticle(toReplaceParticle, replacedPos)
        self.wakeUpNeighbors(replacedPos)
    
    def createParticleInstance(self, particleName: str) -> Particle:
        if not particleName:
            raise ValueError(f"createParticleInstance chamada sem nome da particula.")
        return newParticle(particleName)

    # Peguei essa função de um cara no YouTube: MARF | @marf1610
    def iterateAndApplyMethodBetweenTwoPoints(self, pos1: Vector2, pos2: Vector2, function):
        # Se os dois pontos são iguais, executa a função apenas uma vez
        if pos1.X == pos2.X and pos1.Y == pos2.Y:
            function(self, pos1)
            return
        
        matrix_x1 = pos1.X
        matrix_y1 = pos1.Y
        matrix_x2 = pos2.X
        matrix_y2 = pos2.Y
        
        x_diff = matrix_x1 - matrix_x2
        y_diff = matrix_y1 - matrix_y2
        
        x_diff_is_larger = abs(x_diff) > abs(y_diff)
        
        x_modifier = 1 if x_diff < 0 else -1
        y_modifier = 1 if y_diff < 0 else -1
        
        longer_side_length = max(abs(x_diff), abs(y_diff))
        shorter_side_length = min(abs(x_diff), abs(y_diff))
        
        slope = 0.0 if (shorter_side_length == 0 or longer_side_length == 0) else (shorter_side_length / longer_side_length)
        
        for i in range(1, longer_side_length + 1):
            shorter_side_increase = round(i * slope)
            
            if x_diff_is_larger:
                x_increase = i
                y_increase = shorter_side_increase
            else:
                y_increase = i
                x_increase = shorter_side_increase
            
            current_y = matrix_y1 + (y_increase * y_modifier)
            current_x = matrix_x1 + (x_increase * x_modifier)
            
            # Verifica se está dentro dos limites do mundo
            if 0 <= current_x < self.WIDTH and 0 <= current_y < self.HEIGTH:
                function(self, Vector2(current_x, current_y))

    def wakeUpNeighbors(self, particlePosition: Vector2):
        posX, posY = particlePosition.X, particlePosition.Y
        for x, y in self.NEIGHBOR_OFFSETS:
            nx, ny = posX + x, posY + y

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
        posX, posY = position.X, position.Y
        for dx, dy in self.NEIGHBOR_OFFSETS:
            nx = posX + dx
            ny = posY + dy
            
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
        temp_sum = 0
        count = 0
        
        # Média das temperaturas dos vizinhos
        for dx, dy in self.NEIGHBOR_OFFSETS:
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
            new_temp = max(self.MIN_AIR_TEMPERATURE, min(self.MAX_AIR_TEMPERATURE, new_temp))
            
            # Aplica a nova temperatura
            if isinstance(cell, (int, float)):
                self.Chunks[chunk_y][chunk_x].GRID[grid_y][grid_x] = new_temp
            else:
                cell.Temperature = new_temp
                cell.tempChanged(self, position)
            
            # Se a temperatura mudou significativamente, ativa os vizinhos também
            if abs(new_temp - current_temp) > self.TEMP_ACTIVATION_THRESHOLD * 0.5:
                self.wakeUpHeatNeighbors(position)
