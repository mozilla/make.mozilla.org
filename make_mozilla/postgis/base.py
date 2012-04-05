from django.db.backends.postgresql_psycopg2.base import *
from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper as Psycopg2DatabaseWrapper
from django.contrib.gis.db.backends.postgis.creation import PostGISCreation
from django.contrib.gis.db.backends.postgis.introspection import PostGISIntrospection
from django.contrib.gis.db.backends.postgis.operations import PostGISOperations
from django.contrib.gis.db.backends.postgis.adapter import PostGISAdapter
import psycopg2

class PatchedPostGISAdapter(PostGISAdapter):
    def __init__(self, geom):
        super(PatchedPostGISAdapter, self).__init__(geom)
        self._adapter = psycopg2.Binary(self.ewkb)

    def prepare(self, conn):
        """
        This method allows escaping the binary in the style required by the
        server's `standard_conforming_string` setting.
        """
        self._adapter.prepare(conn)

    def getquoted(self):
        "Returns a properly quoted string for use in PostgreSQL/PostGIS."
        # psycopg will figure out whether to use E'\\000' or '\000'
        return 'ST_GeomFromEWKB(%s)' % self._adapter.getquoted()

class PatchedPostGISOperations(PostGISOperations):
    Adapter = PatchedPostGISAdapter
    Adaptor = Adapter # Backwards-compatibility alias.

class DatabaseWrapper(Psycopg2DatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.creation = PostGISCreation(self)
        self.ops = PatchedPostGISOperations(self)
        self.introspection = PostGISIntrospection(self)

