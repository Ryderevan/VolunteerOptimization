import streamlit as st

def run():
    st.header('Volunteer Setup', divider = 'blue')
    st.write(st.session_state['churchesdefinition'])


if __name__ == "__main__":
    run()