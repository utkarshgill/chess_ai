import chess
import time
from typing import List, Tuple, Dict
from dataclasses import dataclass
import pandas as pd
from tqdm import tqdm

from ..chess_engine.base import ChessAI

@dataclass
class GameResult:
    """Stores the result of a single game."""
    white_ai: str
    black_ai: str
    winner: str  # 'white', 'black', or 'draw'
    moves: int
    time_white: float
    time_black: float
    final_fen: str

class ExperimentRunner:
    """Runs experiments comparing different chess AIs."""
    
    def __init__(self):
        self.results: List[GameResult] = []
    
    def run_match(self, white_ai: ChessAI, black_ai: ChessAI, 
                 time_limit: float = 1.0) -> GameResult:
        """Run a single match between two AIs.
        
        Args:
            white_ai: AI playing as white
            black_ai: AI playing as black
            time_limit: Maximum time per move in seconds
            
        Returns:
            GameResult containing match statistics
        """
        board = chess.Board()
        moves = 0
        time_white = 0.0
        time_black = 0.0
        
        while not board.is_game_over():
            current_ai = white_ai if board.turn else black_ai
            start_time = time.time()
            
            try:
                move = current_ai.choose_move(board)
                elapsed = time.time() - start_time
                
                if elapsed > time_limit:
                    # AI took too long, forfeit
                    winner = 'black' if board.turn else 'white'
                    break
                    
                if board.turn:
                    time_white += elapsed
                else:
                    time_black += elapsed
                    
                board.push(move)
                moves += 1
                
            except Exception as e:
                # AI made an illegal move or crashed
                winner = 'black' if board.turn else 'white'
                break
        
        if board.is_checkmate():
            winner = 'black' if board.turn else 'white'
        elif board.is_stalemate() or board.is_insufficient_material():
            winner = 'draw'
            
        return GameResult(
            white_ai=white_ai.name,
            black_ai=black_ai.name,
            winner=winner,
            moves=moves,
            time_white=time_white,
            time_black=time_black,
            final_fen=board.fen()
        )
    
    def run_tournament(self, ais: List[ChessAI], games_per_pair: int = 2,
                      time_limit: float = 1.0) -> pd.DataFrame:
        """Run a round-robin tournament between multiple AIs.
        
        Args:
            ais: List of AIs to compete
            games_per_pair: Number of games for each AI pair (will play both colors)
            time_limit: Maximum time per move in seconds
            
        Returns:
            DataFrame with tournament results
        """
        total_games = len(ais) * (len(ais) - 1) * games_per_pair
        
        with tqdm(total=total_games, desc="Playing matches") as pbar:
            for i, ai1 in enumerate(ais):
                for ai2 in ais[i+1:]:
                    for _ in range(games_per_pair):
                        # Each pair plays both as white and black
                        self.results.append(
                            self.run_match(ai1, ai2, time_limit))
                        self.results.append(
                            self.run_match(ai2, ai1, time_limit))
                        pbar.update(2)
                        
        return self.get_results_df()
    
    def get_results_df(self) -> pd.DataFrame:
        """Convert results to a pandas DataFrame for analysis."""
        return pd.DataFrame([vars(r) for r in self.results]) 