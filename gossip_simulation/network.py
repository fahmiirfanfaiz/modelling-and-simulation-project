# gossip_simulation/network.py - Social network creation and management
import networkx as nx
from typing import List, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from .agent import PersonAgent
    from .config import SimulationConfig


class SocialNetworkBuilder:
    """Builder class for creating social networks"""
    
    @staticmethod
    def create_network(agents: List['PersonAgent'], config: 'SimulationConfig') -> None:
        """Create social network connections between agents"""
        if config.network_type == 'small-world':
            SocialNetworkBuilder._create_small_world_network(agents, config)
        elif config.network_type == 'scale-free':
            SocialNetworkBuilder._create_scale_free_network(agents, config)
        else:
            raise ValueError(f"Unknown network type: {config.network_type}")
    
    @staticmethod
    def _create_small_world_network(agents: List['PersonAgent'], config: 'SimulationConfig') -> None:
        """Create small-world network using Watts-Strogatz model"""
        num_agents = len(agents)
        
        # Create small-world graph
        G = nx.watts_strogatz_graph(n=num_agents, k=6, p=0.1)
        
        # Assign connections to agents
        SocialNetworkBuilder._assign_connections_from_graph(agents, G)
    
    @staticmethod
    def _create_scale_free_network(agents: List['PersonAgent'], config: 'SimulationConfig') -> None:
        """Create scale-free network using Barabási-Albert model"""
        num_agents = len(agents)
        
        # Create scale-free graph
        G = nx.barabasi_albert_graph(n=num_agents, m=3)
        
        # Assign connections to agents
        SocialNetworkBuilder._assign_connections_from_graph(agents, G)
    
    @staticmethod
    def _assign_connections_from_graph(agents: List['PersonAgent'], G: nx.Graph) -> None:
        """Assign social connections to agents based on NetworkX graph"""
        for i, agent in enumerate(agents):
            neighbors_idx = list(G.neighbors(i))
            connections = [agents[j] for j in neighbors_idx if agents[j] != agent]
            agent.create_social_connections(connections)
    
    @staticmethod
    def get_network_statistics(agents: List['PersonAgent']) -> dict:
        """Calculate network statistics"""
        connection_counts = [len(agent.social_connections) for agent in agents 
                           if agent.state.name != 'RESISTANT']
        
        if not connection_counts:
            return {
                'total_agents': len(agents),
                'avg_connections': 0,
                'min_connections': 0,
                'max_connections': 0,
                'std_connections': 0
            }
        
        return {
            'total_agents': len(agents),
            'avg_connections': np.mean(connection_counts),
            'min_connections': np.min(connection_counts),
            'max_connections': np.max(connection_counts),
            'std_connections': np.std(connection_counts)
        }


class NetworkAnalyzer:
    """Analyzer for social network properties"""
    
    @staticmethod
    def analyze_network_structure(agents: List['PersonAgent']) -> dict:
        """Analyze the structure of the social network"""
        # Create NetworkX graph from agent connections
        G = nx.Graph()
        
        # Add nodes
        for agent in agents:
            G.add_node(agent.unique_id)
        
        # Add edges
        for agent in agents:
            for connection in agent.social_connections:
                G.add_edge(agent.unique_id, connection.unique_id)
        
        # Calculate network metrics
        analysis = {
            'num_nodes': G.number_of_nodes(),
            'num_edges': G.number_of_edges(),
            'density': nx.density(G),
            'is_connected': nx.is_connected(G)
        }
        
        if nx.is_connected(G):
            analysis.update({
                'average_path_length': nx.average_shortest_path_length(G),
                'diameter': nx.diameter(G),
                'clustering_coefficient': nx.average_clustering(G)
            })
        else:
            # For disconnected graphs
            largest_cc = max(nx.connected_components(G), key=len)
            largest_subgraph = G.subgraph(largest_cc)
            
            analysis.update({
                'num_connected_components': nx.number_connected_components(G),
                'largest_component_size': len(largest_cc),
                'average_path_length': nx.average_shortest_path_length(largest_subgraph) if len(largest_cc) > 1 else 0,
                'diameter': nx.diameter(largest_subgraph) if len(largest_cc) > 1 else 0,
                'clustering_coefficient': nx.average_clustering(G)
            })
        
        return analysis