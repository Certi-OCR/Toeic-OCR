# Language Certificate Extraction API

An open-source API service for extracting information from language certificates through image processing and OCR technologies.

## Overview

This API allows you to extract structured information from TOEIC language certificates by uploading an image file or providing a URL to an image. The service can return the extracted data in JSON format or display the original image with bounding boxes highlighting the detected information.

## API Endpoints

### Extract Information from Uploaded Image

```
POST /api/file_to_json
```

Upload an image file of a TOEIC certificate and receive structured JSON data containing the extracted information.

**Request:**

- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Form data with a file field named `file`

**Response:**

- Content-Type: `application/json`
- Body: JSON object containing extracted certificate information

### Visualize Bounding Boxes from Uploaded Image

```
POST /api/file_to_bbox
```

Upload an image file of a TOEIC certificate and receive the same image with bounding boxes highlighting the detected information.

**Request:**

- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Form data with a file field named `file`

**Response:**

- Content-Type: `image/jpeg` or `image/png`
- Body: Image with bounding boxes drawn around detected certificate information

### Extract Information from URL

```
POST /api/url_to_json
```

Provide a URL to an image of a TOEIC certificate and receive structured JSON data containing the extracted information.

**Request:**

- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Form data with a field named `url` containing the image URL

**Response:**

- Content-Type: `application/json`
- Body: JSON object containing extracted certificate information

### Visualize Bounding Boxes from URL

```
POST /api/url_to_bbox
```

Provide a URL to an image of a TOEIC certificate and receive the image with bounding boxes highlighting the detected information.

**Request:**

- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Form data with a field named `url` containing the image URL

**Response:**

- Content-Type: `image/jpeg` or `image/png`
- Body: Image with bounding boxes drawn around detected certificate information

## Example Response Structure

The JSON responses will typically include structured data such as:

```json
[
  {
    "name": "Reading",
    "confidence": 0.9181289076805115,
    "text": {
      "content": "475",
      "confidence": 0.9993767142295837
    }
  },
  {
    "name": "Listening",
    "confidence": 0.9007121920585632,
    "text": {
      "content": "425",
      "confidence": 0.9988334774971008
    }
  },
  {
    "name": "Total_score",
    "confidence": 0.8998973369598389,
    "text": {
      "content": "900",
      "confidence": 0.9988196492195129
    }
  },
  {
    "name": "Date_of_Birth",
    "confidence": 0.8646478056907654,
    "text": {
      "content": "2003/08/02",
      "confidence": 0.9971586465835571
    }
  },
  {
    "name": "Name",
    "confidence": 0.8523585796356201,
    "text": {
      "content": "DoanChiKien",
      "confidence": 0.9955270886421204
    }
  },
  {
    "name": "Valid_Until",
    "confidence": 0.8487711548805237,
    "text": {
      "content": "2026/05/03",
      "confidence": 0.9976865649223328
    }
  },
  {
    "name": "Test_date",
    "confidence": 0.7915072441101074,
    "text": {
      "content": "2024/05/03",
      "confidence": 0.9984976053237915
    }
  },
  {
    "name": "Identification",
    "confidence": 0.7884018421173096,
    "text": {
      "content": "046103734623",
      "confidence": 0.9976439476013184
    }
  }
]
```

## Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Certi-OCR/Toeic-OCR.git
   cd Toeic-OCR
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage Examples

### Using cURL

**Extract information from a file:**

```bash
curl -X POST -F "file=@/path/to/toeic-certificate.jpg" http://localhost:8000/api/file_to_json
```

**Extract information from a URL:**

```bash
curl -X POST -F "url=https://example.com/toeic-certificate.jpg" http://localhost:8000/api/url_to_json
```

### Using Python

```python
import requests

# From file
files = {'file': open('toeic-certificate.jpg', 'rb')}
response = requests.post('http://localhost:8000/api/file_to_json', files=files)
print(response.json())

# From URL
data = {'url': 'https://example.com/toeic-certificate.jpg'}
response = requests.post('http://localhost:8000/api/url_to_json', data=data)
print(response.json())
```

## Supported Certificate Types

Currently, this API only supports:

- TOEIC (Test of English for International Communication)

Future versions plan to expand support to other certificate types.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Priority Areas for Contribution

- Support for additional language certificate types
- Improved OCR accuracy for TOEIC certificates
- Performance optimizations
- Documentation improvements

## License

This project is licensed under the MIT License - see the LICENSE file for details.
