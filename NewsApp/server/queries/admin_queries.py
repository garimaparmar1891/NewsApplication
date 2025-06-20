GET_EXTERNAL_SERVERS = """
    SELECT Id, Name, ApiKey, BaseUrl, IsActive, LastAccessed
    FROM ExternalServers
"""

INSERT_EXTERNAL_SERVER = """
    INSERT INTO ExternalServers (Name, ApiKey, BaseUrl)
    VALUES (?, ?, ?)
"""

DELETE_EXTERNAL_SERVER = """
    DELETE FROM ExternalServers
    WHERE Id = ?
"""

GET_CATEGORIES = """
    SELECT Id, Name
    FROM Categories
"""

INSERT_CATEGORY = """
    INSERT INTO Categories (Name)
    VALUES (?)
"""

DELETE_CATEGORY = """
    DELETE FROM Categories
    WHERE Id = ?
"""

UPDATE_EXTERNAL_SERVER_BASE = """
    UPDATE ExternalServers
    SET {fields}
    WHERE Id = ?
"""
