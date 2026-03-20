3/19/26


Project: Chess


Description: A Chess game run through python locally on your computer 


Setup / Requirements: Python, Pip, Pygame, 


How to run: TBD when game is fully finished, but for now, download the folder and run through terminal


Project structure: TBD


Current Features
	•	8x8 chessboard rendering
	•	Piece display (text-based)
	•	Click-to-select and move system
	•	Full movement rules for all pieces (pawn, rook, knight, bishop, queen, king)
	•	Turn enforcement (white/black)
	•	Self-check prevention (illegal moves leaving king in check are blocked)
	•	Pawn promotion to queen at final rank
	•	Check detection status messages



Known issues / limitations: 
    •	The board is represented as a 2D list of strings, which limits flexibility for tracking piece-specific state and move history
	•	Castling and en passant are not implemented
	•	Checkmate/stalemate detection is not implemented
	•	Promotion choice UI is absent (auto-queen only)
	•	No undo/redo, save/load, or AI opponent
	•	Input handling is still basic; drag, misclicks, and hover behavior can be unstable


Author: Pranav Mohanty 