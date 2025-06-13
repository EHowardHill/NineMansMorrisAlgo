import random
from helper import board, connections, mills, count_pieces

class MorrisAI:
    def __init__(self, difficulty=1):
        self.difficulty = difficulty
        self.player = '2'
        self.opponent = '1'
    
    def get_valid_positions(self):
        """Get all empty positions on the board"""
        return [i for i in range(24) if board[i] == ' ']
    
    def get_player_pieces(self, player):
        """Get all positions where player has pieces"""
        return [i for i in range(24) if board[i] == player]
    
    def get_valid_moves(self, player):
        """Get all valid moves for a player"""
        pieces = self.get_player_pieces(player)
        moves = []
        
        for piece in pieces:
            for adjacent in connections[piece]:
                if board[adjacent] == ' ':
                    moves.append((piece, adjacent))
        return moves
    
    def get_valid_flights(self, player):
        """Get all valid flights for a player (can move to any empty position)"""
        pieces = self.get_player_pieces(player)
        empty = self.get_valid_positions()
        moves = []
        
        for piece in pieces:
            for empty_pos in empty:
                moves.append((piece, empty_pos))
        return moves
    
    def check_potential_mill(self, pos, player):
        """Check if placing/moving to position would form a mill"""
        temp_board = board[:]
        temp_board[pos] = player
        
        # Check all mill patterns for this position
        for mill in mills:
            if pos in mill:
                if all(temp_board[p] == player for p in mill):
                    return True
        return False
    
    def check_block_mill(self, pos):
        """Check if placing here would block opponent's mill"""
        # Try placing opponent piece to see if it forms mill
        temp_board = board[:]
        temp_board[pos] = self.opponent
        
        for mill in mills:
            if pos in mill:
                if all(temp_board[p] == self.opponent for p in mill):
                    return True
        return False
    
    def evaluate_position(self, pos):
        """Evaluate how good a position is (higher = better)"""
        score = 0
        
        # Center positions are generally better
        center_positions = [9, 10, 11, 12, 13, 14, 15, 16]
        if pos in center_positions:
            score += 2
        
        # Corner positions can be strategic
        corner_positions = [0, 2, 6, 8, 16, 18, 22, 23]
        if pos in corner_positions:
            score += 1
        
        # Count potential mills through this position
        mill_potential = 0
        for mill in mills:
            if pos in mill:
                empty_count = sum(1 for p in mill if board[p] == ' ')
                ai_count = sum(1 for p in mill if board[p] == self.player)
                if empty_count > 0 and ai_count > 0:
                    mill_potential += 1
        
        score += mill_potential
        return score
    
    def minimax_evaluate_board(self):
        """Simple board evaluation for minimax"""
        ai_pieces = count_pieces(self.player)
        opponent_pieces = count_pieces(self.opponent)
        
        # Basic evaluation: piece advantage
        score = (ai_pieces - opponent_pieces) * 10
        
        # Add bonus for mills and potential mills
        ai_positions = self.get_player_pieces(self.player)
        for pos in ai_positions:
            score += self.evaluate_position(pos)
        
        return score
    
    def make_move(self, phase, pieces_left=0):
        """Make AI move based on difficulty and phase"""
        if phase == 'placing':
            return self.make_placing_move()
        elif phase == 'moving':
            return self.make_moving_move()
        elif phase == 'flying':
            return self.make_flying_move()
    
    def make_placing_move(self):
        """AI logic for placing phase"""
        valid_positions = self.get_valid_positions()
        
        if self.difficulty == 1:
            # Level 1: Random placement
            return random.choice(valid_positions)
        
        elif self.difficulty == 2:
            # Level 2: Try to form mills, block opponent
            # First priority: complete a mill
            for pos in valid_positions:
                if self.check_potential_mill(pos, self.player):
                    return pos
            
            # Second priority: block opponent mill
            for pos in valid_positions:
                if self.check_block_mill(pos):
                    return pos
            
            # Otherwise random
            return random.choice(valid_positions)
        
        elif self.difficulty >= 3:
            # Level 3+: Strategic placement with position evaluation
            best_pos = None
            best_score = -1000
            
            for pos in valid_positions:
                score = 0
                
                # Highest priority: form mill
                if self.check_potential_mill(pos, self.player):
                    score += 100
                
                # High priority: block opponent mill
                if self.check_block_mill(pos):
                    score += 50
                
                # Medium priority: position value
                score += self.evaluate_position(pos) * 5
                
                # Level 4+: Look ahead
                if self.difficulty >= 4:
                    # Simulate placing here and evaluate resulting position
                    board[pos] = self.player
                    score += self.minimax_evaluate_board()
                    board[pos] = ' '
                
                if score > best_score:
                    best_score = score
                    best_pos = pos
            
            return best_pos or random.choice(valid_positions)
    
    def make_moving_move(self):
        """AI logic for moving phase"""
        valid_moves = self.get_valid_moves(self.player)
        
        if not valid_moves:
            return None
        
        if self.difficulty == 1:
            # Level 1: Random move
            return random.choice(valid_moves)
        
        elif self.difficulty == 2:
            # Level 2: Try to form mills, block opponent
            for from_pos, to_pos in valid_moves:
                if self.check_potential_mill(to_pos, self.player):
                    return (from_pos, to_pos)
            
            # Try to block opponent
            for from_pos, to_pos in valid_moves:
                if self.check_block_mill(to_pos):
                    return (from_pos, to_pos)
            
            return random.choice(valid_moves)
        
        elif self.difficulty >= 3:
            # Level 3+: Strategic moving
            best_move = None
            best_score = -1000
            
            for from_pos, to_pos in valid_moves:
                score = 0
                
                # Simulate move
                board[from_pos] = ' '
                board[to_pos] = self.player
                
                # Check if this forms a mill
                if self.check_potential_mill(to_pos, self.player):
                    score += 100
                
                # Check if this blocks opponent mill
                board[to_pos] = ' '
                if self.check_block_mill(to_pos):
                    score += 50
                board[to_pos] = self.player
                
                # Position evaluation
                score += self.evaluate_position(to_pos) * 3
                score -= self.evaluate_position(from_pos) * 2
                
                # Level 4+: Board evaluation
                if self.difficulty >= 4:
                    score += self.minimax_evaluate_board()
                
                # Level 5: More sophisticated evaluation
                if self.difficulty == 5:
                    # Consider opponent's responses
                    opponent_moves = self.get_valid_moves(self.opponent)
                    threat_score = 0
                    for opp_from, opp_to in opponent_moves[:5]:  # Check first 5 moves
                        board[opp_from] = ' '
                        board[opp_to] = self.opponent
                        if self.check_potential_mill(opp_to, self.opponent):
                            threat_score -= 30
                        board[opp_from] = self.opponent
                        board[opp_to] = ' '
                    score += threat_score
                
                # Restore board
                board[to_pos] = ' '
                board[from_pos] = self.player
                
                if score > best_score:
                    best_score = score
                    best_move = (from_pos, to_pos)
            
            return best_move or random.choice(valid_moves)
    
    def make_flying_move(self):
        """AI logic for flying phase"""
        valid_moves = self.get_valid_flights(self.player)
        
        if not valid_moves:
            return None
        
        if self.difficulty == 1:
            return random.choice(valid_moves)
        
        # For all levels 2+, prioritize forming mills in flying phase
        best_move = None
        best_score = -1000
        
        for from_pos, to_pos in valid_moves:
            score = 0
            
            # Simulate move
            board[from_pos] = ' '
            board[to_pos] = self.player
            
            if self.check_potential_mill(to_pos, self.player):
                score += 100
            
            score += self.evaluate_position(to_pos) * 2
            
            if self.difficulty >= 4:
                score += self.minimax_evaluate_board()
            
            # Restore board
            board[to_pos] = ' '
            board[from_pos] = self.player
            
            if score > best_score:
                best_score = score
                best_move = (from_pos, to_pos)
        
        return best_move or random.choice(valid_moves)
    
    def choose_piece_to_remove(self):
        """Choose which opponent piece to remove when mill is formed"""
        opponent_pieces = self.get_player_pieces(self.opponent)
        
        if self.difficulty == 1:
            return random.choice(opponent_pieces)
        
        # For higher difficulties, prioritize removing pieces that:
        # 1. Are part of opponent mills
        # 2. Are in strategic positions
        # 3. Reduce opponent's mobility
        
        best_target = None
        best_score = -1000
        
        for piece in opponent_pieces:
            score = 0
            
            # Check if removing this breaks opponent mill
            board[piece] = ' '
            mills_broken = 0
            for mill in mills:
                if piece in mill:
                    if all(board[p] == self.opponent for p in mill if p != piece):
                        mills_broken += 1
            board[piece] = self.opponent
            score += mills_broken * 50
            
            # Prefer removing pieces from good positions
            score += self.evaluate_position(piece) * 3
            
            # Level 4+: Consider mobility impact
            if self.difficulty >= 4:
                # Count how many moves opponent loses by removing this piece
                board[piece] = ' '
                moves_before = len(self.get_valid_moves(self.opponent))
                board[piece] = self.opponent
                moves_after = len(self.get_valid_moves(self.opponent))
                score += (moves_after - moves_before) * 2
            
            if score > best_score:
                best_score = score
                best_target = piece
        
        return best_target or random.choice(opponent_pieces)