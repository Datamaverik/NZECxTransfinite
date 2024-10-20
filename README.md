
# xTransfinitte - CYWRECK CY1: Code Vulnerability Detection Using LLMs
hosted at : http://nzecxtransfinitte.tech/

## Team Members:
- Shreyash Verma
- Avyyukt Ajith
- Arush Pimpalkar
- Nikhil Sharma
- Ayush Sharma

## Project Overview
This project addresses the challenges in modern software development where security vulnerabilities can be introduced across multiple programming languages. Manually identifying these issues is error-prone and time-consuming. Our solution, an **LLM-powered chatbot**, assists developers by detecting vulnerabilities in code and providing real-time suggestions for fixes.

## Problem Statement
Modern software development often leads to security vulnerabilities across multiple languages. Manual detection is inefficient, and there is no unified solution for multi-language code analysis. Key challenges include:
- Lack of centralized tools for multi-language vulnerability detection.
- Identification of common vulnerabilities like SQL injections and buffer overflows.

### Our Objective:
To create a system that:
- Analyzes code in multiple languages for vulnerabilities.
- Provides real-time fixes to enhance code security.

## Approach
1. **Query Handling**: 
   - The system identifies if the user input is a code snippet or a GitHub repository.
   
2. **Code Snippet Analysis**:
   - Code snippets are processed to generate embeddings, and a similarity search is conducted using a vulnerability database.
   - The top matches are used to create an augmented prompt for an LLM to generate a detailed response.
   
3. **GitHub Repository Analysis**:
   - The system uses **CodeQL** to analyze repositories for vulnerabilities.
   - Vulnerable code segments are then processed through the LLM for analysis and fix recommendations.
   
4. **Output**:
   - A detailed report is generated, outlining vulnerabilities and corresponding fixes.

## Tech Stack
- **Frontend**: React.js, Tailwind CSS
- **Backend**: FastAPI, Typescript
- **Vulnerability Analysis**: CodeQL, LLM-powered chatbot

## Use Cases
1. **Code Security Audits**: Automatically detect vulnerabilities before deployment.
2. **Real-Time Developer Assistance**: Offer real-time security checks and fixes while coding.
3. **GitHub Repository Scanning**: Scan entire repositories for vulnerabilities via a GitHub link.

## Future Scope
1. **Support for More Programming Languages**: Expand the app to support additional languages and frameworks.
2. **IDE Integration**: Develop plugins for popular IDEs like VS Code and IntelliJ for real-time vulnerability detection within the coding environment.
3. **Continuous Monitoring in CI/CD**: Integrate continuous security checks in CI/CD pipelines for ongoing protection throughout the development lifecycle.

## How to Run the Project
1. Clone the repository.
2. Install dependencies using:
3. Run the development server:
4. For the backend, navigate to the backend directory and use:
5. To use the GitHub repository scanner, ensure CodeQL is installed and properly configured.

