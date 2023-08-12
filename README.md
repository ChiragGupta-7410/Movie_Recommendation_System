# Movie_Recommendation_System
## Description
This system suggests movies similar to the one searched by the user. It utilizes count vectorization and cosine similarity to find movies with similar plot. User can also search for movies.

## Environment Setup
1. Install Anaconda
2. Open Anaconda Prompt
3. Create New Environment: 
	`conda create -n Env_name python=3.8`
4. Activate Anaconda Environment: 
	`conda activate Env_name`
5. Install Streamlit: 
	`pip install streamlit`

## Running Program
### Method - 1
1. Create 'Processed Data' Folder in the main directory
2. Open Jupyter notebook then 'Movie Recommendation System.ipynb' and run it.
3. If shows `unable to allocate space` error then either reduce of nrows in read_csv or search online for alternative solution
   
### Method - 2
1. Download Pre Processed Data from https://drive.google.com/drive/folders/1xuFLharC7t76NxWFLczqf1zwbOyQZ5OU?usp=drive_link
2. Unzip in the main directory

### Finaly
Run Dashboard: 
`streamlit run Dashboard.py`

