# test_app.py
import pytest
from io import BytesIO

from PIL.Image import Image

from src.main import app

@pytest.fixture
def client():
    # app = create_app()
    app.config.update({
        "TESTING": True,
    })
    with app.test_client() as client:
        yield client

def test_process_stack_success(client):
    # Prepare a fake TIFF file in memory (could be a dummy image as we’re testing the endpoint)
    fake_tiff = BytesIO()
    fake_image = Image.new("L", (100, 100))
    fake_image.save(fake_tiff, format="TIFF")
    fake_tiff.seek(0)  # Rewind the file pointer

    # Make POST request to the /segment endpoint
    response = client.post(
        '/segment',
        data={'file': (fake_tiff, 'test_stack.tif')},
        content_type='multipart/form-data'
    )
    # Assert response status code and content
    assert response.status_code == 200
    # data = response.get_json()
    # assert isinstance(data, list)  # Expecting a list of tracking data
    # assert len(data) > 0
    # assert "Object Index" in data[0]  # Check that tracking data has expected keys
