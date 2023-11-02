from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Date, update
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
DateTime = "DateTime - модуль"


Base = declarative_base()

class DBHelper:
    def __init__(self, data_base_name: str):
        self.__engine = create_engine(f'sqlite:///{data_base_name}')
        self.__Session = sessionmaker(bind=self.__engine)
        self.__session = self.__Session()
        Base.metadata.create_all(self.__engine)

    def insert_info_user(self, user_id: str, user_name: str):
        user_info_obj = User(user_id=user_id, user_name=user_name)
        self.__session.add(user_info_obj)
        self.__session.commit()
        return user_info_obj.id
    
    def insert_info_admin(self, admin_id: str, admin_name: str):
        admin_info_obj = Admin(admin_id=admin_id, admin_name=admin_name)
        self.__session.add(admin_info_obj)
        self.__session.commit()

    def insert_photo(self, user_id: str, photo_id: str):
        photo_obj = Photo(user_id=user_id, photo_id=photo_id)
        self.__session.add(photo_obj)
        self.__session.commit()

    def insert_data_detected_photo(self, user_id: str, count_object: str, face_value_money: str, date: DateTime, photo_id: str):
        dec_photo_obj = DetectedPhoto(user_id=user_id, count_object=count_object, face_value_money=face_value_money, date=date, photo_id=photo_id)
        self.__session.add(dec_photo_obj)
        self.__session.commit()

    def insert_data_favorite_photo(self, user_id: str, count_object: str, face_value_money: str, photo_id: str, message_id: str):
        fav_photo_obj = Favorite(user_id=user_id, count_object=count_object, face_value_money=face_value_money, photo_id=photo_id, message_id=message_id)
        self.__session.add(fav_photo_obj)
        self.__session.commit()
    
    def insert_data_incorrect_detected_photo(self, photo_id):
        incor_photo = IncorrectDetection(photo_id=photo_id)
        self.__session.add(incor_photo)
        self.__session.commit()
    
    def update_message_id(self, message_id: str, id: int):
        up_message_id = update(Favorite).where(Favorite.id == id).values(message_id=message_id)
        self.__session.execute(up_message_id)
        self.__session.commit()

    def get_photo_id(self, user_id: str) -> list[object]:
        photo_obj = self.__session.query(Photo).filter_by(user_id=user_id).order_by(Photo.id.desc()).first()
        return photo_obj
    
    def get_message_info(self, user_id: str) -> list[object]:
        photos = self.__session.query(DetectedPhoto).filter_by(user_id=user_id).all()
        return photos
    
    def get_history_photos(self, user_id: str) -> str:
        photos = self.get_message_info(user_id)
        message = ''
        if len(photos) > 0:
            for column in photos:
                message += (f'Сообщение от {".".join(str(column.date).split("-")[::-1])}:\nКол-во объектов: {column.count_object}\nСумма: {column.face_value_money}\n')
            return message
        else:
            return message
        
    def get_data_detected_photos(self, user_id: str) -> str|tuple: 
        photos = self.get_message_info(user_id)
        if len(photos) > 0:
            return photos[-1].count_object, photos[-1].face_value_money, photos[-1].photo_id
        else:
            return ''
        
    def get_data_favorite_photos(self, user_id: str) -> str|tuple:
        photos = self.__session.query(Favorite).filter_by(user_id=user_id).all()
        list_message = []
        list_photo_id = []
        list_column_id = []
        if len(photos) > 0:
            for column in photos:
                list_message.append(f'Кол-во объектов: {column.count_object}\nСумма: {column.face_value_money}\n')
                list_photo_id.append(column.photo_id)
                list_column_id.append(column.id)
            return list_message, list_photo_id, list_column_id
        else:
            return list_message
    
    def get_id_photo_from_favorite(self, message_id: str) -> str:
        photo_obj = self.__session.query(Favorite).filter(Favorite.message_id == message_id).first()
        return photo_obj.photo_id
    
    def delete_favorite_photo(self, message_id: str):
        row = self.__session.query(Favorite).filter(Favorite.message_id == message_id).first()
        fav_photo = self.__session.query(Favorite).filter(Favorite.id == row.id).first()
        self.__session.delete(fav_photo)
        self.__session.commit()
    
        
class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    photo_id = Column(String, nullable=False)
    user = relationship("User", back_populates="photos")

class DetectedPhoto(Base):
    __tablename__ = 'dec_photos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id')) 
    count_object = Column(String)
    face_value_money = Column(String)
    date = Column(Date)
    photo_id = Column(String)
    user = relationship("User", back_populates="detected_photos")

class Favorite(Base):
    __tablename__ = 'favorite'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id')) 
    count_object = Column(String)
    face_value_money = Column(String)
    photo_id = Column(String)
    message_id = Column(String)
    user = relationship("User", back_populates="favorites")

class IncorrectDetection(Base):
    __tablename__ = 'incorrect'
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(String)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String)
    user_id = Column(Integer)
    photos = relationship("Photo", back_populates="user")
    detected_photos = relationship("DetectedPhoto", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer)
    admin_name = Column(String)

