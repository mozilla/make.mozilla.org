# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Page'
        db.create_table('pages_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('path', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('additional_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('pages', ['Page'])

        # Adding model 'PageSection'
        db.create_table('pages_pagesection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sections', to=orm['pages.Page'])),
            ('poster', self.gf('make_mozilla.core.fields.SizedImageField')(max_length=100, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('sidebar', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('pages', ['PageSection'])

        # Adding M2M table for field quotes on 'PageSection'
        db.create_table('pages_pagesection_quotes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pagesection', models.ForeignKey(orm['pages.pagesection'], null=False)),
            ('quote', models.ForeignKey(orm['pages.quote'], null=False))
        ))
        db.create_unique('pages_pagesection_quotes', ['pagesection_id', 'quote_id'])

        # Adding model 'Quote'
        db.create_table('pages_quote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quote', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.QuoteSource'], null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('show_source_image', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('pages', ['Quote'])

        # Adding model 'QuoteSource'
        db.create_table('pages_quotesource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('strapline', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('avatar', self.gf('make_mozilla.core.fields.SizedImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('pages', ['QuoteSource'])

    def backwards(self, orm):
        # Deleting model 'Page'
        db.delete_table('pages_page')

        # Deleting model 'PageSection'
        db.delete_table('pages_pagesection')

        # Removing M2M table for field quotes on 'PageSection'
        db.delete_table('pages_pagesection_quotes')

        # Deleting model 'Quote'
        db.delete_table('pages_quote')

        # Deleting model 'QuoteSource'
        db.delete_table('pages_quotesource')

    models = {
        'pages.page': {
            'Meta': {'object_name': 'Page'},
            'additional_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
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