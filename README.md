# 🤖 ARISE — Multimodal Desktop AI Assistant

A modular, Python-powered desktop intelligence assistant integrating offline voice recognition, real-time computer vision gesture tracking, persistent memory graphs, and conversational task management.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://python.org)
[![OpenCV](https://img.shields.io/badge/Vision-OpenCV%20%7C%20MediaPipe-red?logo=opencv&logoColor=white)](https://opencv.org)
[![Vosk](https://img.shields.io/badge/Voice-Offline%20Vosk%20ASR-green)](https://alphacephei.com/vosk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Key Features

- **Offline Speech Recognition**: Low-latency voice activation and wake listener powered by Vosk acoustic models.
- **Vision & Gesture Control**: Computer vision pipeline leveraging OpenCV and MediaPipe for hands-free gesture commands.
- **Persistent State & Memory Graph**: Context-preserving state manager and memory engine for multi-turn desktop interaction.
- **Modular Architecture**: Clean separation between audio capture, vision perception, cognitive state, and executor engines.

---

## 🏗️ Architecture Overview

```
arise-multimodal-assistant/
├── arise.py              # Main assistant orchestrator
├── wake_listener.py      # Background voice listener (Vosk)
├── hand_detector.py      # Computer vision & gesture recognition
├── state_manager.py      # Dynamic state machine & event dispatcher
├── arise_memory.py       # Persistent contextual memory manager
└── arise_brain.json      # Structured episodic memory store
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- Microphone and webcam access

### Installation

```bash
git clone https://github.com/IshaanYK/arise-multimodal-assistant.git
cd arise-multimodal-assistant
pip install -r requirements.txt
```

### Running the Assistant

```bash
python arise.py
```

---

## 📄 License
MIT License. Created & maintained by [IshaanYK](https://github.com/IshaanYK).
