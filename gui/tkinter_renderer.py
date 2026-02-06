"""
Renderer Tkinter - Fallback si Pygame non disponible
"""
import tkinter as tk
from tkinter import messagebox
from typing import List
from interfaces.renderer import IRenderer
from models.board import Board
from models.move import Move, Position
from models.types import Player, Piece
from models.game_state import GameState


class TkinterRenderer(IRenderer):
    """Moteur de rendu Tkinter (fallback)"""
    
    def __init__(self, cell_size: int = 60):
        self.cell_size = cell_size
        self.board_size = 8 * cell_size
        
        self.root = tk.Tk()
        self.root.title("Jeu de Dames - Tkinter")
        
        # Canvas pour le plateau
        self.canvas = tk.Canvas(
            self.root, 
            width=self.board_size, 
            height=self.board_size,
            bg='gray'
        )
        self.canvas.pack()
        
        # État
        self.selected_pos: Position | None = None
        self.legal_moves: List[Move] = []
        self.game_state: GameState | None = None
        self.chosen_move: Move | None = None
        
        self.canvas.bind('<Button-1>', self._on_click)
    
    def render(self, board: Board) -> None:
        """Affiche le plateau"""
        self.canvas.delete('all')
        self.game_state = GameState(board)
        self.legal_moves = self.game_state.generate_legal_moves()
        
        # Damier
        for row in range(8):
            for col in range(8):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                color = '#f0d9b5' if (row + col) % 2 == 0 else '#b58863'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
        
        # Pièces
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece:
                    self._draw_piece(row, col, piece[0], piece[1])
        
        # Surbrillance
        if self.selected_pos:
            row, col = self.selected_pos
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline='yellow', width=3)
        
        self.root.update()
    
    def _draw_piece(self, row: int, col: int, player: Player, piece_type: Piece) -> None:
        """Dessine une pièce"""
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 3
        
        color = 'white' if player == Player.WHITE else 'black'
        outline = 'black' if player == Player.WHITE else 'white'
        
        self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=color, outline=outline, width=2
        )
        
        if piece_type == Piece.KING:
            self.canvas.create_text(x, y, text='♔', font=('Arial', 20), fill='gold')
    
    def _on_click(self, event) -> None:
        """Gère les clics"""
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if not (0 <= row < 8 and 0 <= col < 8):
            return
        
        clicked_pos = (row, col)
        
        if self.selected_pos:
            # Chercher un coup
            for move in self.legal_moves:
                if move.start == self.selected_pos and move.end == clicked_pos:
                    self.chosen_move = move
                    return
            
            self.selected_pos = None
        else:
            # Sélectionner
            if any(move.start == clicked_pos for move in self.legal_moves):
                self.selected_pos = clicked_pos
    
    def wait_for_move(self, board: Board) -> Move:
        """Attend un coup"""
        self.chosen_move = None
        self.selected_pos = None
        
        while self.chosen_move is None:
            self.render(board)
            self.root.update()
        
        return self.chosen_move
    
    def show_message(self, message: str) -> None:
        """Affiche un message"""
        messagebox.showinfo("Information", message)
    
    def cleanup(self) -> None:
        """Nettoie les ressources"""
        try:
            self.root.destroy()
        except:
            pass
