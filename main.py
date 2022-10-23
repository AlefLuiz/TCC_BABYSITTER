import uvicorn
from api import app

uvicorn.run(
    app=app,
    host='0.0.0.0',
    port=80
)