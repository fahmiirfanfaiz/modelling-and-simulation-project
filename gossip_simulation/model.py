# gossip_simulation/model.py - Main simulation model
import mesa
from typing import List

from .config import SimulationConfig
from .states import GossipState
from .agent import PersonAgent
from .network import SocialNetworkBuilder


class GossipModel(mesa.Model):
    """Model simulasi penyebaran gosip"""
    
    def __init__(self, config: SimulationConfig):
        super().__init__()
        
        # Validate configuration
        if not config.validate():
            raise ValueError("Invalid configuration provided")
        
        self.config = config
        self.step_count = 0
        
        # Setup Mesa components
        self.grid = mesa.space.MultiGrid(config.width, config.height, torus=True)
        self.schedule = mesa.time.RandomActivation(self)
        
        # Setup data collection
        self._setup_data_collector()
        
        # Create agents and social network
        self._create_agents()
        self._create_social_network()
        self._set_initial_spreaders()
        
        # Collect initial data
        self.datacollector.collect(self)
        self.running = True
    
    def _setup_data_collector(self) -> None:
        """Setup data collector for tracking simulation metrics"""
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Ignorant": lambda m: self._count_agents_by_state(GossipState.IGNORANT),
                "Spreader": lambda m: self._count_agents_by_state(GossipState.SPREADER),
                "Stifler": lambda m: self._count_agents_by_state(GossipState.STIFLER),
                "Resistant": lambda m: self._count_agents_by_state(GossipState.RESISTANT),
                "Total_Informed": lambda m: (
                    self._count_agents_by_state(GossipState.SPREADER) + 
                    self._count_agents_by_state(GossipState.STIFLER)
                )
            }
        )
    
    def _count_agents_by_state(self, state: GossipState) -> int:
        """Count agents in a specific state"""
        return sum(1 for agent in self.schedule.agents if agent.state == state)
    
    def _create_agents(self) -> None:
        """Create and place agents on the grid"""
        agent_id = 0
        
        for x in range(self.config.width):
            for y in range(self.config.height):
                # Determine if agent is resistant
                is_resistant = self.random.random() < self.config.resistance_rate
                
                agent = PersonAgent(agent_id, self, is_resistant)
                self.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))
                agent_id += 1
    
    def _create_social_network(self) -> None:
        """Create social network connections between agents"""
        agents = list(self.schedule.agents)
        SocialNetworkBuilder.create_network(agents, self.config)
    
    def _set_initial_spreaders(self) -> None:
        """Set initial spreaders from non-resistant agents"""
        non_resistant_agents = [
            agent for agent in self.schedule.agents 
            if agent.state != GossipState.RESISTANT
        ]
        
        if not non_resistant_agents:
            print("Warning: No non-resistant agents available for initial spreading")
            return
        
        num_spreaders = min(self.config.initial_spreaders, len(non_resistant_agents))
        initial_spreaders = self.random.sample(non_resistant_agents, num_spreaders)
        
        for agent in initial_spreaders:
            agent.state = GossipState.SPREADER
    
    def step(self) -> None:
        """Execute one step of the simulation"""
        self.step_count += 1
        self.schedule.step()
        self.datacollector.collect(self)
        
        # Check if simulation should stop
        if self._should_stop_simulation():
            self.running = False
    
    def _should_stop_simulation(self) -> bool:
        """Determine if simulation should stop"""
        spreader_count = self._count_agents_by_state(GossipState.SPREADER)
        return spreader_count == 0 or self.step_count >= self.config.max_steps
    
    def get_simulation_summary(self) -> dict:
        """Get summary of current simulation state"""
        total_agents = len(self.schedule.agents)
        
        return {
            'step': self.step_count,
            'total_agents': total_agents,
            'ignorant': self._count_agents_by_state(GossipState.IGNORANT),
            'spreader': self._count_agents_by_state(GossipState.SPREADER),
            'stifler': self._count_agents_by_state(GossipState.STIFLER),
            'resistant': self._count_agents_by_state(GossipState.RESISTANT),
            'informed_percentage': (
                (self._count_agents_by_state(GossipState.SPREADER) + 
                 self._count_agents_by_state(GossipState.STIFLER)) / 
                (total_agents - self._count_agents_by_state(GossipState.RESISTANT)) * 100
                if total_agents - self._count_agents_by_state(GossipState.RESISTANT) > 0 else 0
            ),
            'is_running': self.running
        }
    
    def get_agents_by_state(self, state: GossipState) -> List[PersonAgent]:
        """Get all agents in a specific state"""
        return [agent for agent in self.schedule.agents if agent.state == state]