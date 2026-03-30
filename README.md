Chess

A complete, feature-rich chess game built with Python and Pygame, featuring modern UI design and comprehensive gameplay mechanics.

Game Features

Core Gameplay
- Complete Chess Rules: Full implementation of all standard chess rules
- Piece Movement: Accurate movement patterns for all pieces (pawn, rook, knight, bishop, queen, king)
- Special Moves: En passant, castling, and pawn promotion
- Check & Checkmate Detection: Automatic detection of check and checkmate conditions
- Turn-based Play: Alternating white and black turns with enforcement

User Interface
- Modern Design: Sleek dark theme with professional color scheme
- Visual Chess Board: Classic light/dark square pattern with elegant borders
- Unicode Piece Rendering: High-quality chess piece symbols with distinct white/black coloring
- Interactive Selection: Click-to-select pieces with blue highlight
- Move Indicators: Green circles show valid moves for selected pieces
- Responsive Layout: Properly centered and scaled elements

Game Management
- Menu System: Professional main menu with Start Game, Reset Game, and Quit options
- Game Reset: Reset current game or start fresh match anytime
- Undo Feature: Undo last move with 'U' key for mistake correction
- Navigation: Keyboard (arrow keys, Enter) and mouse support

Timing & Status
- Real-time Timers: Cumulative time tracking for both players
- Turn Indicator: Clear display of whose turn it is
- Game Status: Visual game over screen with restart options
- Performance: Smooth 60 FPS gameplay

Getting Started

Prerequisites
- Python 3.6 or higher
- Pygame library

Installation
1. Ensure Python is installed on your system
2. Install Pygame:
   pip install pygame

Running the Game
1. Download or clone the repository
2. Navigate to the project directory
3. Run the game:
   python Chess.py

How to Play

Menu Navigation
- Use arrow keys or mouse to select menu options
- Press Enter or click to confirm selection

During Gameplay
- Click on a piece to select it (blue highlight appears)
- Click on a destination square to move (green circles show valid moves)
- U key: Undo last move
- R key: Reset current game
- ESC key: Return to main menu

Controls Summary
- Mouse: Select pieces and make moves
- Arrow Keys: Navigate menus
- Enter: Confirm menu selection
- U: Undo last move
- R: Reset game
- ESC: Return to menu

Visual Design

Color Scheme
- Background: Dark gray (#232323)
- Board Light: Cream (#F0D9B5)
- Board Dark: Brown (#B58863)
- Accent Blue: Steel blue for selections (#4682B4)
- Accent Green: Forest green for valid moves (#228B22)
- Highlight: Gold for active elements (#FFD700)

Typography
- Title: Arial Bold 80pt with shadow effect
- Menu: Arial Bold 36pt with rounded backgrounds
- Pieces: Arial Bold 70pt Unicode symbols
- UI Elements: Arial 24pt/18pt for timers and status

Technical Architecture

Game State Management
- Board Representation: 8x8 list of strings for piece positions
- State Variables: Comprehensive tracking of game state, timers, and flags
- Move Validation: Real-time legality checking with check prevention

Rendering System
- Layered Drawing: Background → Board → Pieces → UI overlays
- Efficient Updates: Only redraw changed elements per frame
- Font Management: Multiple font sizes and styles for different UI elements

Input Handling
- Event-driven: Pygame event loop for keyboard and mouse input
- State-based: Different input handling for menu vs gameplay
- Validation: Input bounds checking and move legality verification

Known Limitations

- Board Representation: Uses string-based 2D list (functional but not optimal for advanced features)
- Stalemate Detection: Not implemented (game continues after checkmate)
- Promotion Choice: Auto-promotes to queen only
- Save/Load: No game state persistence
- AI Opponent: Single-player only (no computer opponent)
- Time Controls: Cumulative timing only (no increment or time limits)
- Drag & Drop: Click-to-move only (no drag interface)
- Sound Effects: No audio feedback

Development Notes

Code Structure
- Main Loop: Event handling, game logic, and rendering
- Helper Functions: Move validation, piece logic, UI rendering
- State Management: Global variables for game state
- Modular Design: Separated concerns for maintainability

Performance Considerations
- 60 FPS Cap: Smooth animation and responsive input
- Efficient Rendering: Minimal redraw operations
- Memory Management: Lightweight data structures

Future Enhancements
- Add stalemate detection
- Implement save/load functionality
- Add AI opponent with difficulty levels
- Include sound effects and music
- Add drag-and-drop piece movement
- Implement different time controls
- Add game replay/analysis features

Author

Pranav Mohanty

A passionate developer creating engaging gaming experiences with clean, maintainable code.

License

This project is open source and available under the MIT License.

Experience the classic game of chess with modern UI design and comprehensive features! 