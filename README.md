# LAC Access Site

Web Archive access site for the Libraries and Archives, Canada.

This is a Django-based backend designed to provide access to the LAC's web collections. It's using templating and HTTP on the backend to render these pages. The templates use the Government of Canada's GCWeb framework. SQLite is used to store some LAC-specific metadata. (TODO: is this actually in AIT)

"lac" provides views for those collections.
"fts_search" provides an interface in front of AIT's full text search.
