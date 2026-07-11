# VTown Music 🎵

A lightweight, first-principles Indian music recommendation engine built with raw Python and vector math—bypassing heavy ML frameworks like PyTorch or TensorFlow to explore custom feature mapping in a 5D vector space.

## 📊 Dataset (125 Hand-Curated Tracks)

A manually audited database tailored to Indian cinema with acoustic metrics (Energy, Danceability, Valence) sourced from Musicstax:

- **Tamil:** 40 songs
- **Telugu:** 21 songs
- **Hindi:** 21 songs
- **Bengali:** 20 songs
- **Kannada:** 6 songs

## 🧠 Core Mechanics

### 1. 3D to 5D Feature Expansion

Upgraded from purely acoustic vectors to include cultural context via normalized artist and actor frequencies:

$$\vec{V} = [\text{Energy}, \text{Danceability}, \text{Valence}, \text{Artist Weight}, \text{Actor Weight}]$$

### 2. Cosine Similarity & The Tempo Paradox

Calculates recommendation scores via vector direction rather than magnitude:

$$\text{Cosine Similarity}(\vec{A}, \vec{B}) = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|}$$

> **Key Discovery:** Because Cosine Similarity measures vector orientation, two tracks with wildly different BPMs or loudness (dB) can score near-perfect similarity if their structural Energy-to-Valence ratios align.

## 🛠️ Installation & Setup

### Prerequisites

Ensure you have Python 3.8+ installed.

### Install Dependencies
```bash
pip install -r requirements.txt

