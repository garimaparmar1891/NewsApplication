ADD_OR_UPDATE_REACTION = """
MERGE INTO ArticleReactions AS target
USING (SELECT ? AS UserId, ? AS ArticleId) AS source
ON target.UserId = source.UserId AND target.ArticleId = source.ArticleId
WHEN MATCHED THEN
    UPDATE SET ReactionType = ?
WHEN NOT MATCHED THEN
    INSERT (UserId, ArticleId, ReactionType)
    VALUES (?, ?, ?);
"""

GET_REACTIONS_BY_USER = """
SELECT ArticleId, ReactionType, ReactedAt
FROM ArticleReactions
WHERE UserId = ?
ORDER BY ReactedAt DESC
"""

DELETE_REACTION = """
DELETE FROM ArticleReactions
WHERE UserId = ? AND ArticleId = ?
"""
