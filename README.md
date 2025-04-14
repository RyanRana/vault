Vault
Secured File Sharing and Message Board System with VirusTotal Integration and Hash Authentication

This full-stack application aims to help teams in need of a secure digital platform. This system provides a secure message board and file-sharing platform where users can interact with messages, securely upload/download files, and manage tasks. The system leverages VirusTotal for malware detection, HMAC hash authentication for user verification, and uses JSON for file storage. The entire platform is built with HTML for the user interface and operates on an offline server to ensure security and privacy.
System Workflow
Admin Management:
The admin creates the initial account and sets user credentials.
Admins can add or delete users and export user data to a JSON folder for easy management.
User Login:
Users authenticate via HMAC authentication using their username and password.
Once authenticated, users can interact with the message board, upload/download files, and manage their tasks.
File Upload and Malware Detection:
Files are uploaded by users.
The system checks files for malware using VirusTotal. If the file passes the scan, it is encrypted and stored. If the file fails the scan, it is rejected.
Message Board Interaction:
Users post messages, reply to others, and interact with the community. All actions are logged and tracked for security.
Audit Logs:
All user interactions, such as file uploads, downloads, and message posts, are logged in the audit log for security and monitoring. 
To do list: 
Users can upload and monitor task from different users on the site 


