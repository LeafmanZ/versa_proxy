# Proxy Server Setup for Versa SDWAN Director API

This guide describes how to set up a proxy server to reroute Versa SDWAN Director API commands when deployed on a mobile headend and rerouted to an AWS EC2 instance.

## Overview

### Deployment Options

- **AWS EC2:** The Versa Director deployed on a mobile headend might not have internet reachability as its internet connectivity is utilized between the mobile headend and the EC2 instance. This setup allows for the rerouting of private IP traffic through a proxy server. Deploy the `app.py` code on an AWS EC2 instance in the same availability zone as the Versa Director EC2 instance. Set the FORWARDING_IP to the private ip of the Versa Director EC2 instance. Use the new AWS EC2 instance public IP as the new endpoint for the API.
- **Heroku:** For rerouting traffic to HTTPS on port 443 with universally valid CA certificates, use Heroku. This ensures the traffic is rerouted securely and meets the security standards of companies and government organizations.

## Prerequisites

1. Access to an AWS EC2 instance or a Heroku account.
2. Basic knowledge of Git and Flask.

## Setup Instructions

### AWS Setup

1. Place the `app.py` code on an AWS EC2 instance.
2. Configure the proxy to forward the private IP traffic.
3. Hit the public IP of the AWS EC2 instance as the new API endpoint.

### Heroku Setup

1. **Login to Heroku:**
   ```bash
   $ heroku login
   ```

2. **Create and Setup Git Repository:**
   ```bash
   $ cd my-project/
   $ git init
   $ heroku git:remote -a zieleman1
   ```

3. **Deploy to Heroku:**
   ```bash
   $ git add .
   $ git commit -am "make it better"
   $ git push heroku master
   ```

4. **Setup for Existing Repositories:**
   ```bash
   $ heroku git:remote -a zieleman1
   ```

5. **Generate `requirements.txt`:**
   ```bash
   pip list --format=freeze > requirements.txt
   ```

## Application Details

- **Flask App Setup:** Initializes Flask with a secret key and configures the app to run on port 5000.
- **Global Variables:** Contains the forwarding IP and port for destination service.
- **Routes and Forwarding Logic:** Handles different HTTP requests and forwards them to the specified endpoints.
- **Authentication Handling:** Manages authentication requests, including token refreshes.
- **Security Considerations:** Utilizing `verify=False` during SSL certificate verification is discouraged in production due to potential security risks.

## Security and Maintenance

- Ensure SSL/TLS verification is enabled in production environments to mitigate security vulnerabilities.
- Enhance logging for improved monitoring and debugging.
- Implement error handling to enhance application robustness and usability.

This setup is ideal for scenarios requiring proxy services to reroute API traffic, manage authentication, and ensure secure communication.