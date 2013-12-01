# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Letter'
        db.create_table(u'voter_letter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('letter', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'voter', ['Letter'])

        # Adding model 'MatchUp'
        db.create_table(u'voter_matchup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('letter_a', self.gf('django.db.models.fields.related.ForeignKey')(related_name='left', to=orm['voter.Letter'])),
            ('letter_b', self.gf('django.db.models.fields.related.ForeignKey')(related_name='right', to=orm['voter.Letter'])),
        ))
        db.send_create_signal(u'voter', ['MatchUp'])

        # Adding model 'Vote'
        db.create_table(u'voter_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('letter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voter.Letter'])),
            ('matchup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voter.MatchUp'])),
        ))
        db.send_create_signal(u'voter', ['Vote'])


    def backwards(self, orm):
        # Deleting model 'Letter'
        db.delete_table(u'voter_letter')

        # Deleting model 'MatchUp'
        db.delete_table(u'voter_matchup')

        # Deleting model 'Vote'
        db.delete_table(u'voter_vote')


    models = {
        u'voter.letter': {
            'Meta': {'object_name': 'Letter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'letter': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'voter.matchup': {
            'Meta': {'object_name': 'MatchUp'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter_a': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'left'", 'to': u"orm['voter.Letter']"}),
            'letter_b': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'right'", 'to': u"orm['voter.Letter']"})
        },
        u'voter.vote': {
            'Meta': {'object_name': 'Vote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voter.Letter']"}),
            'matchup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voter.MatchUp']"})
        }
    }

    complete_apps = ['voter']