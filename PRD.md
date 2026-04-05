# Master Product Requirements Document (PRD): NEAT AI Snake

## 1. Project Overview
**Objective:** Develop a Python-based Snake game where an AI learns to play autonomously using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. 
**Tech Stack:** Python 3.x, `pygame` (rendering and UI), `neat-python` (neural evolution), `git` (version control).
**Target Audience / User:** The developer (acting as the observer/trainer).

## 2. The Game Environment (Pygame)
The standard Snake game mechanics apply, but modified to run seamlessly in an AI-training loop.
* **Grid System:** The game operates on a fixed 2D grid.
* **Mechanics:** The snake grows by 1 segment each time it eats an apple. Hitting the screen boundaries or its own tail results in immediate death.
* **Performance:** The game loop must be decoupled from the rendering framerate so the AI can train at uncapped speeds when visuals are disabled or sped up.

## 3. AI Architecture & State Space
The AI will use the NEAT algorithm to evolve a population of Feed-Forward Neural Networks.

### 3.1. The Inputs (Feature Vector)
For every frame, calculate and pass the following state variables to the neural network:
* **Immediate Danger (3 inputs, Binary `0` or `1`):** Is there a wall or tail directly 1 step ahead, 1 step to the left, or 1 step to the right (relative to the snake's current heading)?
* **Direction to Food (4 inputs, Binary `0` or `1`):** Is the apple located Above, Below, Left, or Right of the snake's head?
* **Current Heading (4 inputs, Binary `0` or `1`):** Is the snake currently moving Up, Down, Left, or Right?
* **Self-Awareness (1 input, Integer):** Current length of the snake.

### 3.2. The Outputs (Action Space)
The network will output an array of 3 values. The highest value determines the relative movement:
* `[1, 0, 0]` -> Continue straight
* `[0, 1, 0]` -> Turn right
* `[0, 0, 1]` -> Turn left

### 3.3. Fitness & Reward Function
* **Eat Apple:** `+10` points.
* **Death (Wall/Tail):** `-10` points.
* **Time Penalty:** `-0.1` points per frame to prevent infinite looping and encourage efficient hunting.
* *Note: A hard cap on frames (e.g., 100 frames allowed without eating an apple, scaling up as the snake grows) must be implemented to kill snakes that get stuck in safe loops.*

### 3.4. NEAT Configuration
* **Population Size:** 50 - 100 genomes per generation.
* **Hidden Layers:** Start at 0, allow NEAT to augment and add nodes dynamically.
* **Activation Function:** ReLU or Tanh.

## 4. UI, Visuals, & Interactive Controls
The simulation must include an interactive dashboard built into the Pygame window to allow the developer to observe and control the training process.

### 4.1. On-Screen Statistics
Render real-time text on the screen displaying:
* Current Generation Number
* Number of Snakes Currently Alive
* Highest Fitness in Current Generation
* All-Time Best Fitness
* Current Mutation Rate (if dynamic)

### 4.2. Interactive Buttons (Clickable UI)
Implement clickable UI buttons (or clearly labeled keyboard hotkeys mapped to visual toggles) for the following controls:
* **View Mode Toggle:** Switch between "Show All Snakes" (renders the entire population simultaneously with semi-transparency) and "Show Best Only" (renders only the current highest-performing snake to reduce visual clutter).
* **Speed Controls:**
  * `1x Speed`: Normal human-playable speed for observation.
  * `Fast Forward`: Uncaps the framerate but keeps rendering enabled.
  * `Lightning Mode`: Disables visual rendering completely to compute generations instantly in the background.

## 5. Deployment & Version Control Strict Directives
**CRITICAL INSTRUCTION FOR THE AI CODING AGENT:** The developer is already authenticated with GitHub in their terminal environment. Under no circumstances should the AI agent automatically execute `git commit` or `git push` commands. 

The agent must follow this exact sequence:
1. Write, test, and debug the local Python code.
2. Initialize the local git repository (`git init`) if not already present.
3. **HALT OPERATION.**
4. Explicitly ask the user in the chat interface: *"The code is complete and functional. Do you want me to upload this final project to your GitHub repository?"*
5. Execute `git add .`, `git commit`, and `git push` **ONLY** after receiving an affirmative response from the human user.