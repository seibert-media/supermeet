from datetime import datetime, timedelta

from requests import Session

from . import CONFIG


class AnnyAPI:
    def __init__(self):
        self._resources = {}
        self._last_resource_get = datetime.now() - timedelta(days=1)

        self.session = Session()
        self.session.headers = {
            "Authorization": f"Bearer {CONFIG.get('anny_api_key')}",
        }

    def _paginated_get(self, api_endpoint):
        data = []
        if "?" in api_endpoint:
            next_link = f"{api_endpoint}&page[size]=50&page[number]=1"
        else:
            next_link = f"{api_endpoint}?page[size]=50&page[number]=1"
        while next_link:
            r = self.__get(next_link)
            data.extend(r["data"])
            next_link = r.get("links", {}).get("next")
        return data

    def __get(self, api_endpoint):
        if not api_endpoint.startswith("https://b.anny.co"):
            api_endpoint = f"https://b.anny.co/api/v1/{api_endpoint}"
        r = self.session.get(api_endpoint, timeout=5)
        r.raise_for_status()
        return r.json()

    def get_resources(self):
        if not self._resources or datetime.now() - self._last_resource_get > timedelta(
            minutes=10
        ):
            resources = {}
            api_result = self._paginated_get(
                "resources?filter[exclude_child_resources]=false"
            )
            for item in api_result:
                item_id = int(item["id"])
                if item["meta"]["parent_id"]:
                    parent_id = int(item["meta"]["parent_id"])
                    resources.setdefault(parent_id, {}).setdefault("children", {})
                    resources[parent_id]["children"][item_id] = item["attributes"][
                        "name"
                    ]
                else:
                    resources.setdefault(item_id, {}).setdefault("children", {})
                    resources[item_id]["name"] = item["attributes"]["name"]
                    resources[item_id]["description"] = item["attributes"][
                        "description"
                    ]
                    resources[item_id]["plain_description"] = item["attributes"][
                        "plain_description"
                    ]

            self._resources = resources
            self._last_resource_get = datetime.now()
        return self._resources

    def get_events(self, start=None, until=None, resources=None):
        if start is None:
            start = datetime.utcnow() - timedelta(days=1)

        if until is None:
            until = start + timedelta(days=14)

        if resources is None:
            resources = [None]

        all_events = []

        for resource in resources:
            resource_filter = ""
            if resource:
                resource_filter += f"&filter[resources]={resource}"

            events = self._paginated_get(
                "bookings?include=resource&filter[end_date]={end}&filter[start_date]={start}{resource_filter}".format(
                    start=start.isoformat()[:19],
                    end=until.isoformat()[:19],
                    resource_filter=resource_filter,
                )
            )
            for booking in events:
                if booking["attributes"]["status"] in (
                    "accepted",
                    "requested",
                    "reserved",
                ):
                    all_events.append(booking)

        return all_events


# we need to initialize this here so we can have caching
anny_api = AnnyAPI()
