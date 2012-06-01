# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table('projects_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('teaser', self.gf('django.db.models.fields.TextField')()),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url_hash', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('image', self.gf('make_mozilla.core.fields.SizedImageField')(max_length=100)),
            ('contributor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Contributor'], null=True, blank=True)),
            ('tool', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tools.Tool'], null=True, blank=True)),
            ('difficulty', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Difficulty'], null=True, blank=True)),
        ))
        db.send_create_signal('projects', ['Project'])

        # Adding M2M table for field audience on 'Project'
        db.create_table('projects_project_audience', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['projects.project'], null=False)),
            ('audience', models.ForeignKey(orm['projects.audience'], null=False))
        ))
        db.create_unique('projects_project_audience', ['project_id', 'audience_id'])

        # Adding M2M table for field skills on 'Project'
        db.create_table('projects_project_skills', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['projects.project'], null=False)),
            ('skill', models.ForeignKey(orm['projects.skill'], null=False))
        ))
        db.create_unique('projects_project_skills', ['project_id', 'skill_id'])

        # Adding model 'ProjectStep'
        db.create_table('projects_projectstep', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='steps', to=orm['projects.Project'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('projects', ['ProjectStep'])

        # Adding model 'Audience'
        db.create_table('projects_audience', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('index', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=2)),
        ))
        db.send_create_signal('projects', ['Audience'])

        # Adding model 'Difficulty'
        db.create_table('projects_difficulty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('index', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=2)),
        ))
        db.send_create_signal('projects', ['Difficulty'])

        # Adding model 'Skill'
        db.create_table('projects_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('index', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=2)),
        ))
        db.send_create_signal('projects', ['Skill'])

        # Adding model 'Contributor'
        db.create_table('projects_contributor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('local_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Partner'], null=True, blank=True)),
        ))
        db.send_create_signal('projects', ['Contributor'])

    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table('projects_project')

        # Removing M2M table for field audience on 'Project'
        db.delete_table('projects_project_audience')

        # Removing M2M table for field skills on 'Project'
        db.delete_table('projects_project_skills')

        # Deleting model 'ProjectStep'
        db.delete_table('projects_projectstep')

        # Deleting model 'Audience'
        db.delete_table('projects_audience')

        # Deleting model 'Difficulty'
        db.delete_table('projects_difficulty')

        # Deleting model 'Skill'
        db.delete_table('projects_skill')

        # Deleting model 'Contributor'
        db.delete_table('projects_contributor')

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
        'projects.audience': {
            'Meta': {'ordering': "['index', 'id']", 'object_name': 'Audience'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
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
            'audience': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['projects.Audience']", 'null': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Contributor']", 'null': 'True', 'blank': 'True'}),
            'difficulty': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Difficulty']", 'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('make_mozilla.core.fields.SizedImageField', [], {'max_length': '100'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['projects.Skill']", 'null': 'True', 'blank': 'True'}),
            'teaser': ('django.db.models.fields.TextField', [], {}),
            'tool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tools.Tool']", 'null': 'True', 'blank': 'True'}),
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