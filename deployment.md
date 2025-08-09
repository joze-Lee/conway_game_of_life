Deployment Guide – Monument AI Conway’s Game of Life Challenge
1. Overview
This document provides a complete deployment process for the Monument AI Conway’s Game of Life Challenge.
The deployment strategy ensures:

Portability via Docker

Scalability on AWS EC2

Secure and efficient routing through Nginx

Professional CI/CD readiness

2. Prerequisites
Before starting, ensure the following are ready:

2.1 Local Environment
Git installed

Docker & Docker Compose installed

AWS CLI installed and configured

SSH access to your AWS EC2 instance

2.2 AWS EC2 Instance
OS: Ubuntu 22.04 LTS (recommended)

Minimum: t2.micro (free tier) or t3.small for better performance

Open security group ports:

22 → SSH

80 → HTTP (Nginx)

443 → HTTPS (if using SSL)

3. Clone the Repository
On your local machine:

bash
Copy code
git clone https://github.com/<your-repo>.git
cd <your-repo>
4. Environment Configuration
Create a .env file in the backend directory:

bash
Copy code
OPENAI_API_KEY=your_openai_api_key_here
(Ensure this file is never committed to the repository.)

5. Docker Setup
The project contains:

Backend: Python + FastAPI

Frontend: Static HTML/CSS/JS

Nginx: Reverse proxy for frontend/backend

5.1 Build & Run Locally
bash
Copy code
docker-compose up --build
Verify:

API: http://localhost:8000/docs

Frontend: http://localhost

6. Deploy to AWS EC2
6.1 Connect to EC2
bash
Copy code
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
6.2 Install Docker & Git
bash
Copy code
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose git -y
sudo systemctl enable docker
6.3 Clone Repository on EC2
bash
Copy code
git clone https://github.com/<your-repo>.git
cd <your-repo>
6.4 Build & Run
bash
Copy code
docker-compose up --build -d
7. Nginx Configuration
Inside the nginx.conf file:

nginx
Copy code
server {
    listen 80;

    server_name _;

    location / {
        root /usr/share/nginx/html;
        index index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
Restart Nginx:

bash
Copy code
docker exec -it <nginx_container_name> nginx -s reload
8. SSL (Optional but Recommended)
Install Certbot for HTTPS:

bash
Copy code
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
(Update DNS before running this.)

9. Redeployment Process
When code changes:

bash
Copy code
git pull origin main
docker-compose down
docker-compose up --build -d
10. Verification
Visit http://<EC2_PUBLIC_IP> or https://yourdomain.com

Use /api/docs for API testing

Test frontend interactions

11. Maintenance Notes
Monitor logs:

bash
Copy code
docker-compose logs -f
Restart services:

bash
Copy code
docker-compose restart
Regularly pull updates from GitHub and rebuild

12. Security Best Practices
Never commit .env or sensitive keys

Use HTTPS in production

Restrict SSH access to trusted IPs

Keep Docker & dependencies updated

13. Architecture Diagram
pgsql
Copy code
[Browser/Client]
      ↓
   [Nginx]
   /     \
Frontend  Backend (FastAPI)
             ↓
     [Conway Logic + AI Wrapper]
