# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        import hashlib

        # Adding field 'Project.slug'
        db.add_column('projects_project', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='', unique=False, max_length=50),
                      keep_default=False)

        if not db.dry_run:
            db.start_transaction()
            # Set project slug from previously generated URL hash
            for project in orm.Project.objects.all():
                if not project.url_hash:
                    project.url_hash = hashlib.sha224('%d' % project.id).hexdigest()[:9]
                if not project.slug:
                    project.slug = project.url_hash
                project.save()
            db.commit_transaction()

            # Slug should be unique, but we can't create column with multiple
            # empty 'slugs', so doing it after population
            db.create_unique('projects_project', ['slug'])

    def backwards(self, orm):
        # Deleting field 'Project.slug'
        db.delete_column('projects_project', 'slug')

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
        'events.partner': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Partner'},
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'for_campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Campaign']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'projects.contributor': {
            'Meta': {'object_name': 'Contributor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Partner']", 'null': 'True', 'blank': 'True'})
        },
        'projects.difficulty': {
            'Meta': {'ordering': "['index', 'label', 'id']", 'object_name': 'Difficulty'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'projects.project': {
            'Meta': {'ordering': "['-added']", 'object_name': 'Project'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Contributor']", 'null': 'True', 'blank': 'True'}),
            'difficulties': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['projects.Difficulty']", 'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('make_mozilla.core.fields.SizedImageField', [], {'max_length': '100'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['projects.Skill']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            'teaser': ('django.db.models.fields.TextField', [], {}),
            'tools': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tools.Tool']", 'null': 'True', 'blank': 'True'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['projects.Topic']", 'null': 'True', 'blank': 'True'}),
            'url_hash': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'projects.projectstep': {
            'Meta': {'object_name': 'ProjectStep'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'steps'", 'to': "orm['projects.Project']"})
        },
        'projects.skill': {
            'Meta': {'ordering': "['index', 'label', 'id']", 'object_name': 'Skill'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'projects.topic': {
            'Meta': {'ordering': "['index', 'label', 'id']", 'object_name': 'Topic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'tools.tool': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tool'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'strapline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['projects']