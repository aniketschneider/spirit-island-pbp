import uuid
from django.db import models

class Spirit(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name

    def starting_hand(self):
        return Card.objects.filter(spirit_id=self.id)

    def url(self):
        return '/pbf/' + self.name.lower() + '.jpg'

class Card(models.Model):
    MINOR = 0
    MAJOR = 1
    UNIQUE = 2

    name = models.CharField(max_length=255, blank=False)
    TYPES = (
        (MINOR, 'Minor'),
        (MAJOR, 'Major'),
        (UNIQUE, 'Unique'),
    )
    type = models.IntegerField(choices=TYPES)
    spirit = models.ForeignKey(Spirit, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def url(self):
        return '/pbf/' + self.name.replace(",", '').replace("-", '').replace("'", '').replace(' ', '_').lower() + '.jpg'

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    turn = models.IntegerField(default=1)
    name = models.CharField(max_length=255, blank=False)
    minor_deck = models.ManyToManyField(Card, related_name='minor_deck')
    major_deck = models.ManyToManyField(Card, related_name='major_deck')
    screenshot = models.ImageField(upload_to='screenshot', blank=True)
    discord_channel = models.CharField(max_length=255, default="")

    def __str__(self):
        return str(self.id)

class GamePlayer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    spirit = models.ForeignKey(Spirit, blank=False, on_delete=models.CASCADE)
    hand = models.ManyToManyField(Card, related_name='hand')
    discard = models.ManyToManyField(Card, related_name='discard')
    play = models.ManyToManyField(Card, related_name='play')
    selection = models.ManyToManyField(Card, related_name='selection')
    ready = models.BooleanField(default=False)
    energy = models.IntegerField(default=0)
    notes = models.TextField()

class Presence(models.Model):
    game_player = models.ForeignKey(GamePlayer, on_delete=models.CASCADE)
    left = models.IntegerField()
    top = models.IntegerField()
    opacity = models.FloatField(default=1.0)

class GameLog(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    text = models.CharField(max_length=255, blank=False)
