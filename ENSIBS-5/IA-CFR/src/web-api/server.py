"""
Server file for the web API, it uses the access functions to retrieve data from Elasticsearch and display it in the web
interface.
"""
import base64
from io import BytesIO

from PIL import Image
from fastapi import FastAPI, Request
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Import your DataParser class and create an instance of it
from utils.modeling.Indexing import Indexing
from utils.modeling.Accessing import Accessing
from utils.config.ElasticConfig import ElasticConfig


ElasticConfig = ElasticConfig()
Indexing = Indexing(es=ElasticConfig, index_name="flows")

templates = Jinja2Templates(directory="templates")

# Define the available functions
available_functions = {
    'test_data': ElasticConfig.test_es_connection,
    'protocolsStats': Accessing.get_stats_protocols,
    'applicationStats': Accessing.get_stats_applications,
    'diagram': Accessing.display_diagram,
    'protocols': Accessing.get_protocols,
    'parse': Indexing.parse,
    'protocol': Accessing.get_protocol_flows,
    'protocolsFlowCard': Accessing.get_protocols_flow_card,
    'protocolsPayloadSize': Accessing.get_protocols_payload_size,
    'protocolsTotalBytes': Accessing.get_protocols_total_bytes,
    'protocolsTotalPackets': Accessing.get_protocols_total_packets,
    'applications': Accessing.get_applications,
    'application': Accessing.get_application_flows,
    'applicationsFlowCard': Accessing.get_applications_flow_card,
    'applicationsPayloadSize': Accessing.get_application_payload_size,
    'applicationsTotalBytes': Accessing.get_application_total_bytes,
    'applicationsTotalPackets': Accessing.get_application_total_packets,
}


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def run_function(request: Request, function: str = Form(...)):
    response = None  # Initialize response as None

    if function in available_functions:
        result = available_functions[function]()

        if "image_data" in result:
            # Check if the result is an image
            try:
                image_data = base64.b64decode(result["image_data"])
                img = Image.open(BytesIO(image_data))
                img.show()  # Display the image

            except Exception as e:
                response = {"message": f"Error displaying image: {str(e)}"}
        else:
            response = {"result": list(result)}

    return templates.TemplateResponse("index.html", {"request": request, "response": response})