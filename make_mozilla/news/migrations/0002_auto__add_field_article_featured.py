# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Article.featured'
        db.add_column('news_article', 'featured',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Article.featured'
        db.delete_column('news_article', 'featured')

    models = {
        'news.article': {
            'Meta': {'object_name': 'Article'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'checksum': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'page': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['news']