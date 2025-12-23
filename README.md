# 🐤 Flappy Bird - Python Edition

A fully-featured Flappy Bird clone developed in Python using Pygame and other powerful libraries. This project demonstrates game development fundamentals, modular code architecture, and collaborative programming practices.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.x-green.svg)](https://www.pygame.org/)


---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Technologies & Libraries](#technologies--libraries)
- [Project Architecture](#project-architecture)
- [Getting Started](#getting-started)
- [How to Play](#how-to-play)
- [Contributing](#contributing)
- [The Team](#the-team)

---

## 🎮 About the Project

This is a modern recreation of the classic **Flappy Bird** game, built entirely in Python. The project focuses on clean code organization, efficient game loop management, and extensible architecture. Currently supporting single-player mode, we're actively developing multiplayer functionality with networking capabilities.

**Project Goals:**
- Provide a learning resource for game development with Python
- Demonstrate modular code architecture and design patterns
- Create an extensible platform for additional features and game modes
- Build a foundation for real-time multiplayer gaming

---

## ✨ Features

### Current Features
- ✅ **Smooth Gameplay**: 60 FPS game loop with responsive controls
- ✅ **Collision Detection**: Precise hitbox system for pipes, ground, and sky
- ✅ **Dynamic Obstacles**: Procedurally generated pipes with randomized gaps
- ✅ **Score Tracking**: Real-time score display and high score persistence
- ✅ **Sound Effects**: Immersive audio feedback for actions and events
- ✅ **Custom Graphics**: Pixel-art styled sprites and backgrounds
- ✅ **Gravity Physics**: Realistic bird flight mechanics with acceleration

### Coming Soon
- 🚧 **Multiplayer Mode**: Real-time competitive gameplay
- 🚧 **Network Integration**: Client-server architecture for online play
- 🚧 **Leaderboards**: Global and local high score rankings
- 🚧 **Power-ups**: Special abilities and game modifiers

---

## 🛠️ Technologies & Libraries

This project leverages several Python libraries to achieve its functionality:

| Library | Purpose | Usage in Project |
|---------|---------|------------------|
| **Pygame** | Game engine and graphics | Rendering sprites, handling events, and managing game loop |
| **Tkinter** | GUI framework | Creating menus and dialogs |
| **PIL (Pillow)** | Image processing | Loading and manipulating sprite images |
| **Math** | Mathematical operations | Calculating trajectories and collision angles |
| **Ctypes** | C library interfacing | System-level operations and performance optimization |
| **Sys** | System operations | Command-line arguments and exit handling |
| **Pickle** | Data serialization | Saving and loading game state and high scores |

---

## 🏗️ Project Architecture

The codebase is organized into modular components for maintainability and scalability:

```
Flappy-Bird/
│
├── main.py                 # Entry point - initializes and runs the game
├── score.py               # Score management and persistence system
├── background.jpeg        # Background sprite asset
├── pixel.TTF             # Custom font for text rendering
│
├── __pycache__/          # Python bytecode cache
├── pipes/                # Pipe generation and movement logic
├── sound/                # Audio files and sound manager
├── start_page/           # Main menu and UI screens
├── present/              # Asset presentation layer
├── version_two/          # Alternative implementation/features
│
└── multiplayer/          # 🚧 Work in progress
    ├── client.py         # Client-side networking logic
    ├── server.py         # Server implementation
    └── protocol.py       # Communication protocol definitions
```

### Component Breakdown

#### 🐦 **Bird Module**
Handles all bird-related functionality:
- Bird sprite rendering and animation
- Gravity simulation and jumping mechanics
- Bird state management (flying, falling, dead)
- Position and velocity calculations

#### 💥 **Collision Module**
Manages collision detection:
- Hitbox calculations for bird, pipes, ground, and ceiling
- Pixel-perfect collision detection algorithms
- Game-over state triggering
- Boundary checking

#### 🔧 **Pipes Module**
Controls obstacle generation:
- Random pipe pair generation with configurable gaps
- Horizontal scrolling mechanics
- Pipe recycling for memory efficiency
- Difficulty scaling based on score

#### 🔊 **Sounds Module**
Audio management system:
- Sound effect playback (wing flap, collision, scoring)
- Background music looping
- Volume control
- Audio channel management

#### 📊 **Score Module**
Score tracking and persistence:
- Real-time score display during gameplay
- High score saving using pickle serialization
- Score calculation based on passed obstacles
- End-game score presentation

#### 🎨 **Start Page Module**
Entry point and main menu:
- Game entry point with welcoming interface
- Animated start screen with visual effects
- "Start Game" button and menu navigation
- Title display with custom pixel font
- Smooth transitions to gameplay
- Initial game state setup

#### 🎨 **Start Page Module**
Entry point and main menu:
- Game entry point with welcoming interface
- Animated start screen with visual effects
- "Start Game" button and menu navigation
- Title display with custom pixel font
- Smooth transitions to gameplay
- Initial game state setup

#### 🎯 **Main Module**
Core game controller:
- Initializes Pygame and game components
- Manages the main game loop (update, render, events)
- Coordinates interactions between all modules
- Handles game states (menu, playing, game over)
- Frame rate management and timing

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.7+** installed on your system
- **pip** package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Mawadda0/Flappy-Bird.git
cd Flappy-Bird
```

2. **Install required dependencies**
```bash
pip install pygame pillow
```

3. **Run the game**
```bash
python main.py
```

### Optional: Create a Virtual Environment

For isolated dependency management:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install pygame pillow
```

---

## 🎮 How to Play

### Controls
- **SPACE** or **UP ARROW**: Make the bird flap/jump
- **ESC**: Pause game or return to menu

### Objective
- Navigate the bird through gaps between pipes
- Each successful pass awards 1 point
- Avoid colliding with pipes, ground, or ceiling
- Try to beat your high score!

### Tips
- Timing is everything - find your rhythm
- Short, quick taps work better than holding the key
- Anticipate upcoming pipe positions
- Stay calm and focus on one pipe at a time

---

## 🤝 Contributing

We **welcome and encourage contributions** from the community! Whether you're fixing bugs, adding features, improving documentation, or helping with the multiplayer system, your input is valuable.

### 🌟 Ways to Contribute

1. **Code Contributions**
   - Implement new features
   - Fix bugs and issues
   - Optimize existing code
   - Add unit tests

2. **Multiplayer Development** 🔥
   We're actively building the multiplayer and networking components! If you have experience with:
   - Socket programming
   - Network protocols
   - Real-time synchronization
   - Game server architecture
   
   **Please join us!** Check out the `multiplayer/` directory and see our current progress.

3. **Documentation**
   - Improve README and code comments
   - Create tutorials or guides
   - Write API documentation

4. **Design & Assets**
   - Create new sprites or backgrounds
   - Design UI elements
   - Contribute sound effects or music

### 📝 Contribution Guidelines

#### Step 1: Fork and Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Flappy-Bird.git
cd Flappy-Bird
```

#### Step 2: Create a Branch
```bash
# Create a descriptive branch name
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

#### Step 3: Make Your Changes
- Write clean, well-commented code
- Follow existing code style and conventions
- Test your changes thoroughly
- Update documentation if needed

#### Step 4: Commit Your Changes
```bash
git add .
git commit -m "Add: brief description of your changes"
```

Use clear commit messages:
- `Add:` for new features
- `Fix:` for bug fixes
- `Update:` for improvements to existing features
- `Docs:` for documentation changes

#### Step 5: Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:
- Clear title describing the change
- Detailed description of what you did and why
- Reference any related issues

### 🐛 Reporting Issues

Found a bug? Have a suggestion? Please open an issue with:
- Clear, descriptive title
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Screenshots if applicable
- Your environment (OS, Python version)

### 💬 Questions?

Feel free to open a discussion or reach out to any team member. We're here to help!

---

## 👥 The Team

This project is the result of collaborative effort by a talented team of developers:

| Name | Role | GitHub Profile |
|------|------|----------------|
| **Mohanad Galmad** | Developer | [@hondagalmad](https://github.com/hondagalmad) |
| **Mohanad Alsayed** | Developer | [@Mawadda0](https://github.com/Mawadda0) |
| **Moaz Ibrahim** | Developer | [@m0ozaa](https://github.com/m0ozaa) |
| **Moaz Waleed** | Developer | [@Moza202](https://github.com/Moza202) |
| **Moaz Karam** | Developer | [@moaz-karam](https://github.com/moaz-karam) |
| **Mostafa Abdelwahab** | Developer | [@Muggle-B0rn](https://github.com/Muggle-B0rn) |
| **Mostafa Refaat** | Developer | [@Mostafa-R2fat](https://github.com/Mostafa-R2fat) |
| **Mawadda Gaber** | Developer | [@Mawadda0](https://github.com/Mawadda0) |
| **Nour Elhouda** | Developer | [@Nourelhouda101](https://github.com/Nourelhouda101) |

---

## 🙏 Acknowledgments

- Original Flappy Bird concept by Dong Nguyen
- Pygame community for excellent documentation
- All contributors who have helped improve this project
- Open source community for inspiration and support

---

<div align="center">

**⭐ If you like this project, please give it a star on GitHub! ⭐**

Made with ❤️ by Us, we didn't name our team yet, so let it be us for now

</div>
