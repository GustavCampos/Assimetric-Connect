# LAN Chat Application

## Overview

This project is a **LAN-based chat application** designed to allow secure communication between peers over a local network. It uses **asymmetric cryptography** to ensure that messages exchanged between peers are encrypted and secure. The application is built using **Flask**, **Flask-SocketIO**, and **cryptography** libraries, and it supports both direct local execution and containerized deployment using **Docker**.

---

## Purpose

The main purpose of this project is to demonstrate the use of **asymmetric cryptography** in a peer-to-peer chat application. It allows users to connect to other peers on the same LAN, exchange public keys, and securely send encrypted messages.

---

## How Asymmetric Cryptography Works in This Project

Asymmetric cryptography involves the use of a **key pair**:
- **Private Key**: Kept secret and used to decrypt messages.
- **Public Key**: Shared with others and used to encrypt messages.

### Workflow:
1. **Key Generation**: Each peer generates a unique key pair when the application starts.
2. **Key Exchange**: When a peer connects to another, they exchange public keys.
3. **Message Encryption**: Messages are encrypted using the recipient's public key.
4. **Message Decryption**: The recipient decrypts the message using their private key.

This ensures that:
- Only the intended recipient can decrypt the message.
- Even if the message is intercepted, it cannot be read without the private key.

---

## How to Run the Project

### 1. **Run Locally**
To run the project locally without Docker, follow these steps:

#### Prerequisites:
- Python 3.10 or higher installed.
- `pip` (Python package manager) installed.

#### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/GustavCampos/Assimetric-Connect
   cd assimetric-chat
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open your browser and navigate to `http://localhost:5000`.

---

### 2. **Run with Docker**
To containerize and run the project using Docker:

#### Prerequisites:
- Docker and `docker compose` installed on your system.

Just run the following command:
   ```bash
   docker compose up
   ```
This will create an app instance for you on `http://localhost:5000`.

---

### 3. **Run the Two-Peer Simulation**
The `two_peer_simulation.yml` file is a Docker Compose configuration that runs two instances of the application on the same machine to simulate two peers.

#### Prerequisites:
- Docker and Docker Compose installed.

#### Steps:
1. Run the simulation:
   ```bash
   docker compose -f two_peer_simulation.yml up
   ```
2. Open two browser tabs:
   - First instance: `http://localhost:5000`
   - Second instance: `http://localhost:5001`
3. Use the IP addresses displayed on each instance to connect the two peers.

---

## Key Features
- **Peer-to-Peer Communication**: Connect directly to other peers on the same LAN.
- **Asymmetric Encryption**: Ensures secure message exchange.
- **Dockerized Deployment**: Easily run the application in isolated containers.
- **Two-Peer Simulation**: Test the application locally with two instances.

---

## File Structure
- `app.py`: Main application logic.
- `security.py`: Handles key generation, encryption, and decryption.
- `templates/`: Contains HTML templates for the web interface.
- `Dockerfile`: Defines the Docker image.
- `docker-compose.yml`: Configuration for running a single instance with Docker.
- `two_peer_simulation.yml`: Configuration for running two instances to simulate peer-to-peer communication.

---

## Notes
- Ensure that the `keys/` directory is writable, as it stores the generated keys.
- The `--network host` option in Docker is required for LAN communication. This works on Linux; for macOS/Windows, additional configuration may be needed.