from app.database import engine
from app.models import Base

# Import ALL models so they register
from app.models import Feedback  # add this line
# also import other models if needed

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully")