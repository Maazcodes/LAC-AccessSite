# LAC Access Site

Web Archive access site for the Libraries and Archives, Canada.

This is a Django-based backend designed to provide access to the LAC's web collections. It's using templating and HTTP on the backend to render these pages. The templates use the Government of Canada's GCWeb framework. SQLite is used to store some site-specific data.

The "lac" app provides views for those collections.

## Settings Overview
* API_KEY - used for authenticated requests to the AIT partner site API, generated via the admin. Configured via ansible + ansible vault
* API_ROOT - partner API endpoint. Configured via ansible
* SEARCH_ROOT - Opensearch endpoint for the fulltext search functionality, configured in ansible.


## Search Results Collection Names

The way that collection name is derived in search results is sub-optimal. A list of AIT collection ids is stored in `AccessSiteCollection.ait_collection_map`, which is a `JSONField`. sqlite3 support for querying the JSON-as-JSON requires sqlite 3.38+, or must be manually compiled in. So, we query it as a string. Though unlikely with the small mnumber of collection in use here, this may result in wrong collection name being shown for a search result.
