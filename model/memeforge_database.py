from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from PIL import Image
import base64
from io import BytesIO
import json 

Base = declarative_base()

def initializeDatabase():
    global engine, Session, session

    engine = create_engine('sqlite:///database2.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

def clearDatabase():
    initializeDatabase()
    session.query(Images).delete()
    session.commit()
    session.close()

class Images(Base):
    __tablename__ = 'images'
    imageName = Column(String, primary_key=True, nullable=False, unique=False)  # Added nullable=False for primary key
    imageFunc = Column(String, nullable=False, unique=False)  # Added nullable=False for non-nullable columns
    imageBase64 = Column(String, nullable=False, unique=False)

def createImage(name, func, image):
    initializeDatabase()
    newImage = Images(imageName=name, imageFunc=func, imageBase64=image)
    session.add(newImage)
    session.commit()

def queryImages():
    initializeDatabase()
    images = session.query(Images).all()
    image_list = []

    for image in images:
        image_data = {
            'name': image.imageName,
            'func': image.imageFunc,
            'image': image.imageBase64
        }
        image_list.append(image_data)

    return json.dumps(image_list)  

def debugDatabase():
    print('debugged')

    