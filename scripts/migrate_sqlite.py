"""Inspect first; explicitly copy Restrictapp 2 SQLite data into empty Postgres."""
import argparse
from contextlib import closing
import json
import os
from pathlib import Path
import re
import sqlite3
from api import storage

TABLES = {'users':['id','email','password','preferred_language'], 'trips':['id','user_id','origin','destination','created','context'],
    'profiles':['user_id','data'], 'checklist_progress':['trip_id','task_id','done']}

def read_source(path):
    if not path.is_file():
        raise ValueError('Source SQLite database does not exist.')
    with closing(sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute('BEGIN')
        tables = {r['name'] for r in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not {'users','trips'} <= tables:
            raise ValueError('Source is not a Restrictapp 2 database.')
        result = {}
        for table,columns in TABLES.items():
            rows = [dict(r) for r in connection.execute(f'SELECT * FROM {table}')] if table in tables else []
            for row in rows:
                if table == 'trips': row.setdefault('context','{}')
                if table == 'users': row.setdefault('preferred_language','en')
                if any(column not in row for column in columns):
                    raise ValueError('Source schema is unsupported.')
                if table == 'users' and not re.fullmatch(r'[0-9a-f]{32}:[0-9a-f]{128}',row['password']):
                    raise ValueError('Unsupported password format; plaintext legacy credentials cannot be migrated.')
                for column in ('context','data'):
                    if column in row: json.loads(row[column])
            result[table] = rows
        return result

def copy_to_postgres(rows, database):
    with database() as db:
        if not db.postgres:
            raise ValueError('Migration target must be PostgreSQL.')
        db.execute('LOCK TABLE users,trips,profiles,checklist_progress,sessions IN ACCESS EXCLUSIVE MODE')
        for table in [*TABLES,'sessions']:
            if db.execute(f'SELECT COUNT(*) AS count FROM {table}').fetchone()['count']:
                raise ValueError('Target must be empty; existing records will not be overwritten.')
        for table,columns in TABLES.items():
            for row in rows[table]:
                db.execute(f"INSERT INTO {table}({','.join(columns)}) VALUES ({','.join('?' for _ in columns)})",tuple(row.get(c,'en') if c=='preferred_language' else row[c] for c in columns))
        for table in ('users','trips'):
            db.execute(f"SELECT setval(pg_get_serial_sequence('{table}','id'), COALESCE(MAX(id),1), MAX(id) IS NOT NULL) FROM {table}")
        for table in TABLES:
            actual = db.execute(f'SELECT COUNT(*) AS count FROM {table}').fetchone()['count']
            if actual != len(rows[table]):
                raise ValueError('Migration row count mismatch; transaction will be rolled back.')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=Path('api/data/restrictapp.sqlite3'))
    parser.add_argument('--apply',action='store_true',help='Copy into the empty database named by DATABASE_URL')
    args = parser.parse_args()
    try:
        rows = read_source(args.source.resolve())
        print(json.dumps({'rows':{table:len(values) for table,values in rows.items()},'sessions':'not copied'},indent=2))
        if not args.apply:
            print('Inspection only. No destination connection or data changes were made.')
            return
        if not os.getenv('DATABASE_URL'):
            raise ValueError('Set DATABASE_URL in the process environment before applying.')
        copy_to_postgres(rows,lambda:storage.database(args.source))
        print('Migration committed. Users must sign in again. Source SQLite was not modified.')
    except ValueError as error:
        parser.exit(1,str(error)+'\n')
    except Exception:
        parser.exit(1,'Migration failed; imported rows were rolled back. Check connectivity and source integrity. No credentials are printed.\n')

if __name__ == '__main__':
    main()
