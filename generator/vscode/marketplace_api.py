import aiohttp
import asyncio
import json
import os

from utils import log
from utils.log import console
from utils import nix
from vscode.constants import Constants
from zipfile import ZipFile

async def get_extensions_data_page(page) -> tuple[bool, list[dict]]:
    with console.status(f"[bold yellow]Getting page {page} of extensions data..."):
        async with aiohttp.ClientSession() as session:
            url = Constants.API_URL
            headers = Constants.REQUEST_HEADERS
            json = Constants.REQUEST_BODY
            # set correct page number
            json["filters"][0]["pageNumber"] = page

            # perform http request
            async with session.post(url, headers = headers, json = json) as response:
                
                if response.status != Constants.STATUS_OK:
                    log.error(f"Getting page {page} of extensions data failed")
                    return False, []

                try:
                    data = await response.json()
                except:
                    log.error(f"Getting page {page} of extensions data failed")
                    return False, []

                extensions_data = data["results"][0]["extensions"]

                log.success(f"Fetched page {page} of extensions data")

                extensions = [{
                    "id": e["extensionId"],
                    "name": e["extensionName"],
                    "publisher": e["publisher"]["publisherName"],
                    "last_updated": e["lastUpdated"]
                } for e in extensions_data]

                return True, extensions

async def get_extensions_data() -> list[dict]:
    page = Constants.REQUEST_STARTING_PAGE_NUMBER
    extensions = []
    while True:
        success, page_extensions = await get_extensions_data_page(page)
        if not success:
            with console.status(f"[bold yellow]Wait to retry fetching page {page}..."):
                # sleep for one minute
                await asyncio.sleep(60)
                continue
        extensions += page_extensions
        if len(page_extensions) == 0:
            log.success("Fetched extensions data")
            log.info(f"Found {len(extensions)} extensions")
            return extensions
        page += 1

async def download_extensions(extensions: list[dict]) -> list[dict]:
    i = 0
    while True:
        if i >= len(extensions):
            log.success(f"Downloaded {len(extensions)} extensions")
            break
        e = extensions[i]
        success = await download_extension(e, i)
        if not success:
            with console.status(f"[bold yellow]Wait to retry downloading {nix.get_nix_package_name(e)}..."):
                # sleep for one minute
                await asyncio.sleep(60)
                continue
        i += 1

async def download_extension(e: dict, i: int) -> bool:
    if not os.path.exists(Constants.ZIP_DIR):
        os.mkdir(Constants.ZIP_DIR)

    with console.status(f"[bold yellow]Downloading extension [{i}]..."):
        async with aiohttp.ClientSession() as session:
            async with session.get(get_download_url(e)) as response:
                if response.status != Constants.STATUS_OK:
                    log.error(f"Downloading [{i}] {nix.get_nix_package_name(e)} failed")
                    return False

                with open(get_zip_file_path(e), "wb") as f:
                    try:
                        async for chunk in response.content.iter_chunked(Constants.CHUNK_SIZE):
                            f.write(chunk)
                        log.success(f"Downloaded [{i}] {nix.get_nix_package_name(e)}")
                        return True
                    except:
                        log.error(f"Downloading [{i}] {nix.get_nix_package_name(e)} failed")
                        return False

def get_download_url(extension: dict) -> str:
    return f"https://{extension['publisher']}.gallery.vsassets.io/_apis/public/gallery/publisher/{extension['publisher']}/extension/{extension['name']}/latest/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage"

def get_zip_file_path(extension: dict) -> str:
    return f"{Constants.ZIP_DIR}/{nix.get_nix_package_name(extension)}.zip"

def extract_versions(extensions: list[dict]) -> list[str]:
    versions = []
    with console.status("[bold yellow]Extracting extension versions..."):
        for e in extensions:
            with ZipFile(get_zip_file_path(e), "r") as zip:
                info = json.loads(zip.read("extension/package.json"))
                versions.append(info["version"])
    log.success("Extracted versions")
    return versions

def compute_sha256(extensions: list[dict]) -> list[str]:
    sha256 = []
    with console.status("[bold yellow]Computing extension SHA256..."):
        for e in extensions:
            command_output = os.popen(f"nix-hash --flat --base32 --type sha256 {get_zip_file_path(e)}").read()
            sha256.append(command_output.replace("\n", ""))
    log.success("Computed SHA256")
    return sha256