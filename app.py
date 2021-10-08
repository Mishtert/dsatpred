import streamlit as st
import layout as lt
import predict
import base64

LOGO_IMAGE = "main_logo.png"
sidebar_image = 'side_logo.png'
st.markdown(
    """
        <style>
        .container {
            display: flex;
            justify-content: center;
        }
             
        .logo-text {
            font-weight:700 !important;
            font-size:50px !important;
            color: #f9a01b !important;
            padding-top: 75px !important;
        }
        .logo-img {
            float:right;
            padding: 10px
        }
        </style>
        """,
    unsafe_allow_html=True
)
st.markdown(
    f"""
        <div class="container">
            <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        </div>

        """,
    unsafe_allow_html=True
)

st.markdown(
    """
        <style>
        .sidebar {
            display: flex;
        }
        .logo-img {
            float:left;
        }
        </style>
        """,
    unsafe_allow_html=True
)
st.sidebar.markdown(
    f"""
        <div class="sidebar">
         <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(sidebar_image, "rb").read()).decode()}">
        </div>
     
        """,
    unsafe_allow_html=True
)
# <div style = "background.color:#6CC049; padding:10px">
# Main panel title

# lt.display_app_header(main_txt='trakk',
#                       main_txt2='Proactive Customer Experience (Cx) Management',
#                       sub_txt='Predict Potential Interaction with Bad Cx !!!')





PAGES = {
    # "VOC": shot,
    'Potential DSAT Interactions': predict,
}

def sidebar_credits():
    #Credits
    st.sidebar.subheader("About App")
    st.sidebar.text("Understand Quality of Interaction")
    st.sidebar.text("Proactively Manage Customer Experience")
    st.sidebar.subheader("Analytics, Design & Development")
    st.sidebar.text("Mishtert T")
    # st.sidebar.markdown("D&A Team")
    # st.sidebar.text("Subhendu Mandal | Mishtert T | Akash Nath Garg")



def main():
    lt.reverse_sidebar()
    lt.display_side_panel_header(txt='Navigation')

    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]

    with st.spinner(f"Extracting {selection} Loading ..."):
        page.write()  # each page has a write function
    sidebar_credits()


if __name__ == "__main__":
    main()


