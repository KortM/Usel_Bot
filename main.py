import os
from bd import Session, Usel, engine, Base
import openpyxl

class Worker:

    def __init__(self) -> None:
        self.file_path = ''

    def upload_file(self) -> str:
        '''
            Открываем файл с узлами и пишем в БД
        '''
        session = Session()
        wookbook = openpyxl.load_workbook(self.file_path)
        sheet = wookbook.active
        print(sheet.max_row)
        for i in range(0, sheet.max_row):
            tmp = []
            for col in sheet.iter_cols(1, sheet.max_column):
                tmp.append(str(col[i].value))
            usel = Usel(description = ''.join(tmp))
            session.add(usel)
            session.commit()

    def find_data(self, name: str) -> list:
        '''
            Ещем узел в БД по описанию, через LIKE SQL
        '''
        session = Session()
        result = session.query(Usel).filter(Usel.description.like('%{}%'.format(name))).all()
        if result:
            return result
        else:
            return 'Узел не найден!'
    
    def drop_data(self) -> str:
        '''
            Перед запуском убираем БД и создаем новую, пустую. 
        '''
        try:
            os.remove('BD.db')
            Base.metadata.create_all(engine)
        except Exception:
            pass

    def start(self, path: str) -> None:
        '''
            Запуск:
            1. Указываем путь к файлу,
            2. Убираем базу, если она есть и создаем новую,
            3. Заполняем БД. 
        '''
        self.file_path = path
        self.drop_data()
        self.upload_file()
