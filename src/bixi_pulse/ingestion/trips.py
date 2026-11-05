"""Conversion des trajets historiques BIXI (CSV) en Parquet partitionné par mois."""
from datetime import datetime, timezone
from pathlib import Path

import duckdb

CSV_COLUMNS = {
    "STARTSTATIONNAME": "VARCHAR",
    "STARTSTATIONARRONDISSEMENT": "VARCHAR",
    "STARTSTATIONLATITUDE": "DOUBLE",
    "STARTSTATIONLONGITUDE": "DOUBLE",
    "ENDSTATIONNAME": "VARCHAR",
    "ENDSTATIONARRONDISSEMENT": "VARCHAR",
    "ENDSTATIONLATITUDE": "DOUBLE",
    "ENDSTATIONLONGITUDE": "DOUBLE",
    "STARTTIMEMS": "BIGINT",
    "ENDTIMEMS": "BIGINT",
}


def convert_csv_to_parquet(csv_path: Path, output_dir: Path) -> None:
    """Lit le CSV en streaming et écrit un dossier Parquet par mois de départ."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ingested_at = datetime.now(timezone.utc).isoformat()
    con = duckdb.connect()
    con.execute("SET TimeZone = 'UTC'")
    con.execute(f"""
        COPY (
            SELECT
                STARTSTATIONNAME              AS start_station_name,
                STARTSTATIONARRONDISSEMENT    AS start_station_borough,
                STARTSTATIONLATITUDE          AS start_station_lat,
                STARTSTATIONLONGITUDE         AS start_station_lon,
                ENDSTATIONNAME                AS end_station_name,
                ENDSTATIONARRONDISSEMENT      AS end_station_borough,
                ENDSTATIONLATITUDE            AS end_station_lat,
                ENDSTATIONLONGITUDE           AS end_station_lon,
                epoch_ms(STARTTIMEMS)::TIMESTAMPTZ AS started_at,
                epoch_ms(ENDTIMEMS)::TIMESTAMPTZ   AS ended_at,
                strftime(epoch_ms(STARTTIMEMS), '%Y-%m') AS trip_month,
                '{csv_path.name}'             AS source_file,
                TIMESTAMPTZ '{ingested_at}'   AS ingested_at
            FROM read_csv('{csv_path.as_posix()}', header = true, columns = {CSV_COLUMNS})
        )
        TO '{output_dir.as_posix()}'
        (FORMAT parquet, PARTITION_BY (trip_month), OVERWRITE_OR_IGNORE true)
    """)
    con.close()