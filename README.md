
---

# 🚗 **Driver Alertness System**

The **Driver Alertness System** is an intelligent web application designed to monitor and improve driver safety by tracking their alertness. Through real-time webcam input and advanced gaze detection, the system can detect signs of drowsiness or distractions, such as looking at a phone, and warn the driver when their focus is compromised. With WebRTC for video streaming and WebSockets for real-time data transmission, the system ensures a seamless and responsive experience.

---

## 📌 **Features**

- **Real-Time Monitoring**: Detects the driver’s gaze direction in real time (forward, eyes closed, or looking down at a phone).
- **Alert System**: Issues warnings when the driver shows signs of drowsiness (eyes closed) or distraction (looking down).
- **Session Timer**: Tracks the duration of the driving session and warns if the driver has been on the road too long.
- **WebRTC & WebSocket Integration**: Ensures real-time video streaming and data exchange between the front-end and server.
- **Audio Alerts**: Provides audio cues for critical warnings, alerting the driver to stay focused.
- **Alertness Score**: A calculated score based on the driver's attention and behavior, offering quick feedback on alertness.

---

## 💻 **System Requirements**

- A **webcam** with video capture support.
- A **modern web browser** (e.g., Google Chrome, Mozilla Firefox) supporting WebRTC.
- An **active internet connection** for WebSocket communication.

---

## 🛠️ **Installation Instructions**

### 1. **Clone the Repository**
First, clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/driver-alertness-system.git
cd driver-alertness-system
```

### 2. **Install Dependencies**
Make sure you have **Node.js** installed. Then, run the following command to install the required dependencies:
```bash
npm install
```

### 3. **Start the Application**
Launch the application in development mode:
```bash
npm run dev
```

### 4. **WebSocket Server**
Ensure that the WebSocket server is running locally or remotely. Update the WebSocket server URL in the code to match your configuration.

---

## 🚦 **How It Works**

1. **Driver Monitoring**: 
   - The webcam feed captures the driver’s face, analyzing their gaze direction.
   - **Forward**: The driver is looking straight ahead.
   - **Eyes Closed**: Detected when the driver’s eyes are closed for a specified period.
   - **Looking Down**: Identifies when the driver is looking down, potentially at their phone.

2. **Alert System**:
   - **Drowsiness Alert**: If the driver’s eyes remain closed for more than 3 seconds, a drowsiness alert is triggered.
   - **Distraction Alert**: If the driver looks down (e.g., at their phone) for more than 2 seconds, a distraction alert is issued.

3. **Real-Time Feedback**: 
   - The system continuously updates the driver’s alertness status in real time, showing the **alertness score** and **session time**.
   - **Alertness Score**: A value calculated based on the occurrence of events like eyes closed or phone usage.

4. **Safety Tips**: 
   - Displays reminders to encourage safe driving practices, such as taking breaks and staying alert.

---

## ⚙️ **Testing Controls**

For testing purposes, you can simulate different driver behaviors using the following keyboard shortcuts:

- **F**: Simulate the driver looking forward.
- **C**: Simulate eyes closed (to simulate drowsiness).
- **D**: Simulate looking down (to simulate checking a phone).
- **N**: Simulate no detection (driver not visible).

These shortcuts allow you to manually test how the system responds to various scenarios.

---

## 🎨 **User Interface**

- **Video Feed**: Displays the webcam feed along with the detected gaze direction.
- **Alert Level**: A visual indicator (Normal, Warning) based on the driver’s attention.
- **Session Time**: Tracks the time elapsed since the start of the driving session.
- **Alertness Score**: Reflects the driver's overall alertness based on detected behaviors.
- **Safety Tips**: Displays helpful driving reminders to reduce the risk of accidents.

---

## 🚀 **Future Improvements**

- **Advanced Gaze Tracking**: Enhance the gaze detection algorithm for better accuracy.
- **Fatigue Detection**: Incorporate additional signals like blink rate and head nods to detect fatigue more reliably.
- **Mobile App Integration**: Develop a mobile version of the system to make it accessible on smartphones and tablets.
- **Driver Profile**: Create customizable profiles to track individual driver patterns over time.

---

## 📄 **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Feel free to contribute, report issues, or suggest new features by opening an issue or pull request!

---

