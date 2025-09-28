#DDL
team_get_players = """
CREATE TABLE IF NOT EXISTS team_get_players (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    imageId BIGINT,
    battingStyle VARCHAR(50),
    bowlingStyle VARCHAR(50)
)
"""

team_get_players_data = """
INSERT INTO players (id, name, imageId, battingStyle, bowlingStyle)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            imageId = VALUES(imageId),
            battingStyle = VALUES(battingStyle),
            bowlingStyle = VALUES(bowlingStyle)
"""