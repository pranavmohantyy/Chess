3/22/26


Project: Chess


Description: A Chess game run through python locally on your computer 


Setup / Requirements: Python, Pip, Pygame, 


How to run: TBD when game is fully finished, but for now, download the folder and run through terminal


Project structure: TBD	


Current Features
	•	8x8 chessboard rendering
	•	Piece display with better visuals (image-based / Unicode glyphs)
	•	Click-to-select and move system
	•	Full movement rules for all pieces (pawn, rook, knight, bishop, queen, king)
	•	Turn enforcement (white/black)
	•	Self-check prevention (illegal moves leaving king in check are blocked)
	•	Pawn promotion to queen at final rank
	•	Check detection status messages
	•	Legal move highlighting (green circles on valid squares when piece selected)
	•	Checkmate detection and game end
	•	Special rules: en passant and castling
	•	Menu screen with Start Game, Reset Game, and Quit options
	•	Reset game via menu or R key during play
	•	Cumulative time tracking for each player
	•	Real-time timer display during gameplay





Known issues / limitations: 
    •	The board is still represented as a 2D list of strings, which limits flexibility for advanced state tracking and move history
	•	Stalemate detection is not implemented
	•	Promotion choice UI is absent (auto-queen only)
	•	No undo/redo, save/load, or AI opponent
	•	No time limit enforcement (timers are cumulative only)
	•	Drag-and-drop UI not supported (click-to-move only)
	•	No sound effects yet
	
Author: Pranav Mohanty 