# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Page.show_subnav'
        db.add_column('pages_page', 'show_subnav',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Page.subnav_title'
        db.add_column('pages_page', 'subnav_title',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PageSection.subnav_title'
        db.add_column('pages_pagesection', 'subnav_title',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Page.show_subnav'
        db.delete_column('pages_page', 'show_subnav')

        # Deleting field 'Page.subnav_title'
        db.delete_column('pages_page', 'subnav_title')

        # Deleting field 'PageSection.subnav_title'
        db.delete_column('pages_pagesection', 'subnav_title')

    models = {
        'pages.page': {
            'Meta': {'object_name': 'Page'},
            'additional_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'show_subnav': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subnav_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'pages.pagesection': {
            'Meta': {'ordering': "['id']", 'object_name': 'PageSection'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': "orm['pages.Page']"}),
            'poster': ('make_mozilla.core.fields.SizedImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'quotes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['pages.Quote']", 'null': 'True', 'blank': 'True'}),
            'sidebar': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subnav_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'pages.quote': {
            'Meta': {'object_name': 'Quote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quote': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'show_source_image': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pages.QuoteSource']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'pages.quotesource': {
            'Meta': {'object_name': 'QuoteSource'},
            'avatar': ('make_mozilla.core.fields.SizedImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'strapline': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['pages']
