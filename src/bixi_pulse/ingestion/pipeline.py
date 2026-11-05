from bixi_pulse.ingestion.gbfs import fetch_feed, to_rows
from bixi_pulse.ingestion.lake_writer import write_rows

def main() -> None:
    rows = to_rows(fetch_feed("station_status"))
    path = write_rows(rows, "station_status")
    print(f"{len(rows)} stations écrites dans bronze/{path}")

if __name__ == "__main__":
    main()