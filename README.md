# DevOps Assignment – AWS Terraform & Docker

## Overview

This repository contains the implementation of two DevOps assignment tasks:

### Task 1 – Infrastructure as Code (Terraform / CDK)

#### Objective:

- Use an Infrastructure as Code (IaC) tool to provision the following infrastructure:
- An EC2 instance with a public IP address.
- An EBS volume attached to the EC2 instance and encrypted using AWS KMS.
- Configure the instance with dynamic AMI lookup so that it works without hard-coding an AMI ID per region

I have chose to complete this task with Terraform as the IaC tool for this task as it provides a straightforward way to provision EC2, EBS, networking, and encryption resources without requiring additional programming code. And more reason that led me to this choice is the Dynamic AMI lookup.Terraform provides data sources that make it straightforward to retrieve the appropriate AMI dynamically based on the selected AWS region.

#### Aproach 

- A dedicated VPC (virtual network) was created to provide an isolated environment for hosting the EC2 instance and related resources. It was configured with the CIDR block 10.0.0.0/16, with DNS support and DNS hostnames enabled.
- A public subnet was created within the VPC to host the EC2 instance and enable internet connectivity. It was configured with the CIDR block 10.0.1.0/24, and public IP assignment was enabled for the EC2 instance.
- An Internet Gateway was created and attached to the VPC to enable communication between the EC2 instance and the internet.
- A route table was created and associated with the public subnet to direct internet-bound traffic through the Internet Gateway. A default route 0.0.0.0/0 was configured to achieve this.
- A security group was created and attached to the EC2 instance to control network traffic. Port 22 was allowed through the EC2 Instance Connect managed prefix list for SSH access, while port 8081 was opened to allow public access to the application. Outbound traffic was allowed to all destinations.
- An AWS KMS customer-managed key was created for encrypting the EBS volume.It has a deletion waiting period of 7 days and Automatic key rotation enabled.

Requirement 1:  
The EC2 instance was provisioned using the aws_instance resource.
The main configurations are:
- AMI: Uses the dynamically retrieved Ubuntu 24.04 AMI.
- Instance Type: t3.micro, selected as a small instance suitable for this assignment.
- Public IP: Explicitly enabled using associate_public_ip_address = true.

Requirement 2:  
An additional EBS volume was created using the aws_ebs_volume resource.
The configuration includes:
- Size: 8 GB.
- Volume Type: gp3, a general-purpose SSD volume.
- Encryption: Enabled using encrypted = true.
- KMS Key: Uses the customer-managed KMS key created earlier.
- The availability zone is dynamically obtained from the EC2 instance: availability_zone = aws_instance.web.availability_zone
Finally, the aws_volume_attachment resource attaches the encrypted EBS volume which is KMS-encrypted to the EC2 instance.

Requirement 3:  
Instead of specifying a fixed AMI ID, Terraform uses the aws_ami data source to automatically find the latest matching Ubuntu 24.04 image. Because AMI IDs vary across AWS regions, the region is passed through a variable named aws_region. While the AMI ID is not hardcoded, the region is specified manually in a variables file.A terraform.tfvars file is created to specify the region, making it much easier to find and update regions in a single, centralized location.

Deploy  
All the infractrucute with defined configurations will be created once the terraform code is Applied using "terraform apply"

### Task 2 – Application & Docker

#### Objective:
- Write a python application that returns a random string from given set Whenever a request is received on /api/v1
- A dockerfile for this application
- Exposing this application on port 8081
- Deploy the docker container on EC2 instance created in Task-1

#### Approach

- The Python application code and Dockerfile were initially created on the local system and tested to ensure that the application and its configuration were working as expected.
- After the initial testing, an SSH connection was established to the EC2 instance provisioned in Task 1.
- The required installations, including Docker, were performed on the EC2 instance to prepare the environment for deploying the application.
- The application files, including `app.py`, `requirements.txt`, and the Dockerfile, were then created again directly on the EC2 instance.
- Docker was used to build an image of the application and run it inside a container on the EC2 instance.

Requirement 1:  
The application was developed using Python and Flask.

The main implementation includes:
- Flask: Used to create the web application and define API endpoints.
- Route: The /api/v1 endpoint accepts GET requests.
- Random Selection: The random.choice() function selects a random string from the predefined list of five investment-related terms.
- Health Check: An additional /health endpoint returns Healthy with HTTP status code 200 to verify application availability.
Whenever a request is received at /api/v1, the application returns one randomly selected term from the list.

Requirement 2: 
A Dockerfile was created to package the Python application into a Docker image.

The main configurations include:
- Base Image: python:3.14-slim was selected as a lightweight Python image.
- Working Directory: A dedicated working directory was configured inside the container.
- Dependencies: The required Flask package was installed using requirements.txt.
- Application Files: The application code was copied into the Docker image.
- Port: Port 8081 was exposed for application access.
- Startup Command: The Flask application was configured to run on 0.0.0.0 at port 8081, allowing it to accept connections from outside the container.
  
#### Requirement 3: Expose the Application on Port 8081

The Flask application was configured to listen on port `8081` and `0.0.0.0` so that it could accept requests from outside the container.  
The Docker container was started using the following port mapping: -p 8081:8081  
This connects port `8081` of the EC2 instance to port `8081` inside the Docker container, allowing incoming requests to reach the Flask application.  
Additionally, the security group configuration in `main.tf` from task-1 was updated to allow inbound traffic on port `8081` from `0.0.0.0/0`. These changes were applied using Terraform.
This made the application accessible over the internet using the EC2 instance's public IP address

#### Requirement 4: Deploy the Docker Container on EC2

The application was deployed on the EC2 instance created in Task 1.

The deployment involved the following steps:

- Docker was installed on the EC2 instance.
- The application files and Dockerfile were created on the EC2 instance.
- A Docker image was built using the Dockerfile.
- A container was started using the generated image.
- The running container was verified using `docker ps`.

**Commands used:**

**Build the Docker image:**
```bash
docker build -t marketpulse-api .
```

**Run the Docker container:**
```bash
docker run -d --name marketpulse -p 8081:8081 marketpulse-api
```

**Verify the running container:**
```bash
docker ps
```

#### Testing the Application

Once the Docker container was deployed, the application was accessed using the public IP address of the EC2 instance.

**API Endpoint:**

[http://35.154.4.134:8081/api/v1](http://35.154.4.134:8081/api/v1)

Each GET request returns a randomly selected investment-related term.

**Health Check Endpoint:**

[http://35.154.4.134:8081/health](http://35.154.4.134:8081/health)

**Expected Response:**

```text
Healthy
```

Both endpoints were successfully tested using the EC2 instance's public IP address.

## Conclusion

Both tasks were successfully completed. Terraform was used to provision the AWS infrastructure, including an EC2 instance and a KMS-encrypted EBS volume. The Python application was containerized using Docker and deployed on the same EC2 instance. Both API endpoints were tested successfully and are accessible through the EC2 public IP address.

### Future Improvements

The project can be further improved by introducing the following enhancements:

- **Infrastructure Improvements:** Use Terraform modules to make the infrastructure code more reusable and easier to maintain.
- **Application Enhancement:** The Python application can be extended with additional features, more API endpoints, input validation, and better error handling to make it more functional.
- **Improved Deployment Approach:** Instead of creating application files directly on the EC2 instance, the deployment process can be improved by managing the code locally, storing it in GitHub, and using a CI/CD pipeline to automatically deploy the application to EC2. Docker images can also be built through the pipeline and stored in Amazon ECR.
