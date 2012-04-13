# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Venue'
        db.create_table('events_venue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('street_address', self.gf('django.db.models.fields.TextField')()),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(blank=True)),
        ))
        db.send_create_signal('events', ['Venue'])

        # Adding model 'Event'
        db.create_table('events_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('event_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Venue'])),
        ))
        db.send_create_signal('events', ['Event'])

    def backwards(self, orm):
        # Deleting model 'Venue'
        db.delete_table('events_venue')

        # Deleting model 'Event'
        db.delete_table('events_event')

    models = {
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'event_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Venue']"})
        },
        'events.venue': {
            'Meta': {'object_name': 'Venue'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street_address': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['events']