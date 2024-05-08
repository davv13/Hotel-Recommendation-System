import pandas as pd
import openai
from langdetect import detect, LangDetectException
from transformers import pipeline
import spacy

listing = pd.read_csv('Data/listings.csv')

listing = listing[
    ['id', 'listing_url',
       'description', 'neighborhood_overview', 'host_id',
       'host_url', 'host_since', 'host_about',
       'host_response_time', 'host_response_rate', 'host_acceptance_rate',
       'host_is_superhost', 'host_verifications',
       'host_identity_verified', 'neighbourhood',
       'neighbourhood_cleansed', 'latitude',
       'longitude', 'property_type', 'room_type', 'accommodates', 'bathrooms',
       'bathrooms_text', 'bedrooms', 'beds', 'amenities', 'price',
       'minimum_nights', 'maximum_nights', 
       'number_of_reviews', 'review_scores_rating', 'review_scores_accuracy',
       'review_scores_cleanliness', 'review_scores_checkin',
       'review_scores_communication', 'review_scores_location',
       'review_scores_value', 'instant_bookable']
]

listing20= listing.head(20)

reviews = pd.read_csv('Data/reviews.csv')   
reviews.drop(['id', 'reviewer_id'], axis=1, inplace=True)
reviews.rename(columns={'listing_id': 'id'}, inplace=True)

data_merged20= pd.merge(listing20, reviews, on='id', how='left')

nlp = spacy.load('en_core_web_sm')
def is_english(text):
    doc = nlp(text)
    english_tokens = [token for token in doc if token.lang_ == 'en']
    return len(english_tokens) > 0.5 * len(doc)

data_merged20['is_english'] = data_merged20['comments'].apply(is_english)
data_merged20= data_merged20[data_merged20['is_english']].drop(columns='is_english')

concatenated_comments = data_merged20.groupby('id')['comments'].agg(lambda x: '. '.join(x.dropna())).reset_index()
concatenated_comments.columns = ['id', 'concatenated_comments']

data= pd.merge(concatenated_comments, listing20, on='id', how='left')