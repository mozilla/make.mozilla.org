# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Page', fields ['path']
        db.delete_unique('pages_page', ['path'])

        # Adding field 'Page.real_path'
        # We'll set the column up to accept nulls for now, and fix it in when we're done
        db.add_column('pages_page', 'real_path',
                      self.gf('django.db.models.fields.CharField')(default=None, null=True, blank=True, unique=True, max_length=1024),
                      keep_default=False)

        # Adding field 'Page.parent'
        db.add_column('pages_page', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page'], null=True, blank=True),
                      keep_default=False)

        if not db.dry_run:
            # Correctly set 'real_path' value
            for page in orm.Page.objects.all():
                # As we're only just introducing parents, we know nothing complicated is happening
                page.real_path = page.path
                page.save()

        # Changing field 'Page.real_path'
        # Removing that 'null' option
        db.alter_column('pages_page', 'real_path',
                        self.gf('django.db.models.fields.CharField')(blank=True, unique=True, max_length=1024))

    def backwards(self, orm):
        # Deleting field 'Page.real_path'
        db.delete_column('pages_page', 'real_path')

        # Deleting field 'Page.parent'
        db.delete_column('pages_page', 'parent_id')

        # Adding unique constraint on 'Page', fields ['path']
        db.create_unique('pages_page', ['path'])

    models = {
        'pages.page': {
            'Meta': {'object_name': 'Page'},
            'additional_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pages.Page']", 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'real_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'}),
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