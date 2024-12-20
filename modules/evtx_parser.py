from Evtx.Evtx import Evtx
from xml.etree.ElementTree import fromstring

def parse_evtx_file(evtx_file):
    """Parse EVTX file and return useful log entries."""
    logs = []
    with Evtx(evtx_file) as log:
        for record in log.records():
            xml_data = fromstring(record.xml())
            event_id = xml_data.find(".//EventID").text
            time_created = xml_data.find(".//TimeCreated").get("SystemTime")
            provider = xml_data.find(".//Provider").get("Name")

            logs.append({
                "event_id": event_id,
                "time_created": time_created,
                "provider": provider
            })
    return logs
