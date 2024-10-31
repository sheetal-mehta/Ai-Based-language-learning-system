# AI-based Pronunciation Assessment and Grammatical Error Correction with Feedback for the German Language​

Multiple CALL systems as well as pronunciation assessment methods and Grammatical error correction 
methods have been developed in the past. Most of them focusing on English language. This given CALL system
focus on the pronunciation assessment and Grammatical error correction with feedback for German language, and focuses on the two main challenges faced by German language learners - Pronunciation and Grammar.

Below are the steps to setup and use the developed system-

* Download python version, 3.9 or above.(3.10.14 preferably)
* Setup virtual environment by following - https://docs.python.org/3/library/venv.html or using anaconda.
* Clone or download the given repository -  
~~~
gh repo clone SRH-Heidelberg-University-ADSA/GermanPronunciation
~~~
* Navigate to frontend directory and download and install all the requirements by using below command - 
~~~
pip install -r requirements.txt
~~~
* Setup your own credentials by navigating to frontend directory and adding credentials to setup_users.py and running it.
~~~
python setup_users.py
~~~
* Create a directory named "base_files" in frontend directory and add the base audio files (no longer than 3 seconds each) in wav format that acts as base/correct pronunciation reference.
* Go to https://drive.google.com/file/d/1x5vj6mGmUomyX2WaPK8PdfzaLwGMDgy3/view?usp=sharing download the zip file. Extract the folder "mt5-base-2" and place this folder into feedback directory. If you dont have access then request access.
* Navigate to the path where all the python packages and libraries are stored onto your system, find the allosaurus folder in the library, in there create a "pretrained" folder and Copy and paste the finetuned directory to the pretrained folder.
* Go to together Ai platform - https://www.together.ai/ , login and create your api key and add it to your .env file in frontend directory with TOGETHER_API_KEY = your_key.
* Finally run the streamlit app - 
~~~
python -m streamlit run main.py
~~~
* Login with the credentials you have set up and enjoy learning!
