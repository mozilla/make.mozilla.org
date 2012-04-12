# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table('base_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('venue_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('venue_address', self.gf('django.db.models.fields.TextField')()),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('event_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(blank=True)),
        ))
        db.send_create_signal('base', ['Event'])

    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table('base_event')

    models = {
        'base.event': {
            'Meta': {'object_name': 'Event'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'event_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'venue_address': ('django.db.models.fields.TextField', [], {}),
            'venue_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['base']
