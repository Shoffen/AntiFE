import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x, y, dates):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    plt.title('Kraujo tyrimai')
    
    # Plot the line
    plt.plot(x, y, marker='o', linestyle='-')
    
    plt.xlabel('Data')
    plt.ylabel('Fenilalaninas µmol/l')
    
    plt.xticks(rotation=45, ha='right')  # Set ticks with the calculated interval
    # Customize y-axis ticks to range from 0 to 900 with increments of 100
    plt.yticks(np.arange(0, 900, 100))
    
    # Set x-axis tick labels to the corresponding dates
   
    plt.gca().set_xticks(np.linspace(0, len(x) - 1, len(dates)))
    plt.gca().set_xticklabels(dates)
    
    # Add shaded region for the "normal" range
    plt.axhspan(120, 600, color='green', alpha=0.3)
    
    # Set y-axis limits explicitly
    plt.ylim(0, 900)
    
    # Adjust figure margins
    plt.subplots_adjust(bottom=0.2)  # Adjust bottom margin to make room for rotated labels

    # Save the plot to a buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph
