# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Letter.archived'
        db.add_column(u'voter_letter', 'archived',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Letter.archived'
        db.delete_column(u'voter_letter', 'archived')


    models = {
        u'voter.letter': {
            'Meta': {'object_name': 'Letter'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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