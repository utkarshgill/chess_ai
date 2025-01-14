from abc import ABC, abstractmethod
import chess

class ChessAI(ABC):
    """Base class for all chess AI implementations."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def choose_move(self, board: chess.Board) -> chess.Move:
        """Choose the next move given the current board state.
        
        Args:
            board: Current chess board state
            
        Returns:
            The chosen move
        """
        pass
    
    @abstractmethod
    def train(self, games_data: list) -> None:
        """Train the AI using historical game data.
        
        Args:
            games_data: List of game records for training
        """
        pass
    
    def __str__(self) -> str:
        return f"{self.name} Chess AI" 