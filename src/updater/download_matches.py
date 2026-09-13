from pathlib import Path

import requests

from config import LEAGUES, SEASONS


BASE_URL = "https://www.football-data.co.uk/mmz4281"


def download_file(url, output):

    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        print(f"✗ {url}")
        return

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_bytes(response.content)

    print(f"✓ {output.name}")


def main():

    root = Path(__file__).resolve().parents[2]

    raw_dir = root / "data" / "raw"

    for season in SEASONS:

        season_dir = raw_dir / season

        for league in LEAGUES:

            url = (
                f"{BASE_URL}/"
                f"{season}/"
                f"{league}.csv"
            )

            output = season_dir / f"{league}.csv"

            download_file(
                url,
                output,
            )


if __name__ == "__main__":
    main()