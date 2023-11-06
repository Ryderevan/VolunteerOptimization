import streamlit as st

def run():
    st.header('Volunteer Blackout Dates', divider = 'blue')
    st.write(st.session_state['blackoutdates'])


if __name__ == "__main__":
    run()