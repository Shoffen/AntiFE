import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph





def get_plot(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    plt.title('Kraujo tyrimai')
    
    # Plot the line
    plt.plot(x, y, marker='o', linestyle='-')
    
    plt.xlabel('Data')
    plt.ylabel('Fenilalaninas')
    # Set x and y axis ticks to only include data corresponding to your points
    plt.xticks(x)
    plt.yticks(y)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the plot to a buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph

