# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Match'
        db.create_table(u'chess_match', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('white', self.gf('django.db.models.fields.related.ForeignKey')(related_name='White', to=orm['auth.User'])),
            ('black', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='Black', null=True, to=orm['auth.User'])),
            ('moves', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_played', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('winner', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('game_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('current_move', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('current_state', self.gf('django.db.models.fields.CharField')(max_length=72, blank=True)),
            ('white_turn', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('in_progress', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'chess', ['Match'])

        # Adding model 'Player'
        db.create_table(u'chess_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('age', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=4)),
            ('country', self.gf('django.db.models.fields.CharField')(default='USA', max_length=10)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.date.today, auto_now=True, blank=True)),
            ('reg_rating', self.gf('django.db.models.fields.DecimalField')(default=1200.0, max_digits=6, decimal_places=2)),
            ('reg_wins', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('reg_losses', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('reg_draws', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('bl_rating', self.gf('django.db.models.fields.DecimalField')(default=1200.0, max_digits=6, decimal_places=2)),
            ('bl_wins', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('bl_losses', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('bl_draws', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('bu_rating', self.gf('django.db.models.fields.DecimalField')(default=1200.0, max_digits=6, decimal_places=2)),
            ('bu_wins', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('bu_losses', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('bu_draws', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('in_match', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('all_opponents_rating', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'chess', ['Player'])

        # Adding M2M table for field matches on 'Player'
        m2m_table_name = db.shorten_name(u'chess_player_matches')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('player', models.ForeignKey(orm[u'chess.player'], null=False)),
            ('match', models.ForeignKey(orm[u'chess.match'], null=False))
        ))
        db.create_unique(m2m_table_name, ['player_id', 'match_id'])

        # Adding model 'Logedin'
        db.create_table(u'chess_logedin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.OneToOneField')(related_name='a_player', unique=True, blank=True, to=orm['chess.Player'])),
        ))
        db.send_create_signal(u'chess', ['Logedin'])


    def backwards(self, orm):
        # Deleting model 'Match'
        db.delete_table(u'chess_match')

        # Deleting model 'Player'
        db.delete_table(u'chess_player')

        # Removing M2M table for field matches on 'Player'
        db.delete_table(db.shorten_name(u'chess_player_matches'))

        # Deleting model 'Logedin'
        db.delete_table(u'chess_logedin')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'chess.logedin': {
            'Meta': {'object_name': 'Logedin'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'a_player'", 'unique': 'True', 'blank': 'True', 'to': u"orm['chess.Player']"})
        },
        u'chess.match': {
            'Meta': {'object_name': 'Match'},
            'black': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'Black'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'current_move': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'current_state': ('django.db.models.fields.CharField', [], {'max_length': '72', 'blank': 'True'}),
            'date_played': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'game_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_progress': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'moves': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'white': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'White'", 'to': u"orm['auth.User']"}),
            'white_turn': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'winner': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'chess.player': {
            'Meta': {'object_name': 'Player'},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '4'}),
            'all_opponents_rating': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bl_draws': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bl_losses': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bl_rating': ('django.db.models.fields.DecimalField', [], {'default': '1200.0', 'max_digits': '6', 'decimal_places': '2'}),
            'bl_wins': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bu_draws': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bu_losses': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bu_rating': ('django.db.models.fields.DecimalField', [], {'default': '1200.0', 'max_digits': '6', 'decimal_places': '2'}),
            'bu_wins': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'USA'", 'max_length': '10'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.date.today', 'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_match': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'matches': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'Player'", 'blank': 'True', 'to': u"orm['chess.Match']"}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'reg_draws': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'reg_losses': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'reg_rating': ('django.db.models.fields.DecimalField', [], {'default': '1200.0', 'max_digits': '6', 'decimal_places': '2'}),
            'reg_wins': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['chess']