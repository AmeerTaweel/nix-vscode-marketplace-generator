class Constants():
    API_URL = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery/"
    API_VERSION = "3.0-preview.1"
    REQUEST_STARTING_PAGE_NUMBER = 1
    REQUEST_PAGE_SIZE = 1000
    REQUEST_HEADERS = {
        "content-type": "application/json",
        "accept": f"application/json; api-version={API_VERSION}",
        "accept-encoding": "gzip"
    }
    REQUEST_BODY = {
        "filters": [{
            "criteria": [{
                "filterType": 8, 
                "value": "Microsoft.VisualStudio.Code"
            }],
            "pageNumber": REQUEST_STARTING_PAGE_NUMBER,
            "pageSize": REQUEST_PAGE_SIZE,
            "sortBy": 0,
            "sortOrder": 0
        }],
        "assetTypes": [],
        "flags": 0
    }
    CHUNK_SIZE = 100
    STATUS_OK = 200
    ZIP_DIR = "zip"