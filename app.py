# Import required libraries
import streamlit as st
import plotly.graph_objs as go

# Sample data for the line graph
x_values = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
y_values = [10, 15, 8, 25, 18]

# Create a Plotly figure
fig = go.Figure(
    data=go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        name='Sample Data'
    )
)

# Customize layout
fig.update_layout(
    title="Monthly Data",
    xaxis_title="Month",
    yaxis_title="Value",
    template="plotly_dark"
)

# Streamlit app layout
st.title("Basic Line Graph")
st.plotly_chart(fig)
