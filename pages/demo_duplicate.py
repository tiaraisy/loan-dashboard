import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Demo Dashboard",
    page_icon="💡",
    layout='wide'
)

st.title("Financial Insights Dashboard: Loan Performance & Trends")

st.markdown("---")

st.sidebar.header("Dashboard Filters and Features")
st.sidebar.markdown(
"""
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
"""
)
loan = pd.read_pickle('data_input/loan_clean')
loan['purpose'] = loan['purpose'].str.replace("-","")

with st.container(border=True):
    col1,col2 = st.columns(2)

    with col1:
        st.metric('Total Loans', f"{loan['id'].count():,.0f}", help="Total Number of Loans")
        st.metric('Total Loan Amount', f"${loan['loan_amount'].sum():,.0f}")

    with col2:
        st.metric('Total Loan Amount', f"{loan['interest_rate'].mean():,.0f}%")
        st.metric('Total Loan Amount', f"${loan['loan_amount'].mean():,.0f}")

import plotly.express as px


with st.container(border=True):
    tab1, tab2, tab3 = st.tabs(['Loans Issued Over Time','Loan Amount Over Time', 'Issue Date Analysis'])

    with tab1:
        loan_date_count = loan.groupby('issue_date')['loan_amount'].count()

        line_count = px.line(
            loan_date_count,
            markers=True,
            title='Number of Loans Issued Over Time',
            labels={
            'issue_date':'Issue Date',
            'value':'Number of Loans'
        }
        ).update_layout(showlegend=False)

        st.plotly_chart(line_count)

    with tab2:
        loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()

        line_sum = px.line(
            loan_date_sum,
            markers=True,
            labels={
                'value':'Number of Loans',
                'issue_date':'Issue Date'
            },
            template='seaborn',
            title="Loans Amount Over Time"
        ).update_layout(showlegend=False)
        
        st.plotly_chart(line_sum)

    with tab3:
        loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()

        line_dist = px.bar(
            loan_day_count,
            category_orders={
            'issue_weekday':['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
            },
            title='Number of Loans Over Time',
            labels={
            'value':'Number of Loans',
            'issue_weekday':'Day of the Week'
            },
            template='seaborn'
        ).update_layout(showlegend=False)
        
        st.plotly_chart(line_dist)

with st.expander("Click Here to Expand Visualization"):
    col3, col4 = st.columns(2)

    with col3:
        pie = px.pie(
            loan, 
            names='loan_condition', 
            title='Distribution of Loans by Condition', 
            hole=0.4,  # Creates the donut chart style
            template='seaborn'
    ).update_traces(textinfo='percent + value')
        
        st.plotly_chart(pie)

    with col4:
        grade = loan['grade'].value_counts().sort_index()

        bar_grade = px.bar(
            grade,
            title='Distribution of Loans by Grade',
            labels={
                'value':'Number of Loans',
                'grade':'Grade'
            },
            template='seaborn'
        ).update_layout(showlegend=False)

        st.plotly_chart(bar_grade)

condition = st.selectbox("Select Loan Condition",["Good Loan","Bad Loan"])
loan_condition = loan[loan['loan_condition'] == condition]

with st.container(border=True):
    tab1, tab2 = st.tabs(['Loans Amount Distribution','Loan Amount Distribution by Purpose'])

    with tab1:

        hist_loan_by_condition = px.histogram(
            loan_condition,
            x = 'loan_amount',
            nbins=20,
            color='term', #kolom pada dataframe untuk memecah/menentukan perbedaan warna

            labels={
            'loan_amount': 'Loan Amount',
            'count': 'Number of Loans',
            'income_category': 'Income Category',
            'term': 'Duration of Loan'
            },
        template='seaborn'
        ).update_layout(showlegend=False)

        st.plotly_chart(hist_loan_by_condition)

    with tab2:
        box_dist_by_purpose = px.box(
            loan_condition,
            x = 'purpose',
            y='loan_amount',
            color = 'term',
             title='Loan Amount Distribution by Purpose',

            labels={
            'loan_amount': 'Loan Amount',
            'purpose': 'Loan Purpose',
            'term':'Loan Term'
            },
        template='seaborn'
        ).update_layout(showlegend=False)

        st.plotly_chart(box_dist_by_purpose)

