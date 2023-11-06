from ortools.sat.python import cp_model
import pandas as pd
import math

def run_scheduling(churches, num_weeks, num_scheduled, unavailable, max_consecutive_gap, min_gap_church):

    model = cp_model.CpModel()

    # Create scheduled times variables and add constraints to ensure they are different
    scheduled_times = {}
    for c in churches:
        for i in range(num_scheduled[c]):  # Use the specified number of times for each church
            scheduled_times[c, i] = model.NewIntVar(0, num_weeks, f'church_{c}_for_the_{i}_time')
            if i > 0:
                model.Add(scheduled_times[c, i - 1] < scheduled_times[c, i])

    #No times equal to eachother.
    for c1, t1 in scheduled_times:
        for c2, t2 in scheduled_times:
            if c1 != c2: #and t1 > 0 and t2 > 0: 
                model.Add(scheduled_times[c1, t1] != scheduled_times[c2, t2])


    #unavailable weeks
    for c, w in unavailable:
        for t in range(num_scheduled[c]):
            model.Add(scheduled_times[c, t] != w)

    #n weeks apart constraint
    for c in churches:
        for t in range(num_scheduled[c]):
            if t>0:
                model.Add(scheduled_times[c, t-1]+ min_gap_church <= scheduled_times[c, t])

    
    ##Limit the number of consecutive unscheduled weeks
    # Create a binary variable for each week indicating if it's scheduled or not
    week_scheduled = {w: model.NewBoolVar(f'week_{w}_scheduled') for w in range(num_weeks)}

    # Add constraints to link the week_scheduled variables with the scheduled_times variables
    for w in range(num_weeks):
        # Create a list of boolean variables, each indicating if a particular church is scheduled in week w
        church_scheduled_this_week = []
        for c in churches:
            for t in range(num_scheduled[c]):
                church_scheduled = model.NewBoolVar(f'church_{c}_scheduled_in_week_{w}')
                model.Add(scheduled_times[c, t] == w).OnlyEnforceIf(church_scheduled)
                model.Add(scheduled_times[c, t] != w).OnlyEnforceIf(church_scheduled.Not())
                church_scheduled_this_week.append(church_scheduled)

        # If any church is scheduled in week w, set week_scheduled[w] to true
        model.AddMaxEquality(week_scheduled[w], church_scheduled_this_week)

    # Use a sliding window of size max_consecutive_gap + 1
    for w in range(num_weeks - max_consecutive_gap):
        # Count the number of unscheduled weeks in the window
        unscheduled_count = sum(week_scheduled[w + offset].Not() for offset in range(max_consecutive_gap + 1))
        # Ensure the count does not exceed max_consecutive_gap
        model.Add(unscheduled_count <= max_consecutive_gap)

    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    #Do not find all solutions
    solver.parameters.enumerate_all_solutions = False

    solver.Solve(model)

    



    return solver, scheduled_times