# gossip_simulation/states.py - State definitions and utilities
from enum import Enum
from typing import List, Dict


class GossipState(Enum):
    """Status agen dalam penyebaran gosip"""
    UNINFORMED = 0    # Belum tahu gosip (biru)
    SPREADER = 1    # Menyebarkan gosip (merah)
    DORMANT = 2     # Sudah bosan gosip (hijau)
    RESISTANT = 3   # Kebal gosip (abu-abu)
    
    @classmethod
    def get_color_mapping(cls) -> Dict[int, str]:
        """Get color mapping for visualization"""
        return {
            cls.UNINFORMED.value: '#87CEEB',   # Light blue
            cls.SPREADER.value: '#FF6B6B',   # Red
            cls.DORMANT.value: '#98FB98',    # Light green
            cls.RESISTANT.value: '#D3D3D3'   # Light gray
        }
    
    @classmethod
    def get_state_labels(cls) -> Dict[int, str]:
        """Get state labels for visualization"""
        return {
            cls.UNINFORMED.value: 'Uninformed',
            cls.SPREADER.value: 'Spreader', 
            cls.DORMANT.value: 'Dormant',
            cls.RESISTANT.value: 'Resistant'
        }
    
    @classmethod
    def get_active_states(cls) -> List['GossipState']:
        """Get states that can participate in gossip spread"""
        return [cls.UNINFORMED, cls.SPREADER, cls.DORMANT]
    
    @classmethod
    def get_spreading_states(cls) -> List['GossipState']:
        """Get states that actively spread gossip"""
        return [cls.SPREADER]
    
    @classmethod
    def get_receptive_states(cls) -> List['GossipState']:
        """Get states that can receive gossip"""
        return [cls.UNINFORMED]