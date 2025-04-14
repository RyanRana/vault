# Vault: Secured File Sharing and Message Board System with VirusTotal Integration and Hash Authentication

Vault is a full-stack application designed to provide teams with a secure digital platform. The system offers a secure message board and file-sharing platform, allowing users to interact with messages, securely upload/download files, and manage tasks. It leverages VirusTotal for malware detection, HMAC hash authentication for user verification, and uses JSON for file storage. The entire platform is built with HTML for the user interface and operates on an offline server, ensuring security and privacy.

Was awarded first at RutgersXFiserv Hackathon

## System Workflow

### Admin Management
- The admin creates the initial account and sets user credentials.
- Admins can add or delete users and export user data to a JSON folder for easy management.

### User Login
- Users authenticate via HMAC authentication using their username and password.
- Once authenticated, users can interact with the message board, upload/download files, and manage their tasks.

### File Upload and Malware Detection
- Users upload files.
- The system checks files for malware using VirusTotal.
  - If the file passes the scan, it is encrypted and stored.
  - If the file fails the scan, it is rejected.

### Message Board Interaction
- Users post messages, reply to others, and interact with the community.
- All actions are logged and tracked for security.

### Audit Logs
- All user interactions, such as file uploads, downloads, and message posts, are logged in the audit log for security and monitoring.

### To-Do List
- Users can upload and monitor tasks from different users on the site.

## Technologies Used
- **Frontend**: HTML
- **Backend**: Node.js (for server-side operations)
- **Security**: HMAC hash authentication, VirusTotal API (for malware detection)
- **File Storage**: JSON
- **Encryption**: AES (for file encryption)
- **Database**: Local file storage (JSON)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ryanrana/vault.git
