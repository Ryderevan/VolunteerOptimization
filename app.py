import streamlit as st
from ortools.sat.python import cp_model
import pandas as pd
#import math Why did I use this
import Run_Scheduling as rs



# Set custom page name
st.set_page_config(page_title='Schedule', page_icon=':calendar:', layout='wide')

#Show logo #####Why is this not working!?
#st.sidebar.image("C:\\Users\\ryder\\Documents\\Software\\ChurchesOptimization\Logos\\FP.png")

st.header('Volunteer Scheduling', divider='blue')
st.write(':gray[How to use this app: Constraints must be defined in the \'Constraints\' tab in the left sidebar.] '
         + ':gray[ Next, individual volunteers must be defined in the \'Volunteers\' tab. Once the required]'
         + ':gray[ information is populated, the \'Schedule Churches\' button will run the optimization and show the solution below.]')

#Load files
st.session_state['churchesdefinition'] = pd.read_csv('C:\\Users\\ryder\\Documents\\Software\\ChurchesOptimization\\Churches.csv')
st.session_state['blackoutdates'] = pd.read_csv('C:\\Users\\ryder\\Documents\\Software\\ChurchesOptimization\\BlackoutDates.csv')
st.session_state['weekdefinitions'] = pd.read_csv('C:\\Users\\ryder\\Documents\\Software\\ChurchesOptimization\\WeekDefinitions.csv')

#Get variables
churches = range(len(st.session_state['churchesdefinition']))
num_weeks = st.session_state['num_weeks']
max_consecutive_gap = st.session_state['max_consecutive_gap']
min_gap_church = st.session_state['min_gap_church']


#Create data structures to send to model
num_scheduled = st.session_state['churchesdefinition'].set_index('ChurchID')['NumWeeksScheduled'].to_dict()

unavailable = st.session_state['blackoutdates'].values.tolist()


schedule = pd.DataFrame(columns = ['Church', 'Week'])
schedule52 = pd.DataFrame(columns = ['Week'])

for i in range(53):
    schedule52 = pd.concat([schedule52, pd.DataFrame({'Week':[i]})])


#Populate dataframes for printing schedule
if st.button('Schedule Churches'):
    solution, scheduled_times = rs.run_scheduling(churches, num_weeks, num_scheduled, unavailable, max_consecutive_gap, min_gap_church)
    
    if solution.StatusName() == 'OPTIMAL':
        st.write('A solution was found!')
        for c in churches:
            #print
            for t in range(num_scheduled[c]):
                
                schedule = pd.concat([schedule, pd.DataFrame([{'Church':c, 'Week':solution.Value(scheduled_times[c,t])}])], ignore_index = True)


        schedule = pd.merge(schedule, schedule52, left_on = 'Week', right_on = 'Week', how = 'right')
        schedule = pd.merge(schedule, st.session_state['churchesdefinition'], left_on = 'Church', right_on = 'ChurchID', how = 'left')
        schedule = schedule.drop(columns = ['NumWeeksScheduled', 'ChurchID', 'Church'])
        schedule = schedule.sort_values(by = ['Week'])
        st.dataframe(schedule, column_config= {"ChurchName":"Church","Week":"Week"}, hide_index=True)



    else:
        st.write("No solution found or an error occurred. Please adjust constraints and try again")
    


