from django.db import models
import redis


class Player(models.Model):
    name = models.CharField(max_length=12, unique=True, error_messages={'unique': '이미 있는 이름이네요!'})
    coin = models.IntegerField()

    def __str__(self):
        return self.name


with redis.StrictRedis(host='127.0.0.1', port=6379, db=0) as conn:
    players = Player.objects.all().values('name', 'coin')
    for player in players:
        name = player['name']
        coin = player['coin']
        conn.zadd('coinrank', {name: coin})
    data = conn.zrange('coinrank', 0, 9, desc=True)
