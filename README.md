# 🧩 Logicuino - A simple logic analyzer

A simple Python-based logic analyzer that utilizes an Arduino (ATmega328P) as the source, or any other chip as long as it sends data in the same format and rate.
It is intended for hobbiest who doesn't have a proper logic analyzer to help them debug and analyzer simple issues. 

This part of the code is the PC side based on python that receives digital input data via **serial** and displays each channel as a live waveform in its own subplot.

---

## 🔌 Arduino code 
The arduino code can be found here:
Arduino repo: [Logicuino Arduino Logic Analyzer](https://github.com/fduraibi/Logicuino-Logic-Analyzer)  

---

## ✨ Features
- Reads bytes from Arduino over **Serial (115200–1000000 baud)**  
- Each bit in the byte represents the logic level of one channel  
- Supports **8 digital channels** (default: Arduino pins D2–D9)  
- **Live waveform plotting** with Matplotlib  
- **Zoom & Pan**:
  - `+` / `-` keys → zoom in/out horizontally  
  - Mouse wheel → zoom in/out  
  - Left mouse drag → pan left/right  
- **Freeze/Resume button** to pause the display for inspection  
- Each channel has its **own subplot** with shared time axis (like a real logic analyzer)

---

## 🛠 Requirements
Install Python dependencies:

```bash
pip install pyserial matplotlib
```