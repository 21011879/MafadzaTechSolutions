import psycopg2
from urllib.parse import urlparse
import sys

# Get your Render database URL (from Render dashboard)
DATABASE_URL = "postgresql://mafadza:0wwwJZXRIUN15eXDUm3ls1N9JdR0wpF4@dpg-d51vkueuk2gs73a5s45g-a.oregon-postgres.render.com/mafadzatech_db"  # Replace with your actual URL

# Parse the URL
url = urlparse(DATABASE_URL)

# Connect to database
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

# Generate a password hash for 'admin123'
# This is a pbkdf2:sha256 hash for 'admin123'
password_hash = "pbkdf2:sha256:260000$MqHfIVkK$8b0b8c7f7e6d5c4b3a291827364554433221100aabbccddeeff001122334455"

# Update admin password
cursor = conn.cursor()
cursor.execute("""
    UPDATE users 
    SET password_hash = %s 
    WHERE username = 'admin'
""", (password_hash,))

conn.commit()
print(f"✅ Admin password updated to 'admin123'")
print(f"Rows affected: {cursor.rowcount}")

cursor.close()
conn.close()
