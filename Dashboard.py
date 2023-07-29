# -*- coding: utf-8 -*-

import streamlit as st
import pickle
import requests
import numpy as np


dataDumpFolder = 'D:\Machine Learning and Data Science\Projects\Movie Recommendation System\Processed Data'
dataDumpFiles = ['\keyFeature.pkl', '\similarVector.pkl', '\moviesMetadataProcessed.pkl', '\keywordsProcessed.pkl']


@st.cache_data
def loadData():
    keyFeature = pickle.load(open(dataDumpFolder + dataDumpFiles[0], 'rb'))
    moviesMetadataProcessed = pickle.load(open(dataDumpFolder + dataDumpFiles[2], 'rb'))
    keywordsProcessed = pickle.load(open(dataDumpFolder + dataDumpFiles[3], 'rb'))
    
    return keyFeature, moviesMetadataProcessed, keywordsProcessed


@st.cache_resource
def loadModel(): 
    similarVector = pickle.load(open(dataDumpFolder + dataDumpFiles[1], 'rb'))

    return similarVector


def doOnPageLoad():
    st.set_page_config(layout="wide")
    cssFolderPath = 'D:\Machine Learning and Data Science\Projects\Movie Recommendation System\css'
    cssFile = '\master.css'

    with open(cssFolderPath + cssFile) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)
    


def recommendMovie(movieTitle):
    index = keyFeature[keyFeature[keyFeatureColumns[2]] == movieTitle].index[0]  
    cosineDistance = sorted(list(enumerate(similarVector[index])), reverse = True, key = lambda x : x[1])
    
    recommendedMovie = []
    recommendedMoviePoster = []
    for i in cosineDistance[1:13]:
        
        recommendedMovie.append(keyFeature.loc[i[0],keyFeatureColumns[2]])
        recommendedMoviePoster.append(fetchPoster(keyFeature.loc[i[0],keyFeatureColumns[1]]))

    return recommendedMovie, recommendedMoviePoster


def fetchPoster(movieID):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=23478094a8d378acf902362b1f403457".format(movieID)
    movieFetchedData = requests.get(url)
    movieFetchedData = movieFetchedData.json()
    try:
        posterPath = 'https://image.tmdb.org/t/p/w500' + movieFetchedData["poster_path"]
    except:
        posterPath = 'https://www.shutterstock.com/shutterstock/photos/1030785001/display_1500/stock-vector-house-not-available-icon-flat-symbol-isolated-vector-illustration-of-icon-sign-concept-for-your-1030785001.jpg'
    
    return posterPath


def main():
    
    global keyFeature, keyFeatureColumns, similarVector, moviesMetadataProcessed, moviesMetadataProcessedColumns, keywordsProcessed, keywordsProcessedColumns
    
    doOnPageLoad()
    
    keyFeature, moviesMetadataProcessed, keywordsProcessed = loadData()   
    
    keyFeatureColumns= keyFeature.columns
    moviesMetadataProcessedColumns = moviesMetadataProcessed.columns
    keywordsProcessedColumns = keywordsProcessed.columns
    
    similarVector = loadModel()
    
    st.title("Movie Database")
    
    dropboxItems = ('Movie Recommendation System', 'Search Movie')
    sidebar = st.sidebar.selectbox("Menu", dropboxItems)
    
    if sidebar == dropboxItems[0]:
        st.header(dropboxItems[0])
        
        selectBoxItems = tuple(keyFeature[keyFeatureColumns[2]])
        
        selectBoxTitle = st.selectbox("Select Movie", selectBoxItems)
        
        selectBoxButton = st.button("Show Similar Movies", type = 'primary')
        
        recommendedMovie = []
        recommendedMoviePoster = []
        
        if selectBoxButton:
            recommendedMovie, recommendedMoviePoster = recommendMovie(selectBoxTitle)
            
            cardsPerRow = 4
            for rowNo in range(len(recommendedMovie)):    
                i = rowNo % cardsPerRow
                if i == 0:
                    st.divider()
                    cols = st.columns(cardsPerRow, gap = "large")
                
                with cols[i]:
                    st.image(recommendedMoviePoster[rowNo]) 
                    st.caption(recommendedMovie[rowNo].capitalize())
        else:
            for i in range(15):
                st.text("")
    
    if sidebar == dropboxItems[1]:
        st.header(dropboxItems[1])
        
        movieTitleSearched = st.text_input("Enter Movie Name", placeholder = "Movie Name", value = "")
        
        searchByOriginalTitle = moviesMetadataProcessed[moviesMetadataProcessedColumns[8]].str.contains(movieTitleSearched, case = False)
        searchByTitle = moviesMetadataProcessed[moviesMetadataProcessedColumns[20]].str.contains(movieTitleSearched, case = False)
        
        movieMatchedColumns = [moviesMetadataProcessedColumns[5], moviesMetadataProcessedColumns[20], moviesMetadataProcessedColumns[9], moviesMetadataProcessedColumns[10], moviesMetadataProcessedColumns[14], moviesMetadataProcessedColumns[16], moviesMetadataProcessedColumns[22], moviesMetadataProcessedColumns[23], moviesMetadataProcessedColumns[8]]
        
        moviesMatched = moviesMetadataProcessed.loc[np.logical_or(searchByOriginalTitle, searchByTitle), movieMatchedColumns]
        
        cardsPerRow = 3
        if movieTitleSearched:
            for rowNo, row in moviesMatched.reset_index().iterrows():
                i = rowNo % cardsPerRow
                if i == 0:
                    st.divider()
                    cols = st.columns(cardsPerRow, gap = "large")
                    
                with cols[i]:
                    
                    st.image(fetchPoster(row[movieMatchedColumns[0]]))
                    st.subheader(row[movieMatchedColumns[1]])
                    st.caption("Alternate Name : " + row[movieMatchedColumns[8]])
                    
                    st.divider()
                    
                    st.caption(row[movieMatchedColumns[2]])
                    
                    subCols = st.columns(2)
                    with subCols[0]:
                        st.write("Popularity : ", round(row[movieMatchedColumns[3]], 2))
                        st.write("Average Vote : ", round(row[movieMatchedColumns[6]], 2))
                        st.write("Vote Count : ", row[movieMatchedColumns[7]])
                    
                    with subCols[1]:
                        st.write("Release Year : \n", row[movieMatchedColumns[4]].year)
                        st.write("Runtime : ",row[movieMatchedColumns[5]], ':green[min]')
        else:
            for i in range(15):
                st.text("")
            
        
    
    st.divider()
    cols = st.columns(5, gap = 'large')
    with cols[2]:
        st.caption('© Chirag Gupta')
        
        

if __name__ == '__main__':
    main()