import io
from datetime import datetime
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

from bixi_pulse.config import AZURE_STORAGE_ACCOUNT, BRONZE_CONTAINER



def get_service_client() -> DataLakeServiceClient:
    """Create a DataLakeServiceClient using DefaultAzureCredential."""
    account_url = f"https://{AZURE_STORAGE_ACCOUNT}.dfs.core.windows.net"
    return DataLakeServiceClient(account_url=account_url, credential=DefaultAzureCredential())

def _to_parquet_bytes(rows: list[dict[str, Any]]) -> bytes:
    table = pa.Table.from_pylist(rows)
    buffer = io.BytesIO()
    pq.write_table(table, buffer)
    return buffer.getvalue()

def build_path(dataset: str, ingested_at: datetime) -> str:
    """Construit le chemin partitionné du fichier dans le lake."""
    return (
        f"{dataset}/ingestion_date={ingested_at:%Y-%m-%d}/"
        f"{ingested_at:%Y-%m-%dT%H-%M-%S}.parquet"
    )

def write_rows(rows: list[dict[str, Any]], dataset: str) -> str:
    if not rows:
        raise ValueError("Aucune ligne à écrire.")
    
    path = build_path(dataset, rows[0]["ingested_at"])
    file_system = get_service_client().get_file_system_client(BRONZE_CONTAINER)
    file_system.get_file_client(path).upload_data(_to_parquet_bytes(rows), overwrite=True)
    return path
    
 
    
    