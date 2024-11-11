import streamlit as st
import pyrebase
import page1, page2, page3, page4

# Hide Streamlit's default menu and footer for a cleaner look
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .css-1v3fvcr {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Firebase configuration
firebaseConfig = {
    'apiKey': "AIzaSyDsrIcuUlnVM-CYNj_lLlSrfiX_bqOx6so",
    'authDomain': "paygap-project.firebaseapp.com",
    'projectId': "paygap-project",
    'databaseURL': "https://paygap-project-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "paygap-project.firebasestorage.app",
    'messagingSenderId': "288758264928",
    'appId': "1:288758264928:web:94f7e0a06610a91a113f05",
    'measurementId': "G-M6DDG0QVE6"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Streamlit CSS styling with improved layout and colors
st.markdown("""
    <style>
    /* Header title styling */
    .header-title {
        font-size: 2rem;
        font-weight: 700;
        color: #E74C3C;
        text-align: center;
        margin: 20px auto;
    }

    /* Button styling */
    .stButton > button {
        display: block;
        margin: 15px auto;
        width: 80%;
        height: 50px;
        border-radius: 10px;
        background-color: #3498db;
        color: white;
        font-weight: 600;
        font-size: 16px;
        border: none;
        transition: background-color 0.3s, box-shadow 0.3s;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    }

    /* Button hover effect */
    .stButton > button:hover {
        background-color: #2980b9;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
    }

    /* Input field styling */
    .stTextInput > div > input {
        width: 100%;
        padding: 12px;
        font-size: 16px;
        color: #333;
        background-color: #ecf0f1;
        border: 2px solid #3498db;
        border-radius: 8px;
        margin-bottom: 20px;
        transition: border-color 0.3s, background-color 0.3s;
    }

    /* Input placeholder styling */
    .stTextInput > div > input::placeholder {
        color: #7f8c8d;
    }

    /* Input focus styling */
    .stTextInput > div > input:focus {
        border-color: #2980b9;
        background-color: #ffffff;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f9f9f9;
        padding: 20px;
        border-right: 2px solid #3498db;
    }

    /* Sidebar title */
    [data-testid="stSidebar"] h1 {
        font-size: 22px;
        font-weight: bold;
        color: #333;
        text-align: center;
    }

    /* Sidebar button styling */
    [data-testid="stSidebar"] button {
        margin: 8px 0;
        width: 100%;
        padding: 12px;
        font-size: 16px;
        color: #fff;
        background-color: #3498db;
        border: none;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    
    /* Sidebar button hover effect */
    [data-testid="stSidebar"] button:hover {
        background-color: #2980b9;
    }

    /* Custom text styling */
    .info-text {
        color: #2C3E50;
        font-size: 1.1rem;
        margin: 10px 0;
        text-align: center;

    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation
def sidebar():
    st.sidebar.title("Navigation")
    st.sidebar.button("Home", key="sidebar_home", on_click=lambda: go_to_page('home'))
    st.sidebar.button("Login", key="sidebar_login", on_click=lambda: go_to_page('login'))
    st.sidebar.button("Register", key="sidebar_register", on_click=lambda: go_to_page('register'))

# Page navigation
def go_to_page(page_name):
    st.session_state.page = page_name

# Login Page
def login_page():
    st.markdown("<div class='main'><h5 class='header-title'>Login</h5>", unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="Enter your email", key="login_email")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
    
    if st.button("Login", key="login_button"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.logged_in = True
            st.session_state.user = user
            go_to_page('home')
            st.success("Logged in successfully!")
        except Exception as e:
            st.error(f"Invalid email or password. {str(e)}")

# Registration Page
def registration_page():
    st.markdown("<div class='main'><h1 class='header-title'>Create Account</h1></div>", unsafe_allow_html=True)
    email = st.text_input("Email", placeholder="Enter your email", key="register_email")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="confirm_password")

    if st.button("Register", key="register_button"):
        if password != confirm_password:
            st.error("Passwords do not match.")
        else:
            try:
                auth.create_user_with_email_and_password(email, password)
                st.success("Account created successfully! Please log in.")
                go_to_page('login')
            except Exception as e:
                st.error(f"Failed to create account. {str(e)}")

    st.write("---")
    if st.button("Already have an account? Login", key="already_login_button"):
        go_to_page('login')

# Home Page
def home_page():
    st.markdown("<div class='main'><h5 class='header-title'>Pay Range Builder</h5></div>", unsafe_allow_html=True)

    st.markdown("<p class='info-text'>Get data-driven insights to create competitive pay ranges efficiently.</p>", unsafe_allow_html=True)

    st.markdown("""
    <ul class='info-text'>
        <li><strong>Data-Driven</strong>: Avoid guesswork for optimal pay ranges.</li>
        <li><strong>Customizable Approaches</strong>: Tailor solutions to fit your needs.</li>
        <li><strong>Accurate Budgeting</strong>: Align pay with company goals.</li>
    </ul>
    """, unsafe_allow_html=True)

    if st.button("Get Started", key="get_started_button"):
        go_to_page('page1')

    st.write("---")
    if st.button("Logout", key="logout_button"):
        st.session_state.logged_in = False
        go_to_page('login')
        st.success("Logged out successfully!")

# Main function
def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    sidebar()  # Display the sidebar

    if st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'register':
        registration_page()
    elif st.session_state.page == 'home' and st.session_state.logged_in:
        home_page()
    elif st.session_state.page == 'page1' and st.session_state.logged_in:
        page1.display_page1()
    elif st.session_state.page == 'page2' and st.session_state.logged_in:
        page2.display_page2()
    elif st.session_state.page == 'page3' and st.session_state.logged_in:
        page3.show()
    elif st.session_state.page == 'page4' and st.session_state.logged_in:
        page4.show()

# Run main function
if __name__ == "__main__":
    main()
