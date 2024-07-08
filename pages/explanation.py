import streamlit as st
import pandas as pd
st.set_page_config(page_title="SoundShapes", page_icon=":musical_note:" )


thumbnails_loc = 'user_evaluation_app/static/thumbnails/20240623_thumbnails_tsne_4698_600px'
mp3_folder = 'user_evaluation_app/static/mp3_previews'

st.title("SoundShapes explained")
st.write("Here are some examples of SoundShapes, previously known as Music Thumbnails. "
         "Each SoundShape represents an audio file.")


num_col = 6
num_files_to_display = 2 * num_col

selected_files = ['0Ab8mxRYp5yIDbYYobjQH6.svg', '0Ae4gETnUcCGZqWMETpPtt.svg', '0aJDvIeUkceMRueD84rRDR.svg',
                  '0aLlJ7kwSMmvpgTNjEiDeU.svg', '0aNAiwG9kCxFKCJVbo6B1J.svg', '0AOvD8LrdeDVDaLzSB7YsM.svg',
                  '0aPX1AXz8Tp51Nak6B04ij.svg', '0AQDhFnLUd32C8y3cjje9g.svg', '0AsXwDIqbjKbmYZI5AoDfG.svg',
                  '0At03SEJnxh05f0D3ZOUZ6.svg', '0AuX2BFFWQMpxhBkLiQvim.svg', '0Auzn7KMqzh7dhExejMzBy.svg']


columns = st.columns(num_col)
for i, svg_file in enumerate(selected_files):
    col = columns[i % num_col]
    col.image(f'{thumbnails_loc}/{svg_file}', use_column_width=True)

st.write("\n")
st.write("The background color of each thumbnail corresponds to the 'valence' or positivity of the music.")
st.image("user_evaluation_app/static/explanation_images/background_color_valence.svg", use_column_width=True)


st.image("user_evaluation_app/static/explanation_images/empty_radar_pdf.svg", width=500)
st.write("The shape of the thumbnail corresponds to the instruments that are detected.")


st.image("user_evaluation_app/static/explanation_images/_debug_600pxclassical.svg", width=500)
st.write("The thumbnail above could represent a classical chamber music piece.")
st.write("  \n")
st.image("user_evaluation_app/static/explanation_images/_debug_600pxpop.svg", width=500)
st.write("This thumbnail definitely represents something a bit more modern, a rock song perhaps?")

st.write("  \nA wider line corresponds to a more energetic song.")
st.image("user_evaluation_app/static/explanation_images/_debug_600pxloud_pop.svg", width=500)
st.write("This song is probably quite energetic.")

st.write("The color of each shape corresponds to an abstract representation of genre.")
st.image("user_evaluation_app/static/explanation_images/_debug_600pxhighlighted_center.svg", width=500)

st.write("---")
col1, col2 = st.columns(2,gap='large' )
col1.write("And that's it!  \n   \nBackground color ➡ positivity")
col1.image("user_evaluation_app/static/explanation_images/background_color_valence.svg", use_column_width=True)
col2.write("Shape ➡ instruments")
col2.image("user_evaluation_app/static/explanation_images/_debug_600pxclassical.svg", width=200)

col1, col2 = st.columns(2,gap='large' )

col1.write("Line width ➡ energy")
col1.image("user_evaluation_app/static/explanation_images/_debug_600pxloud_pop.svg", width=200)

col2.write("Fill color ➡ genre")
col2.image("user_evaluation_app/static/explanation_images/_debug_600pxhighlighted_center.svg",width=200)

col1, col2, col3 = st.columns(3)
if col3.button("Continue with  study pt 2", use_container_width=True):
    st.switch_page("pages/user_study_pt2.py")

if col2.button("Go back to study pt 1", use_container_width=True):
    st.switch_page("pages/user_study_pt1.py")

if col1.button(":rainbow-background[Go back to Exploring the SoundShapes]", use_container_width=True):
    st.switch_page("pages/thumbnail_exploration.py")