import pickle
import streamlit as st
import requests
import base64
from PIL import Image


###########################################

image = Image.open('logo.png')

#st.sidebar.markdown(f"<h1 style='text-align:center; color: #00e8dc;font-size: 56px;font-weight: bold;'>ZERA</h1>", unsafe_allow_html=True)

###########################################
col1, col2, col3 = st.sidebar.columns([0.1,7.8,0.1])

with col1:
    st.write(' ')

with col2:
    st.image("logo.png")

with col3:
    st.write(' ')
########################################################

########################################################
st.sidebar.markdown(f"<h3 style='text-align:center; color: white;font-size: 20px;'>We predict what u like :) </h3>", unsafe_allow_html=True)
#################

def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )

side_bg = 'sidebar_back.png'
sidebar_bg(side_bg)
#################
#################background image setup
def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.

    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "jpg"

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

image='background.jpg'
set_bg_hack(image)
#################
#the main function that is called first and foremost with the navigation options in the sidebar
def main():
    # Register your pages
    pages = {
        "Recommender": page_first,
        "About Us": about_page
    }

    # Widget to select your page, you can choose between radio buttons or a selectbox
    page = st.sidebar.radio("", tuple(pages.keys()))

    # Display the selected page
    pages[page]()



def page_first():
        def fetch_poster(movie_id):
            url = "https://api.themoviedb.org/3/movie/{}?api_key=afd15a81a78d030256be7e29b657ceee&language=en-US".format(movie_id)
            data = requests.get(url)
            data = data.json()
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path

        def recommend(movie):
            index = movies[movies['title'] == movie].index[0]
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
            recommended_movie_names = []
            recommended_movie_posters = []
            for i in distances[1:6]:
                # fetch the movie poster
                movie_id = movies.iloc[i[0]].movie_id
                recommended_movie_posters.append(fetch_poster(movie_id))
                recommended_movie_names.append(movies.iloc[i[0]].title)

            return recommended_movie_names,recommended_movie_posters

        st.markdown("<h1 style='text-align: center;color: black;font-size: 1px;font-weight: bold;'>.</h1>",
                    unsafe_allow_html=True)
       #leaving space
        st.text("")


        movies = pickle.load(open('movie_list.pkl','rb'))
        similarity = pickle.load(open('similarity.pkl','rb'))

        movie_list = movies['title'].values
        selected_movie = st.selectbox(
            "Tell us what u like😊",
            movie_list
        )

        if st.button('Show Recommendation'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(recommended_movie_names[0])
                st.image(recommended_movie_posters[0])
            with col2:
                st.text(recommended_movie_names[1])
                st.image(recommended_movie_posters[1])

            with col3:
                st.text(recommended_movie_names[2])
                st.image(recommended_movie_posters[2])
            with col4:
                st.text(recommended_movie_names[3])
                st.image(recommended_movie_posters[3])
            with col5:
                st.text(recommended_movie_names[4])
                st.image(recommended_movie_posters[4])


#function for the about page
def about_page():
    #st.markdown("<h1 style='text-align: center;color: #00e8dc;font-size: 56px;font-weight: bold;'>🧿ZERA🧿</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;color: black;font-size: 56px;font-weight: bold;'>.</h1>",
                unsafe_allow_html=True)

    #descriptions
    st.markdown("<h6 style='text-align: justify;font-size:110%;font-family:Arial, sans-serif;line-height: 1.5;'> Zera - A movie recommendation system, to anticipate consumers film preferences based on their previous choices and behaviour. The main purpose of Zera is to filter and predict only those films that a certain user is most likely to enjoy.<br><br>What is the mechanism behind it?<br><br> The recommendation algorithm looks at the user's previous movie preferences and then uses that knowledge to identify comparable films. This data can be found in the database. Following that, the algorithm makes movie suggestions to the user.</h6>", unsafe_allow_html=True)
    # github repository link my project
    st.sidebar.subheader(
        "Check out my [Github Repository](https://github.com/thisisdeepakkumar/Movie_Recommendation_Engine)")
#footer

    hide_menu="""
    <style>
    footer:after{
    content:"[Copyright@2022@Deepak_Kumar 🧿🧿 For better experience switch on dark mode]";
    display:block;
    position:relative;
    color:#00e8dc;
    }
    </style>
    """


    st.markdown(hide_menu, unsafe_allow_html=True)
    # leaving space
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.subheader(
        " [Linkedin](https://www.linkedin.com/in/thisisdeepakkumar)🧿🧿[Insta](https://www.instagram.com/thisisdeepakkumar/)🧿🧿[Facebook](https://www.facebook.com/thisisdeepakkumar8)")

#first page function

##################
if __name__ == "__main__":
    main()