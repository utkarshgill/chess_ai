import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict
import numpy as np

class MetricsAnalyzer:
    """Analyzes and visualizes chess AI performance metrics."""
    
    def __init__(self, results_df: pd.DataFrame):
        self.results_df = results_df
        
    def get_win_rates(self) -> pd.DataFrame:
        """Calculate win rates for each AI.
        
        Returns:
            DataFrame with wins, losses, draws, and win rate for each AI
        """
        stats = []
        
        for ai_name in set(self.results_df['white_ai'].unique()) | set(self.results_df['black_ai'].unique()):
            # Games as white
            white_games = self.results_df[self.results_df['white_ai'] == ai_name]
            white_wins = len(white_games[white_games['winner'] == 'white'])
            white_losses = len(white_games[white_games['winner'] == 'black'])
            white_draws = len(white_games[white_games['winner'] == 'draw'])
            
            # Games as black
            black_games = self.results_df[self.results_df['black_ai'] == ai_name]
            black_wins = len(black_games[black_games['winner'] == 'black'])
            black_losses = len(black_games[black_games['winner'] == 'white'])
            black_draws = len(black_games[black_games['winner'] == 'draw'])
            
            total_games = len(white_games) + len(black_games)
            total_wins = white_wins + black_wins
            total_losses = white_losses + black_losses
            total_draws = white_draws + black_draws
            
            win_rate = (total_wins + 0.5 * total_draws) / total_games if total_games > 0 else 0
            
            stats.append({
                'ai_name': ai_name,
                'games_played': total_games,
                'wins': total_wins,
                'losses': total_losses,
                'draws': total_draws,
                'win_rate': win_rate
            })
            
        return pd.DataFrame(stats).sort_values('win_rate', ascending=False)
    
    def get_average_game_length(self) -> pd.DataFrame:
        """Calculate average game length for each AI.
        
        Returns:
            DataFrame with average moves per game for each AI
        """
        stats = []
        
        for ai_name in set(self.results_df['white_ai'].unique()) | set(self.results_df['black_ai'].unique()):
            white_games = self.results_df[self.results_df['white_ai'] == ai_name]
            black_games = self.results_df[self.results_df['black_ai'] == ai_name]
            
            all_games = pd.concat([white_games, black_games])
            avg_moves = all_games['moves'].mean()
            
            stats.append({
                'ai_name': ai_name,
                'average_moves': avg_moves
            })
            
        return pd.DataFrame(stats)
    
    def plot_win_rates(self, save_path: str = None):
        """Plot win rates for each AI.
        
        Args:
            save_path: Optional path to save the plot
        """
        win_rates = self.get_win_rates()
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(win_rates['ai_name'], win_rates['win_rate'])
        plt.title('Chess AI Win Rates')
        plt.xlabel('AI Name')
        plt.ylabel('Win Rate')
        plt.xticks(rotation=45)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom')
            
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    
    def plot_game_lengths(self, save_path: str = None):
        """Plot average game lengths for each AI.
        
        Args:
            save_path: Optional path to save the plot
        """
        game_lengths = self.get_average_game_length()
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(game_lengths['ai_name'], game_lengths['average_moves'])
        plt.title('Average Game Length by AI')
        plt.xlabel('AI Name')
        plt.ylabel('Average Moves per Game')
        plt.xticks(rotation=45)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom')
            
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        plt.close() 