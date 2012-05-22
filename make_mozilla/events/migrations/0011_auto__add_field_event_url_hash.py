# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.url_hash'
        db.add_column('events_event', 'url_hash',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Event.url_hash'
        db.delete_column('events_event', 'url_hash')

    models = {
        'events.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Campaign']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.EventKind']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'official': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'organiser_email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'url_hash': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Venue']"}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'events.eventkind': {
            'Meta': {'object_name': 'EventKind'},
            'additional': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'figures': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'events.partner': {
            'Meta': {'object_name': 'Partner'},
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'for_campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Campaign']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'events.venue': {
            'Meta': {'object_name': 'Venue'},
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street_address': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['events']