import logging
from typing import Any, IO, Dict, List
from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient, TableClient

logger = logging.getLogger(__name__)

class TableStorageClient:
    def __init__(self, connection_string: str, table_name: str):
        table_service: TableServiceClient = TableServiceClient.from_connection_string(connection_string)
        self.table_client: TableClient = table_service.get_table_client(table_name)

    def make_product(self, product_name: str, resolution: str) -> bool:
        """ Create a product in the table"""
        entity = {
            u'PartitionKey': product_name,
            u'RowKey': resolution
        }
        # Check if product already exists
        if entity in self.get_products():
            logging.info(f"Product: {product_name} with resoluton: {resolution} already exists")
            return False
        
        # Make product
        logging.info(f"Making product: {product_name} with resoluton: {resolution}")
        response = self.table_client.create_entity(entity=entity, logging_enable=True)
        return response is not None

    def delete_product(self, product_name: str) -> None:
        logging.info(f"Deleting product: {product_name}")
        parameters = {
            u'PartitionKey': product_name,
        }
        query_filter = "PartitionKey eq @PartitionKey"
        responses = self.table_client.query_entities(query_filter, parameters=parameters)
        logging.info(responses)

    def add_resolution(self, product_name: str, resolution: str) -> Dict[str, str]:
        """ Adds a resolution to the product"""
        logging.info(f"Adding resoluton {resolution} to {product_name}")
        products = self.get_products()
        if (product_name not in products):
            raise ValueError("Product does not exist")
        entity = {
            u'PartitionKey': product_name,
            u'RowKey': resolution
        }
        return self.table_client.create_entity(entity=entity, logging_enable=True)

    def get_products(self) -> List[Dict[str, str]]:
        return self.table_client.list_entities()

class DirectoryClient:
    def __init__(self, connection_string: str, container_name: str):
        service_client: BlobServiceClient = BlobServiceClient.from_connection_string(connection_string)
        self.client = service_client.get_container_client(container_name)

    def download(self, source: str) -> Any:
        """Download a single file to a path on the local filesystem"""
        logging.info(f'Downloading {source}')
        bc = self.client.get_blob_client(blob=source)
        return bc.download_blob()

    def upload(self, destination: str, data: IO) -> None:
        """Upload a single file to a path inside the container"""
        logging.info(f'Uploading to {destination}')
        self.client.upload_blob(name=destination, data=data)

    def make_product(self, product_name: str) -> None:
        pass
    
    def delete_product(self, product_name: str) -> None:
        pass

    def add_resolution(self, product_name: str, resolution: str) -> None:
        pass
    
    def delete_resolution(self, product_name: str, resolution: str) -> None:
        pass