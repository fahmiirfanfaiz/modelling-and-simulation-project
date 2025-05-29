# gossip_simulation/config.py - Configuration management
from dataclasses import dataclass
from typing import Literal


@dataclass
class SimulationConfig:
    """Configuration class for gossip simulation parameters"""
    
    # Grid parameters
    width: int = 100
    height: int = 100
    
    # Spread probabilities
    spread_probability: float = 0.2          # Local spread probability
    believe_probability: float = 0.7         # Probability to believe gossip
    global_spread_probability: float = 0.15  # Global spread probability
    
    # Population parameters
    resistance_rate: float = 0.1           # Percentage of resistant agents
    initial_spreaders: int = 5              # Number of initial spreaders
    
    # Social network parameters
    network_type: Literal['small-world', 'scale-free'] = 'small-world'
    min_social_connections: int = 3
    max_social_connections: int = 15
    
    # Agent behavior parameters
    min_spread_days: int = 2
    max_spread_days: int = 6
    min_communication_prob: float = 0.1
    max_communication_prob: float = 0.4
    
    # Simulation parameters
    max_steps: int = 30
    
    # Visualization parameters
    animation_interval: int = 800
    save_animation: bool = False
    animation_filename: str = 'enhanced_gossip_simulation.mp4'
    
    def validate(self) -> bool:
        """Validate configuration parameters"""
        errors = []
        
        if self.width <= 0 or self.height <= 0:
            errors.append("Grid dimensions must be positive")
            
        if not (0 <= self.spread_probability <= 1):
            errors.append("Spread probability must be between 0 and 1")
            
        if not (0 <= self.believe_probability <= 1):
            errors.append("Believe probability must be between 0 and 1")
            
        if not (0 <= self.global_spread_probability <= 1):
            errors.append("Global spread probability must be between 0 and 1")
            
        if not (0 <= self.resistance_rate <= 1):
            errors.append("Resistance rate must be between 0 and 1")
            
        if self.initial_spreaders < 0:
            errors.append("Initial spreaders must be non-negative")
            
        if self.min_social_connections > self.max_social_connections:
            errors.append("Min social connections cannot exceed max social connections")
            
        if self.min_spread_days > self.max_spread_days:
            errors.append("Min spread days cannot exceed max spread days")
            
        if errors:
            for error in errors:
                print(f"Configuration Error: {error}")
            return False
            
        return True
    
    @classmethod
    def create_small_test_config(cls) -> 'SimulationConfig':
        """Create a small configuration for testing"""
        return cls(
            width=20,
            height=20,
            max_steps=15,
            initial_spreaders=2
        )
    
    @classmethod
    def create_large_simulation_config(cls) -> 'SimulationConfig':
        """Create a large configuration for detailed simulation"""
        return cls(
            width=150,
            height=150,
            max_steps=50,
            initial_spreaders=10,
            resistance_rate=0.1
        )