import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def plot_graph(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Simple Graph')
    st.pyplot(fig)

def main():
    st.title('Matplotlib Graphs with Streamlit')

    # Sidebar
    st.sidebar.header('Parameters')
    num_points = st.sidebar.slider('Number of points', 10, 100, 50)

    # Generate data
    x = np.linspace(0, 10, num_points)
    y = np.sin(x)
    n=7
    # Plot the graph
    plot_graph(x, y)

if __name__ == "__main__":
    main()
