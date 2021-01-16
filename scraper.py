
import dataset
import get_retries
from bs4 import BeautifulSoup
from dateparser import parse

db = dataset.connect("sqlite:///data.sqlite")

tab_incidents = db["incidents"]
tab_sources = db["sources"]
tab_chronicles = db["chronicles"]


tab_chronicles.insert(
    {
        "iso3166_1": "DE",
        "iso3166_2": "DE-TH",
        "chronicler_name": "ezra",
        "chronicler_description": "ezra ist die Beratung für Betroffene rechter, rassistischer und antisemitischer Gewalt in Thüringen. Wir beraten, begleiten und unterstützen Menschen, die aus Motiven gruppenbezogener Menschenfeindlichkeit angegriffen werden – also deshalb, weil die Täter*innen sie einer von ihnen abgelehnten Personengruppe zuordnen. Daneben richtet sich unser Angebot auch an Angehörige von Betroffenen und an Zeug*innen.",
        "chronicler_url": "https://ezra.de/",
        "chronicle_source": "https://ezra.de/chronik/",
    }
)


url = "https://angstraeume.ezra.de/wp-json/ezra/v1/chronic"

json_data = get_retries.get(url, verbose=True, max_backoff=128).json()

meta_motives = json_data["meta"]["motives"]
meta_locations = json_data["meta"]["locations"]

for x in json_data["entries"]:
    city = x["locationDisplay"]

    county = meta_locations[str(x["locations"][0])] if len(x["locations"]) > 0 else None

    date = parse(x["startDisplay"], languages=["de"])
    title = x["title"]
    description = BeautifulSoup(x["content"], "lxml").get_text().strip()
    rg_id = "ezra-" + str(x["id"])
    motives = ", ".join([meta_motives[str(xx)] for xx in x["motives"]])

    data = dict(
        url="https://ezra.de/chronik/",
        rg_id=rg_id,
        date=date,
        city=city,
        county=county,
        title=title,
        description=description,
        chronicler_name="ezra",
    )

    tab_incidents.insert(data, ["rg_id"])

    sources = x["sourceName"].replace("; ", ", ").split(",")
    sources_data = [
        dict(rg_id=rg_id, name=s.strip(), url=x["sourceUrl"]) for s in sources
    ]
    for s in sources_data:
        tab_sources.insert(s)
