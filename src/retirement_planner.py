import streamlit as st
import os
import json
import matplotlib.pyplot as plt
import numpy as np

def show_retirement_planner():
    st.title("🏖️ Retirement Lifestyle Planner")
    st.header("Retirement Projection Calculator")

    SCENARIOS_DIR = "scenarios"
    os.makedirs(SCENARIOS_DIR, exist_ok=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        capital = st.number_input("Current Capital ($)", min_value=0.0, value=0.0, step=1000.0)
    with col2:
        age = st.number_input("Your Current Age", min_value=0, max_value=100, value=30)
    with col3:
        interest = st.number_input("Expected Annual Interest Rate (%)", min_value=0.0, value=7.0, step=0.1)
    with col4:
        total_years = st.number_input("Planning Period (Years)", min_value=1, max_value=60, value=30, step=1)

    if "contribution_phases" not in st.session_state:
        st.session_state.contribution_phases = []

    st.subheader("📅 Contribution Timeline")
    st.write(f"Define contribution phases across your {total_years}-year planning period. Phases can overlap to model additional contributions during specific periods.")

    # Display existing phases
    if st.session_state.contribution_phases:
        st.markdown("##### Current Phases:")
        for idx, phase in enumerate(st.session_state.contribution_phases):
            col_a, col_b, col_c, col_d, col_e = st.columns([2, 2, 2, 2, 1])
            with col_a:
                st.text(f"Phase {idx+1}")
            with col_b:
                st.text(f"${phase['amount']:,.0f}/year")
            with col_c:
                st.text(f"Years {phase['start_year']} to {phase['start_year'] + phase['duration'] - 1}")
            with col_d:
                st.text(f"Duration: {phase['duration']} years")
            with col_e:
                if st.button("🗑️", key=f"delete_{idx}"):
                    st.session_state.contribution_phases.pop(idx)
                    st.rerun()

    # Add new phase form
    with st.expander("➕ Add New Contribution Phase", expanded=len(st.session_state.contribution_phases) == 0):
        col1, col2, col3 = st.columns(3)
        with col1:
            new_amount = st.number_input("Annual Contribution ($)", min_value=0.0, step=1000.0, key="new_amount")
        with col2:
            new_start = st.number_input("Start Year", min_value=0, max_value=total_years-1, value=0, step=1, key="new_start")
        with col3:
            max_duration = total_years - new_start
            new_duration = st.number_input("Duration (Years)", min_value=1, max_value=max_duration, value=min(10, max_duration), step=1, key="new_duration")
        
        if st.button("Add Phase"):
            end_year = new_start + new_duration
            if end_year > total_years:
                st.error(f"Phase extends beyond planning period (year {total_years})")
            else:
                st.session_state.contribution_phases.append({
                    "amount": new_amount,
                    "start_year": new_start,
                    "duration": new_duration
                })
                st.rerun()

    # Visualize timeline
    if st.session_state.contribution_phases:
        st.markdown("##### Timeline Visualization")
        
        # Create timeline array showing total contributions per year
        yearly_contributions = np.zeros(total_years)
        for phase in st.session_state.contribution_phases:
            start = phase['start_year']
            end = start + phase['duration']
            yearly_contributions[start:end] += phase['amount']
        
        # Plot the timeline
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), gridspec_kw={'height_ratios': [1, 3]})
        
        # Top chart: Stacked phases
        ax1.set_xlim(-0.5, total_years - 0.5)
        ax1.set_ylim(0, len(st.session_state.contribution_phases) + 0.5)
        ax1.set_xlabel("Year")
        ax1.set_ylabel("Phases")
        ax1.set_title("Contribution Phases Timeline")
        colors = plt.cm.Set3(np.linspace(0, 1, len(st.session_state.contribution_phases)))
        
        for idx, phase in enumerate(st.session_state.contribution_phases):
            start = phase['start_year']
            duration = phase['duration']
            ax1.barh(idx, duration, left=start, height=0.8, 
                    label=f"Phase {idx+1}: ${phase['amount']:,.0f}/yr",
                    color=colors[idx], edgecolor='black', linewidth=1)
            # Add text in the middle of the bar
            mid_point = start + duration / 2
            ax1.text(mid_point, idx, f"${phase['amount']/1000:.0f}k", 
                    ha='center', va='center', fontsize=9, fontweight='bold')
        
        ax1.legend(loc='upper right', fontsize=8)
        ax1.grid(True, axis='x', alpha=0.3)
        ax1.set_yticks(range(len(st.session_state.contribution_phases)))
        ax1.set_yticklabels([f"Phase {i+1}" for i in range(len(st.session_state.contribution_phases))])
        
        # Bottom chart: Total contributions per year
        ax2.bar(range(total_years), yearly_contributions, color='steelblue', edgecolor='black', linewidth=0.5)
        ax2.set_xlabel("Year")
        ax2.set_ylabel("Total Annual Contribution ($)")
        ax2.set_title("Combined Annual Contributions (All Phases)")
        ax2.grid(True, axis='y', alpha=0.3)
        ax2.set_xlim(-0.5, total_years - 0.5)
        
        # Format y-axis to show dollar amounts
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}k' if x >= 1000 else f'${x:.0f}'))
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Show summary stats
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            total_invested = sum(yearly_contributions)
            st.metric("Total Contributions", f"${total_invested:,.0f}")
        with col_s2:
            max_yearly = np.max(yearly_contributions)
            st.metric("Peak Annual Contribution", f"${max_yearly:,.0f}")
        with col_s3:
            avg_yearly = np.mean(yearly_contributions)
            st.metric("Average Annual Contribution", f"${avg_yearly:,.0f}")

    if st.button("📈 Calculate Retirement Funds"):
        if not st.session_state.contribution_phases:
            st.warning("Please add at least one contribution phase.")
        else:
            r = interest / 100
            
            # Build year-by-year calculation
            yearly_contributions = np.zeros(total_years)
            for phase in st.session_state.contribution_phases:
                start = phase['start_year']
                end = start + phase['duration']
                yearly_contributions[start:end] += phase['amount']
            
            # Calculate future value year by year
            values_by_year = [capital]  # Start with initial capital
            current_value = capital
            
            for year in range(total_years):
                # Add contribution at start of year, then apply growth for the full year
                current_value = (current_value + yearly_contributions[year]) * (1 + r)
                values_by_year.append(current_value)
            
            total_value = current_value
            retirement_age = age + total_years
            
            st.session_state.future_value = total_value
            st.session_state.retirement_age = retirement_age
            st.session_state.age = age
            st.session_state.values_by_year = values_by_year
            st.session_state.total_years = total_years
            
            st.success(f"You'll have **${total_value:,.2f}** by age **{retirement_age}**.")
            
            # Show growth chart
            fig, ax = plt.subplots(figsize=(10, 5))
            ages = list(range(age, age + total_years + 1))  # Include starting age
            ax.plot(ages, values_by_year, marker='o', markersize=3, linewidth=2, color='green')
            ax.set_xlabel("Age")
            ax.set_ylabel("Portfolio Value ($)")
            ax.set_title("Investment Growth Over Time")
            ax.grid(True, alpha=0.3)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}k'))
            plt.tight_layout()
            st.pyplot(fig)

    if "future_value" in st.session_state:
        with st.expander("💾 Save this Scenario for Comparison"):
            with st.form("save_scenario_form"):
                scenario_name = st.text_input("Scenario Name")
                save_clicked = st.form_submit_button("💾 Save Scenario")
                if save_clicked:
                    if scenario_name.strip() == "":
                        st.warning("Please enter a scenario name.")
                    else:
                        scenario_data = {
                            "name": scenario_name,
                            "capital": capital,
                            "age": age,
                            "interest": interest,
                            "total_years": total_years,
                            "contribution_phases": st.session_state.contribution_phases,
                            "future_value": st.session_state.future_value,
                            "retirement_age": st.session_state.retirement_age,
                        }
                        try:
                            with open(os.path.join(SCENARIOS_DIR, f"{scenario_name}.json"), "w") as f:
                                json.dump(scenario_data, f, indent=2)
                            st.success(f"Scenario '{scenario_name}' saved successfully.")
                        except Exception as e:
                            st.error(f"Failed to save scenario: {e}")

    st.header("Post-Retirement Spending Plan")

    if "future_value" in st.session_state and "retirement_age" in st.session_state:
        col12, col13 = st.columns(2)
        with col12:
            target = st.number_input(
                "Target death age (lol)",
                min_value=st.session_state.age + 1,
                max_value=130,
                value=100,
                key="target_age"
            )

        remaining_years = target - st.session_state.retirement_age
        if remaining_years > 0:
            yearly_spending = st.session_state.future_value / remaining_years
            monthly_spending = yearly_spending / 12
            with col13:
                st.info(f"Spend about **${yearly_spending:,.2f}**/year")
                st.info(f"or **${monthly_spending:,.2f}**/month until age {target} (years to spend: {remaining_years})")
        else:
            st.warning("You will be 100 or older at the end of your investment period.")
    else:
        st.info("👆 Calculate retirement funds first to unlock this section.")

    st.sidebar.header("📊 Compare Retirement Scenarios")
    scenario_files = [f for f in os.listdir(SCENARIOS_DIR) if f.endswith(".json")]
    selected_files = st.sidebar.multiselect("Select Scenarios to Compare", scenario_files)

    if st.sidebar.button("Compare Selected Scenarios") and selected_files:
        fig, ax = plt.subplots(figsize=(10, 6))

        for file in selected_files:
            with open(os.path.join(SCENARIOS_DIR, file)) as f:
                data = json.load(f)
                initial_age = data["age"]
                initial_value = data["capital"]
                r = data["interest"] / 100
                
                # Check if it's old format or new format
                if "contribution_phases" in data:
                    # New format with timeline
                    total_years = data.get("total_years", 30)
                    yearly_contributions = np.zeros(total_years)
                    for phase in data["contribution_phases"]:
                        start = phase['start_year']
                        end = start + phase['duration']
                        yearly_contributions[start:end] += phase['amount']
                    
                    x_vals = []
                    y_vals = []
                    age = initial_age
                    value = initial_value
                    
                    for year in range(total_years):
                        value = value * (1 + r) + yearly_contributions[year]
                        x_vals.append(age)
                        y_vals.append(value)
                        age += 1
                else:
                    # Old format - sequential phases
                    x_vals = []
                    y_vals = []
                    age = initial_age
                    value = initial_value
                    
                    for contrib, yrs in data["contributions"]:
                        for _ in range(yrs):
                            value = value * (1 + r) + contrib
                            x_vals.append(age)
                            y_vals.append(value)
                            age += 1

                ax.plot(x_vals, y_vals, label=f"{data['name']} ({data['interest']}%)", linewidth=2, marker='o', markersize=3)

        ax.set_xlabel("Age")
        ax.set_ylabel("Investment Value ($)")
        ax.set_title("Retirement Scenario Comparison")
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}k'))
        plt.tight_layout()
        st.pyplot(fig)

        # Gather and display scenario investment summary
        summary_data = []
        for file in selected_files:
            with open(os.path.join(SCENARIOS_DIR, file)) as f:
                data = json.load(f)
                
                if "contribution_phases" in data:
                    # New format
                    total_years = data.get("total_years", 30)
                    yearly_contributions = np.zeros(total_years)
                    for phase in data["contribution_phases"]:
                        start = phase['start_year']
                        end = start + phase['duration']
                        yearly_contributions[start:end] += phase['amount']
                    total_contributions = sum(yearly_contributions)
                    years = total_years
                else:
                    # Old format
                    total_contributions = sum(contrib * yrs for contrib, yrs in data["contributions"])
                    years = sum(yrs for _, yrs in data["contributions"])
                
                total_invested = data["capital"] + total_contributions
                summary_data.append({
                    "Scenario Name": data["name"],
                    "Capital ($)": f"${data['capital']:,.2f}",
                    "Years": f"{years}",
                    "Total Contributions ($)": f"${total_contributions:,.2f}",
                    "Total Invested ($)": f"${total_invested:,.2f}"
                })

        st.subheader("📋 Scenario Summary Table")
        st.table(summary_data)
        
        # Final ranking
        st.subheader("🏆 Ranked Retirement Plans")
        st.write("Rankings based on least expensive overtime offering highest yield.")

        ranking = []
        for file in selected_files:
            data = json.load(open(os.path.join(SCENARIOS_DIR, file)))
            
            if "contribution_phases" in data:
                # New format
                total_years = data.get("total_years", 30)
                yearly_contributions = np.zeros(total_years)
                for phase in data["contribution_phases"]:
                    start = phase['start_year']
                    end = start + phase['duration']
                    yearly_contributions[start:end] += phase['amount']
                contrib_total = sum(yearly_contributions)
            else:
                # Old format
                contrib_total = sum(c * y for c, y in data["contributions"])
            
            invested_total = data["capital"] + contrib_total
            future_value = data["future_value"]

            ranking.append({
                "Scenario Name": data["name"],
                "Final Value ($)": future_value,
                "Total Invested ($)": invested_total,
            })

        # Sort by highest return, then lowest cost
        ranking.sort(key=lambda x: (-x["Final Value ($)"], x["Total Invested ($)"]))

        for i, row in enumerate(ranking):
            row["Rank"] = i + 1
            row["Final Value ($)"] = f"${row['Final Value ($)']:,.2f}"
            row["Total Invested ($)"] = f"${row['Total Invested ($)']:,.2f}"

        st.table(ranking)
