from app.database import engine
from app.models import Base

# Import ALL models
from app.models import Feedback  
print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully")
