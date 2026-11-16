
from bixi_pulse.ingestion.gbfs import fetch_feed, to_rows
from bixi_pulse.ingestion.lake_writer import write_rows

FEEDS = ["station_status", "station_information"]


def main() -> None:
    for feed in FEEDS:
        rows = to_rows(fetch_feed(feed))
        path = write_rows(rows, feed)
        print(f"{len(rows)} lignes écrites dans bronze/{path}")


if __name__ == "__main__":
    main()