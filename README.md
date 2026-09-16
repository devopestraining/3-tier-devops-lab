# 3-Tier DevOps VM Lab

A simple 3-tier application for DevOps hands-on practice:

Browser -> Nginx frontend -> Flask backend -> MySQL database

## Prerequisites

Linux VM with:
- Docker
- Docker Compose plugin
- Git (optional)

Check:

    docker --version
    docker compose version

## 1. Start the application

    cd 3-tier-devops
    docker compose up -d --build

Check containers:

    docker compose ps

View logs:

    docker compose logs -f

## 2. Test

From the VM:

    curl http://localhost:8080/
    curl http://localhost:8080/health
    curl http://localhost:8080/db-test

From your workstation, open:

    http://<VM-IP>:8080

If using a cloud VM, allow TCP/8080 in the VM firewall/security group.

## 3. Understand the networking

Frontend is attached to:
- frontend_net

Backend is attached to:
- frontend_net
- backend_net

Database is attached only to:
- backend_net

Therefore the database is NOT directly exposed to the host.

Useful commands:

    docker network ls
    docker network inspect 3-tier-devops_frontend_net
    docker network inspect 3-tier-devops_backend_net

## 4. Troubleshooting exercises

Do these WITHOUT looking for the answer first.

### Exercise 1
Stop the database:

    docker compose stop database

What happens when you call /db-test?

### Exercise 2
Restart the database:

    docker compose start database

How long does it take for the backend health check to recover?

### Exercise 3
Break the database password in docker-compose.yml.

Restart the stack and determine:
- Which tier fails?
- What does the backend log show?
- How do you fix it?

### Exercise 4
Change Nginx proxy_pass from:

    http://backend:5000

to:

    http://wrong-backend:5000

What error do you get?

### Exercise 5
Remove the backend from frontend_net.

Can Nginx still reach the backend?

### Exercise 6
Remove the database from backend_net.

Can the backend reach MySQL?

### Exercise 7
Scale the backend:

    docker compose up -d --build --scale backend=3

What happens to Nginx routing? Research how Docker Compose DNS/service discovery behaves.

### Exercise 8
Check resource usage:

    docker stats

Identify the CPU and memory usage of each tier.

### Exercise 9
Find the container IP addresses:

    docker inspect devops-frontend
    docker inspect devops-backend
    docker inspect devops-database

Explain why application code should use the service name "database" instead of a hard-coded IP.

### Exercise 10
Delete containers but keep the database volume:

    docker compose down

    docker compose up -d --build

Does the database data remain?

Then test the destructive operation:

    docker compose down -v

Explain what was deleted and why this is dangerous in production.

## 5. DevOps challenge

After you understand the basic application, improve it yourself.

Level 1:
- Move passwords to a .env file.
- Add .gitignore.
- Add application logging.
- Add a production WSGI server.

Level 2:
- Add a GitHub repository.
- Create a CI pipeline.
- Run Python tests.
- Build the Docker image.
- Scan the image for vulnerabilities.

Level 3:
- Push the image to a container registry.
- Deploy automatically to your VM.
- Add rollback capability.

Level 4:
- Add Terraform.
- Create a VM/network using Terraform.
- Install Docker automatically with cloud-init or Ansible.

Level 5:
- Recreate the architecture in AWS:
  Route 53 -> ALB -> EC2/ECS -> RDS
- Add IAM, Security Groups, Secrets Manager, CloudWatch and Auto Scaling.

## Cleanup

    docker compose down

To also delete the database volume:

    docker compose down -v
