GET_ALL_KEYS = """
SELECT Name, ApiKey, IsActive, LastAccessed, BaseUrl
FROM ExternalServers
"""

GET_ACTIVE_SOURCES = """
SELECT Name, ApiKey, IsActive, BaseUrl
FROM ExternalServers
WHERE IsActive = 1
ORDER BY Id ASC
"""
