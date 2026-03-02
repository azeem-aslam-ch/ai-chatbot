# AWS Deployment Plan

This document outlines the strategy for deploying the AI Chatbot Website Platform to a production AWS environment.

## 1. Deployment Architecture Options

### Option A: AWS ECS (Elastic Container Service) with Fargate (Recommended)
This approach leverages the existing Docker containerization for a robust, scalable, and management-free infrastructure.
- **VPC:** Deploy into a custom VPC with public and private subnets.
- **Load Balancer (ALB):** Application Load Balancer in the public subnet to route traffic from the internet to the containers.
- **ECS Cluster:** Fargate cluster in the private subnet running the Frontend (Nginx) and Backend (FastAPI) tasks.
- **Secrets Manager:** Securely store the `OPENAI_API_KEY` and inject it into the backend container at runtime.
- **Route 53 & ACM:** Manage domain naming and SSL/TLS certificates for HTTPS.

### Option B: Serverless (AWS Lambda + S3/CloudFront)
This is highly cost-effective for variable traffic.
- **Frontend CloudFront & S3:** Host the static HTML/CSS/JS in an S3 bucket and serve via CloudFront for CDN caching and HTTPS.
- **Backend API Gateway & Lambda:** Convert the FastAPI application using `Mangum` to run as an AWS Lambda function triggered by API Gateway.
- **Systems Manager Parameter Store:** Store the `OPENAI_API_KEY`.

## 2. Step-by-Step Deployment (ECS Fargate Approach)
1. **ECR Setup:** Create two Amazon Elastic Container Registry (ECR) repositories: one for the frontend image, one for the backend.
2. **Push Images:** Build and push the Docker images to ECR.
3. **IAM Roles:** Create an overriding Task Execution Role granting ECS permission to pull from ECR and read from AWS Secrets Manager.
4. **Task Definitions:** Define the memory, CPU, and container configurations (referencing the ECR images and Secrets Manager keys) in task definitions.
5. **Load Balancer Setup:** Provision an ALB targeting port 80 (Frontend). The Nginx frontend will continue reverse-proxying internally to the backend container (if in the same task/pod) or via internal service discovery.
6. **Deploy Service:** Launch the ECS Service using Fargate, setting the desired task count for high availability.

## 3. Cost Optimization Strategy
- **Fargate Spot Instances:** Use Fargate Spot capacity providers for non-critical, interruptible workloads to save up to 70% on compute cost.
- **Right-Sizing:** Start with small container configurations (0.25 vCPU, 512MB RAM) and scale up horizontally based on CloudWatch metrics (CPU/Memory utilization).
- **OpenAI Token Management:** Implement caching (e.g., Redis) for frequently asked identical questions to reduce API calls, and enforce token limits (`max_tokens`) per request.
