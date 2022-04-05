# LAC Access Site

Web Archive access site for the Libraries and Archives, Canada.

This is a Django-based backend designed to provide access to the LAC's web collections. It's using templating and HTTP on the backend to render these pages. The templates use the Government of Canada's GCWeb framework. SQLite is used to store some site-specific data.

The "lac" app provides views for those collections.

## Settings Overview
* API_KEY - used for authenticated requests to the AIT partner site API, generated via the admin. Configured via ansible + ansible vault
* API_ROOT - partner API endpoint. Configured via ansible
* SEARCH_ROOT - Opensearch endpoint for the fulltext search functionality, configured in ansible.
