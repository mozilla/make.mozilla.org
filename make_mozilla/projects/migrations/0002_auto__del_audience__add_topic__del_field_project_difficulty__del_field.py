# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Audience'
        db.delete_table('projects_audience')

        # Adding model 'Topic'
        db.create_table('projects_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('index', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=2)),
        ))
        db.send_create_signal('projects', ['Topic'])

        # Deleting field 'Project.difficulty'
        db.delete_column('projects_project', 'difficulty_id')

        # Deleting field 'Project.tool'
        db.delete_column('projects_project', 'tool_id')

        # Removing M2M table for field audience on 'Project'
        db.delete_table('projects_project_audience')

        # Adding M2M table for field tools on 'Project'
        db.create_table('projects_project_tools', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['projects.project'], null=False)),
            ('tool', models.ForeignKey(orm['tools.tool'], null=False))
        ))
        db.create_unique('projects_project_tools', ['project_id', 'tool_id'])

        # Adding M2M table for field tpoics on 'Project'
        db.create_table('projects_project_tpoics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['projects.project'], null=False)),
            ('topic', models.ForeignKey(orm['projects.topic'], null=False))
        ))
        db.create_unique('projects_project_tpoics', ['project_id', 'topic_id'])

        # Adding M2M table for field difficulties on 'Project'
        db.create_table('projects_project_difficulties', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['projects.project'], null=False)),
            ('difficulty', models.ForeignKey(orm['projects.difficulty'], null=False))
        ))
        db.create_unique('projects_project_difficulties', ['project_id', 'difficulty_id'])

    def backwards(self, orm):
        # Adding model 'Audience'
        db.create_table('projects_audience', (
            ('index', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=2)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('projects', ['Audience'])

        # Deleting model 'Topic'
        db.delete_table('projects_topic')

        # Adding field 'Project.difficulty'
        db.add_column('projects_project', 'difficulty',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Difficulty'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.tool'
        db.add_column('projects_project', 'tool',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tools.Tool'], null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field audience on 'Project'
        db.create_table('projects_project_audience', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['projects.project'], null=False)),
            ('audience', models.ForeignKey(orm['projects.audience'], null=False))
        ))
        db.create_unique('projects_project_audience', ['project_id', 'audience_id'])

        # Removing M2M table for field tools on 'Project'
        db.delete_table('projects_project_tools')

        # Removing M2M table for field tpoics on 'Project'
        db.delete_table('projects_project_tpoics')

        # Removing M2M table for field difficulties on 'Project'
        db.delete_table('projects_project_difficulties')

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
            'Meta': {'ordering': "['index', 'id']", 'object_name': 'Difficulty'},
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
            'teaser': ('django.db.models.fields.TextField', [], {}),
            'tools': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tools.Tool']", 'null': 'True', 'blank': 'True'}),
            'tpoics': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['projects.Topic']", 'null': 'True', 'blank': 'True'}),
            'url_hash': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'projects.projectstep': {
            'Meta': {'object_name': 'ProjectStep'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'steps'", 'to': "orm['projects.Project']"})
        },
        'projects.skill': {
            'Meta': {'ordering': "['index', 'id']", 'object_name': 'Skill'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'projects.topic': {
            'Meta': {'ordering': "['index', 'id']", 'object_name': 'Topic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'tools.tool': {
            'Meta': {'object_name': 'Tool'},
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