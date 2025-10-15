# serverless-financial-pipeline
An event-driven ETL pipeline on AWS for fetching and analyzing financial market data.

# Serverless Financial Data ETL Pipeline

A complete, event-driven ETL (Extract, Transform, Load) pipeline built on AWS serverless architecture. It automatically fetches financial data for a given list of stock tickers, enriches it with several calculated Key Performance Indicators (KPIs), and saves the structured JSON output to an S3 bucket.

***
## **Key Features** ✨

* **Serverless & Scalable**: Uses a fan-out pattern with AWS Lambda and SNS to process a large number of tickers in parallel efficiently and cost-effectively.
* **Rich Data Enrichment**: Goes beyond simple data fetching by calculating valuable KPIs in real-time, including:
    * **Technical Indicators**: 14-Day RSI and 50-Day SMA.
    * **Risk Metrics**: 30-Day Historical Volatility.
    * **Fundamental Ratios**: Dividend Payout Ratio.
    * **Activity Signals**: Volume Anomaly Detection.
* **End-to-End Automation**: The entire process from triggering to data storage is fully automated.
* **Interactive Frontend**: A Vue.js web interface allows users to submit tickers and view the processed results in real-time.

***
## **Architecture Diagram** 🏗️

The project follows a decoupled, event-driven architecture that ensures scalability and resilience.

`[Vue.js Frontend]` -> `[API Gateway]` -> `[Orchestrator Lambda]` -> `[SNS Topic]` -> `[Worker Lambda]` -> `[S3 Bucket]`



1.  The user submits a list of tickers via the **Vue.js frontend**.
2.  **API Gateway** receives the request and triggers the **Orchestrator Lambda**.
3.  The Orchestrator publishes a separate message for each ticker to an **SNS Topic**.
4.  SNS triggers multiple instances of the **Worker Lambda** in parallel.
5.  Each Worker Lambda fetches data from Alpha Vantage, calculates the KPIs, and saves the final JSON to an **S3 Bucket**.
6.  The frontend polls the S3 bucket to display the results as they become available.

***
## **Technology Stack** 🛠️

### **Backend**
* Python 3.9
* Boto3 (AWS SDK for Python)
* Pandas & NumPy (for KPI calculations)

### **Cloud Infrastructure (AWS)**
* **Compute**: AWS Lambda
* **Messaging**: Amazon SNS
* **Storage**: Amazon S3
* **API**: Amazon API Gateway
* **Permissions**: AWS IAM

### **Frontend**
* Vue.js

### **Data Source**
* Alpha Vantage API

***
## **Setup and Installation** 🚀

### **Prerequisites**
* An AWS Account
* Git installed
* Python 3.9+ and pip installed
* Node.js and npm installed (for the frontend)
* A free Alpha Vantage API Key

### **Installation Steps**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/serverless-financial-pipeline.git](https://github.com/YourUsername/serverless-financial-pipeline.git)
    cd serverless-financial-pipeline
    ```

2.  **Backend Setup**:
    * Manually create the AWS resources (S3, SNS, IAM Roles, Lambda functions) as outlined in the architecture.
    * The `backend/` directory contains the Python code for the Lambda functions.
    * Create a Lambda deployment package or Layer that includes the `pandas` and `numpy` libraries.
    * Set the required environment variables in your Lambda functions (`S3_BUCKET_NAME`, `SNS_TOPIC_ARN`, `ALPHA_VANTAGE_API_KEY`).

3.  **Frontend Setup**:
    * Navigate to the frontend directory:
        ```bash
        cd frontend
        ```
    * Install the required npm packages:
        ```bash
        npm install
        ```
    * Update the API Gateway endpoint in the Vue.js code.

***
## **Usage**

1.  **Trigger via the Frontend**:
    * Run the Vue.js development server:
        ```bash
        npm run serve
        ```
    * Open the application in your browser, enter a list of comma-separated tickers, and click "Process".

2.  **Trigger via AWS Console (for testing)**:
    * Navigate to the `dispatch-ticker-orchestrator` Lambda function.
    * Use the "Test" tab to send the following JSON payload:
        ```json
        {
          "tickers": [
            "AAPL",
            "MSFT",
            "TSLA",
            "VFIAX"
          ]
        }
        ```
    * Check your S3 bucket for the resulting JSON files.
