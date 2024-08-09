import os
import sqlite3


class DatabaseHelper():
    PATH_DATABASE = './database_v2.db'

    def __init__(self):

        if os.path.exists(self.PATH_DATABASE) == False:
            self.create_table()

    def create_table(self):

        db = sqlite3.connect(self.PATH_DATABASE)
        cursor = db.cursor()

        cursor.execute('CREATE TABLE packdata('
                       'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                       'name TEXT, '
                       'icon TEXT, '
                       'description TEXT, '
                       'header_uuid TEXT, '
                       'modules_uuid TEXT, '
                       'version TEXT, '
                       'sourcelist TEXT, '
                       'bundle TEXT);')
        db.commit()
        db.close()

    def insert_record(self, name, icon, description, header_uuid, modules_uuid, version, records, bundle):

        records = self.convert_cvs_from_list(records)
        bundle = self.convert_cvs_from_list_bundle(bundle)
        db = sqlite3.connect(self.PATH_DATABASE)
        cursor = db.cursor()

        sql = 'INSERT INTO packdata VALUES (?,?,?,?,?,?,?,?,?);'
        data = (None, name, icon, description, header_uuid, modules_uuid, version, records, bundle)
        cursor.execute(sql, data)
        db.commit()
        db.close()

    def update_record(self, index, name, icon, description, header_uuid, modules_uuid, version, records, bundle):

        records = self.convert_cvs_from_list(records)
        bundle = self.convert_cvs_from_list_bundle(bundle)
        db = sqlite3.connect(self.PATH_DATABASE)
        cursor = db.cursor()
        cursor.execute('UPDATE packdata SET name=? WHERE id=?', (name, index))
        cursor.execute('UPDATE packdata SET icon=? WHERE id=?', (icon, index))
        cursor.execute('UPDATE packdata SET description=? WHERE id=?', (description, index))
        cursor.execute('UPDATE packdata SET header_uuid=? WHERE id=?', (header_uuid, index))
        cursor.execute('UPDATE packdata SET modules_uuid=? WHERE id=?', (modules_uuid, index))
        cursor.execute('UPDATE packdata SET version=? WHERE id=?', (version, index))
        cursor.execute('UPDATE packdata SET sourcelist=? WHERE id=?', (records, index))
        cursor.execute('UPDATE packdata SET bundle=? WHERE id=?', (bundle, index))
        db.commit()
        db.close()

    def delete_record(self, index):
        db = sqlite3.connect(self.PATH_DATABASE)
        cursor = db.cursor()
        cursor.execute('DELETE FROM packdata WHERE id=?', (index,))
        db.commit()
        db.close()

    def get_packdatalist(self):

        db = sqlite3.connect(self.PATH_DATABASE)
        cursor = db.cursor()
        cursor.execute('SELECT * FROM packdata')
        packdatalist = []

        for row in cursor.fetchall():
            '''
            row[0] index
            row[1] name
            row[2] icon
            row[3] description
            row[4] header_uuid
            row[5] modules_uuid
            row[6] version
            row[7] sourcelist
            row[8] bundle
            '''
            newsourcelist = self.convert_list_from_cvs(row[7])
            bundlelist = self.convert_list_from_cvs_bundle(row[8])
            packdatalist.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], newsourcelist, bundlelist])

        db.close()
        packdatalist.reverse()
        return packdatalist

    def convert_cvs_from_list(self, records):
        '''
        [[sound1, ogg1],[sound2, ogg2],[sound3, ogg3]]
        'sound1*ogg1|sound2*ogg2|sound3*ogg'
        '''
        cvs = ''
        for soundfile, ogg in records:
            cvs = cvs + soundfile + '*' + ogg + '|'
        return cvs[0:-1]

    def convert_list_from_cvs(self, cvs):

        list_newsource = []
        list_sound_ogg = cvs.split('|')

        for sound_ogg in list_sound_ogg:
            s_o = sound_ogg.split('*')
            list_newsource.append([s_o[0], s_o[1]])

        return list_newsource

    def convert_list_from_cvs_bundle(self, cvs):

        if cvs == '':
            return []
        else:
            _list = cvs.split('|')
            return [x for x in _list if x]

    def convert_cvs_from_list_bundle(self, bundle):

        if bundle == []:
            return ''
        else:
            cvs = ''
            for b in bundle:
                cvs = cvs + b + '|'
            return cvs[0:-1]
