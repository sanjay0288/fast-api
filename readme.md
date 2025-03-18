# FastAPI Application Deployment to AWS ECS using GitHub Actions

This project demonstrates a CI/CD pipeline for deploying a **FastAPI** application to **AWS ECS** using **GitHub Actions**. The pipeline includes the following:

- **Dockerization** of the FastAPI application.
- **Deployment** of the application on AWS ECS (Elastic Container Service).
- **API** authentication using an API key.
- **Health check** and **data retrieval** endpoints.
- **Automated deployment** via GitHub Actions using the AWS CDK.

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Technologies Used](#technologies-used)
4. [Getting Started](#getting-started)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [GitHub Secrets](#GitHubSecrets)
7. [Testing](#testing)


## Overview

This project creates a simplified cloud-based application deployment pipeline using **GitHub Actions** and **AWS services**. The main goal is to deploy a **containerized FastAPI** application to **AWS ECS**. The application consists of:

- A **health check** endpoint (`/health`) to check the status of the application.
- A **data retrieval** endpoint (`/data`) that requires authentication via an API key.

The deployment process uses the **AWS Free Tier** for cost efficiency, and **AWS CDK** is used to define the infrastructure.

## Project Structure


├── .github/
│   └── workflows/
│       └── workflow.yml        # GitHub Actions pipeline for deployment
├── application/
│   ├── __init__.py
│   ├── auth.py                # Authentication logic for API key validation
│   ├── data.py                # Dummy data or data-related functions
│   └── main.py                # FastAPI application with endpoints
├── my-fastapi-app-cdk/         # AWS CDK infrastructure code
├── Dockerfile                 # Dockerfile to containerize the FastAPI app
├── requirements.txt           # Python dependencies for the FastAPI app
└── README.md                  # Project documentation

## Technologies Used

- FastAPI: For building the Python REST API.

- Docker: For containerizing the application.

- GitHub Actions: For CI/CD pipeline automation.

- AWS ECS: For deploying the containerized FastAPI application.

- AWS CDK: For defining the cloud infrastructure (ECS, Load Balancer, etc.).

- Amazon ECR: For storing the Docker images.

## Getting Started
To get started with this project, follow these steps:

## Pre-requisites
- GitHub Account: You will need a GitHub account to clone the repository and trigger the pipeline.
- AWS Account: You will need an AWS account for deploying the application using ECS.
- AWS CLI: Make sure to have the AWS CLI configured locally to interact with AWS services.

## CI/CD Pipeline GHA Workflow

The pipeline is defined in the .github/workflows/workflow.yml file. The following steps are performed:

- Checkout Code: Checkout the latest code from the main branch. 
- Install Dependencies: Install the necessary dependencies from requirements.txt to ensure that the application can run and build properly within the environment.
- Configure AWS Credentials: Use AWS GitHub Action to configure the AWS credentials.
- Install AWS CDK: Install AWS CDK globally.
- Set up Docker Buildx: Prepare Docker for multi-platform builds.
- Log in to Amazon ECR: Authenticate Docker to Amazon ECR.
- Build Docker Image: Build the Docker image for the FastAPI app.
- Push Docker Image to ECR: Push the Docker image to ECR.
- Deploy with AWS CDK: Deploy the infrastructure (ECS, Load Balancer) using AWS CDK.
- Capture Load Balancer URL: Retrieve the URL of the Load Balancer.
- Test Health Endpoint: Run a health check on the deployed application to ensure it is working properly.

## GitHubSecrets
Ensure the following secrets are set up in your GitHub repository's settings

- AWS_ACCESS_KEY
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- AWS_ACCOUNT_ID
- API_KEY
- API_KEY_HEADER
  
## Testing
You can test the deployed application by making requests to the Load Balancer URL.The two main endpoints are

- Health Check : curl "LB URL"/health
- Data Retrieval: curl -X GET "http://"load-balancer-url"/data" \
  -H "X-API-KEY": "your-api-key" \
  -H "API_KEY_HEADER": "your-api-key-header"

