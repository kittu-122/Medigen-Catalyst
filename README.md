## MediGen Catalyst :microscope:
MediGen Catalyst is a Streamlit application designed to assist in analyzing medical images using advanced AI models. It leverages Google’s AI capabilities to provide insights into medical images, helping in identifying anomalies and suggesting next steps for medical professionals.

## Prerequisites
Before you begin, ensure you have met the following requirements:

* Python 3.7+ installed on your system.
* A valid Google API Key. You can obtain one from the [Google AI Studio](https://aistudio.google.com/app/apikey)
* Google Cloud SDK installed. You can download it from [Google Cloud SDK](https://cloud.google.com/sdk?hl=en)

## Problem Description
1.	Medical professionals often need assistance in analyzing medical images to identify anomalies or health issues. 
2.	Manual analysis can be time-consuming and prone to error.

## Solution Provided
MediGen Catalyst offers an interactive platform where users can upload medical images for AI-powered analysis. The application uses Google’s AI models to generate detailed reports, including:
1.	Detailed Analysis: Examination of the image for any abnormal findings.
2.	Findings Report: Documentation of observed anomalies or signs of disease.
3.	Recommendations and Next Steps: Suggested actions based on the analysis.
4.	Treatment Suggestions: Possible treatment options or interventions.

## Features
* Image Upload: Users can upload medical images in PNG, JPG, or JPEG formats.
* AI Analysis: Generates a detailed report based on the uploaded image.
* Interactive Interface: User-friendly design with progress indicators and feedback.
* Real-time Updates: Provides immediate analysis results once the image is processed.

## Components
The application consists of several key components:
* Streamlit: Framework for building the web application interface.
* Google Cloud AI Platform: Used for initializing the AI models and managing configurations.
* Google Generative AI: Provides the AI capabilities for generating content based on the medical images.
* PIL (Python Imaging Library): Handles image processing and manipulation.
* dotenv: Manages environment variables for secure API key storage.
  
## Additional Notes
* The application requires authentication with Google Cloud Platform to access AI services.
* Environment variables such as the Google API key need to be configured for proper functioning.

## Getting Started
Follow these steps to set up and run the project on your local machine.

1. Install the required packages:
```
pip install -r requirements.txt
```

2. Create a .env file in the project root directory and add the following line:

   Once you have the API Key you can add it in the ```.env.example``` file and rename it ```.env```.
```
GOOGLE_API_KEY=<your_google_api_key>
```

## How to run the Medigen-Catalyst (GUI mode)

Here the instructions to run medigen-catalyst in GUI mode:

1. Git clone the repository on your local machine:
  ```
  git clone https://github.com/kittu-122/Medigen-Catalyst.git
  cd Medigen-Catalyst
  ```

2. Create a Python Virtual environment in your current folder so that you don't corrupt the global python environment creating conflicts with other python applications:
  ```
  python -m venv medical
  ```

3. Activate the Python virtual environment:
  ```
  .\medical\Scripts\activate
  ```

4. Install the Python libraries in your Python virtual environment:
  ```
  pip install -r requirement.txt
  ```

5. Run the Medigen-Catalyst streamlit app:
  ```
  streamlit run filename.py
  ```

## Usage:
To use Medigen Catalyst, follow these steps:
* Open the application in your web browser.
* Upload a medical image using the file uploader.
* Click on "Generate Analysis" to start the analysis.
* Review the generated analysis report displayed on the screen.

## Dependencies:
* Python 3.x
* Streamlit: For building the web application
* Google Cloud AI Platform: For AI model management
* Google Generative AI: For generating content based on images
* PIL (Python Imaging Library): For image processing
* python-dotenv: For managing environment variables

## Contributing
Contributions are welcome! To contribute:

1. Fork the repository.

2. Create a new branch:
   
  ```
  git checkout -b feature/your-feature-name
  ```

3. Make your changes and commit them:

  ```
  git commit -m 'Add your feature description'
  ```

4. Push to the branch:
  
  ```
  git push origin feature/your-feature-name
  ```

5. Open a pull request with a description of your changes.
   
**Thank you for choosing this project. Hoping that this project proves useful and delivers a seamless experience for your needs!**
