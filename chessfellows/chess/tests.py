from django.test import TestCase
from chess.models import Match, Player, User


class MatchTests(TestCase):

    def setUp(self):

        self.usr1 = User(username="Eyuel")
        self.usr2 = User(username="Josh")
        self.player1 = Player(user=self.usr1)
        self.player2 = Player(user=self.usr2)

        self.table = Match(white=self.usr1, black=self.usr2)


    def test_player_creation(self):

        self.assertEqual(self.usr1.username, "Eyuel")
        self.assertEqual(self.usr2.username, "Josh")
        self.assertEqual(self.player1.user, self.usr1)
        self.assertEqual(self.player2.user, self.usr2)