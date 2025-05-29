# gossip_simulation/agent.py - Agent behavior and interactions
import mesa
import numpy as np
from typing import List, TYPE_CHECKING

from .states import GossipState

if TYPE_CHECKING:
    from .model import GossipModel


class PersonAgent(mesa.Agent):
    """Agen individu dalam simulasi penyebaran gosip"""
    
    def __init__(self, unique_id: int, model: 'GossipModel', is_resistant: bool = False):
        super().__init__(unique_id, model)
        self.state = GossipState.RESISTANT if is_resistant else GossipState.IGNORANT
        self.days_spreading = 0
        self.max_spread_days = np.random.randint(
            model.config.min_spread_days, 
            model.config.max_spread_days + 1
        )
        self.social_connections: List['PersonAgent'] = []
        self.communication_probability = np.random.uniform(
            model.config.min_communication_prob,
            model.config.max_communication_prob
        )
        
    def create_social_connections(self, connections: List['PersonAgent']) -> None:
        """Set social connections for this agent"""
        self.social_connections = connections
        
    def step(self) -> None:
        """Langkah eksekusi agen setiap iterasi"""
        if self.state == GossipState.SPREADER:
            self._spread_gossip()
            self._update_spreading_days()
        elif self.state == GossipState.IGNORANT:
            self._listen_for_gossip()
    
    def _spread_gossip(self) -> None:
        """Menyebarkan gosip ke tetangga dan koneksi sosial"""
        self._spread_gossip_local()
        self._spread_gossip_global()
    
    def _spread_gossip_local(self) -> None:
        """Menyebarkan gosip ke tetangga fisik"""
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False, radius=1
        )
        
        for neighbor in neighbors:
            if neighbor.state == GossipState.IGNORANT:
                if self.random.random() < self.model.config.spread_probability:
                    neighbor.hear_gossip()
    
    def _spread_gossip_global(self) -> None:
        """Menyebarkan gosip melalui koneksi sosial"""
        for connection in self.social_connections:
            if connection.state == GossipState.IGNORANT:
                if self.random.random() < self.communication_probability:
                    if self.random.random() < self.model.config.global_spread_probability:
                        connection.hear_gossip()
    
    def _update_spreading_days(self) -> None:
        """Update days spreading and transition to stifler if needed"""
        self.days_spreading += 1
        if self.days_spreading >= self.max_spread_days:
            self.state = GossipState.STIFLER
    
    def _listen_for_gossip(self) -> None:
        """Mendengarkan gosip dari tetangga dan koneksi sosial"""
        self._listen_for_gossip_local()
        self._listen_for_gossip_global()
    
    def hear_gossip(self) -> None:
        """Mendengar gosip dan mungkin mulai menyebar"""
        if self.state == GossipState.IGNORANT:
            if self.random.random() < self.model.config.believe_probability:
                self.state = GossipState.SPREADER
                self.days_spreading = 0
    
    def _listen_for_gossip_local(self) -> None:
        """Mendengarkan gosip secara pasif dari tetangga fisik"""
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False, radius=1
        )
        
        spreader_neighbors = [n for n in neighbors if n.state == GossipState.SPREADER]
        
        if spreader_neighbors:
            hearing_chance = min(0.8, len(spreader_neighbors) * 0.2)
            if self.random.random() < hearing_chance:
                self.hear_gossip()
    
    def _listen_for_gossip_global(self) -> None:
        """Mendengarkan gosip dari koneksi sosial"""
        spreader_connections = [c for c in self.social_connections 
                              if c.state == GossipState.SPREADER]
        
        for connection in spreader_connections:
            if self.random.random() < connection.communication_probability:
                if self.random.random() < self.model.config.global_spread_probability:
                    self.hear_gossip()
                    break
    
    def get_state_info(self) -> dict:
        """Get information about agent's current state"""
        return {
            'id': self.unique_id,
            'state': self.state.name,
            'position': self.pos,
            'days_spreading': self.days_spreading,
            'max_spread_days': self.max_spread_days,
            'social_connections_count': len(self.social_connections),
            'communication_probability': self.communication_probability
        }