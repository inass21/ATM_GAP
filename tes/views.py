import io
import base64
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from django.shortcuts import render

def chart_view(request):
    x_data = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    y_data = [10, 25, 18, 40, 32]

    plt.figure(figsize=(6, 4))
    plt.plot(x_data, y_data, marker='o', color='blue', linewidth=2)
    plt.title('Monthly Sales Performance')
    plt.xlabel('Months')
    plt.ylabel('Revenue ($)')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)

    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graph_base64 = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'chart.html', {
        'chart_data': graph_base64
    })