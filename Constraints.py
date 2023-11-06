import streamlit as st
import pandas as pd

def run():
    st.header("Constraints", divider = 'blue')

    #Read constraints file 
    constraints = pd.read_csv('C:\\Users\\ryder\\Documents\\Software\\ChurchesOptimization\\Constraints.csv')
    
    #Query the DataFrame for min_gap_church
    filtered_df1 = constraints[constraints['constraint'] == 'min_gap_church']
    
    #Find value
    if not filtered_df1.empty:
        min_gap_church = filtered_df1['value'].iloc[0]

    #update  constraint and constraint dataframe according to inputs
    condition1 = constraints['constraint'] == 'min_gap_church'
    min_gap_church = st.number_input('Minimum Gap Between One Volunteers Scheduled Weeks', min_value=0, value = int(min_gap_church))
    constraints.loc[condition1, 'value'] = min_gap_church

    #Save to session state
    st.session_state['min_gap_church'] = min_gap_church




    #Query the DataFrame for max_consecutive_gap
    filtered_df2 = constraints[constraints['constraint'] == 'max_consecutive_gap']
    
    #Find value
    if not filtered_df2.empty:
        max_consecutive_gap = filtered_df2['value'].iloc[0]

    #update  constraint and constraint dataframe according to inputs
    condition2 = constraints['constraint'] == 'max_consecutive_gap'
    max_consecutive_gap = st.number_input('Maximum Consecutive Unscheduled Weeks', min_value = 0, value = max_consecutive_gap)
    constraints.loc[condition2, 'value'] = max_consecutive_gap

    #Save to session state
    st.session_state['max_consecutive_gap'] = max_consecutive_gap




    #Query the DataFrame for num_weeks
    filtered_df3 = constraints[constraints['constraint'] == 'num_weeks']
    
    #Find value
    if not filtered_df3.empty:
        num_weeks = filtered_df3['value'].iloc[0]

    #update  constraint and constraint dataframe according to inputs
    condition3 = constraints['constraint'] == 'num_weeks'
    num_weeks = st.number_input('Number of Weeks to Schedule', min_value = 1, value = num_weeks)
    constraints.loc[condition3, 'value'] = num_weeks

    #Save to session state
    st.session_state['num_weeks'] = num_weeks

    
    # Step 3: Write the modified DataFrame back to the CSV
    constraints.to_csv('C:\\Users\\ryder\\Documents\\Software\\ChurchesOptimization\\Constraints.csv', index=False)
    

# You can call the run function if you want this page to be standalone as well
if __name__ == "__main__":
    run()


