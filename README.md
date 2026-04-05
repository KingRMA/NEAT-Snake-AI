# 🧬 NEAT Snake AI

An advanced, highly-optimized Snake AI written in Python. This project utilizes the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm to evolve a neural network capable of playing Snake autonomously. 

The environment is designed to aggressively train and evaluate the population using toroidal (wrap-around) board geography and intense frame-by-frame fitness reinforcement.

## ✨ Features
* **Limitless Training:** The AI generation loop runs continuously until strict plateau conditions are triggered.
* **Wrap-Around Mechanics:** The grid functions purely continuously. Hitting walls does not kill the snake; it simply wraps exactly to the opposite edge (modulo geometry calculation).
* **Toroidal Distance Rewards:** Calculates exact grid shortest paths (accounting for physical wall-wrap shortcuts) to properly reward the snake `+0.1` for moving correctly towards the food, and `-1.0` penalty for drifting away.
* **Hunter's Stagnation Countdown:** When an AI wanders within 5 Manhattan blocks of an apple, it becomes locked into a permanent 5-frame countdown sequence. Every 5 frames it fails to secure the target, it hemorrhages `-5.0` fitness until capturing its prey!
* **Despair Death Culling:** To safeguard against infinite-looping neuro-mutants, any specimen that spirals down to `-50` overall fitness is violently terminated by the environment to accelerate hardware calculations for the remaining generation.
* **Dynamically Protected Elitism:** Securely maintains a deepcloned snapshot of the highest ever performing model directly to disk (`best_snake.pkl`), entirely immune to manual interrupts or generation resets.

## 🧠 State Representation
The Neural Network assesses 12 specific numeric inputs each processing frame:
1. **Danger Sensors (3):** Is my tail physically located specifically Forward, Left, or Right of my current heading trajectory?
2. **Apple Proximity (4):** Up, Down, Left, Right directional flags indicating the relative positioning of the target.
3. **Current Momentum (4):** Flags indicating whether the agent is presently travelling Up, Down, Left, or Right.
4. **Body Mass (1):** Total current node length.

The network then outputs to three potential action states: **[Turn Left, Turn Right, Continue Straight]**.

## 🚀 Quickstart

### Prerequisites 
Requires Python 3.10+
```bash
pip install neat-python pygame numpy
```

### Commands

**1. Watch the Best Trained AI:**
Watches whatever generation `best_snake.pkl` has recorded.
```bash
python watch_best.py
```

**2. Train the Population (Live Evaluation):**
Spawns and calculates the generations.
```bash
python train.py
```

### 🎮 Pygame GUI Controls (During Training)
When running `python train.py`, use the number keys to alter simulation speeds:
* `1` - **Toggle View Mode:** Swap between mapping every single entity vs strictly locking the camera to the highest performing genome that generation.
* `2` - **Normal Speed:** Renders physics at 15 FPS so humans can comfortably watch the AI decisions.
* `3` - **Fast-Forward:** Removes FPS caps and pushes engine clock rate as high as rendering processly allows!
* `4` - **Lightning Mode:** Kills off all standard Pygame visual rendering and blitzes strictly the mathematical headless AI calculations at hundreds of generations per second!

## ⚙️ Configuration Details
All algorithm hyperparameters, speciation rates, and mutation odds are cleanly defined inside `config-feedforward.txt`. The absolute termination conditions lie firmly rooted inside the plateau algorithms configured directly inside `train.py`.

---
*Developed autonomously to demonstrate rapid AI prototyping.*
