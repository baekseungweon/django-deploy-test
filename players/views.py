from django.shortcuts import render, redirect
import redis
from players.forms import PlayerForm
from players.models import Player


def player_list(request):
    players = Player.objects.all().values()
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, charset="utf-8", decode_responses=True)
    range_rank = r.zrevrange('coinrank', 0, -1, withscores=True)
    result_rank = []
    for idx, data in enumerate(range_rank, 1):
        for i in players:
            if data[0] == i['name']:
                result_rank.append({
                    'rank': idx,
                    'id': i['id'],
                    'name': data[0],
                    'score': int(data[1])
                })
                break

    return render(request, 'players/player_list.html', {'result_rank': result_rank, 'players': players})


    # for i in players:
    #     for j in result_rank:
    #         if i['name'] == j['name']:
    #             j['id'] = i['id']


# def player_coinrank(request):
#     r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, charset="utf-8", decode_responses=True)
#     players = Player.objects.all().values('name', 'coin')
#     for player in players:
#         name = player['name']
#         coin = player['coin']
#         r.zadd('coinrank', {name: coin})
#     range_rank = r.zrevrange('coinrank', 0, -1, withscores=True)
#     result_rank = [{'idx': idx, 'name': data[0], 'score': int(data[1])} for idx, data in enumerate(range_rank, 1)]
#     return render(request, 'players/player_coinrank.html', {'result_rank': result_rank, 'players': players})


def player_detail(request, player_id):
    player = Player.objects.get(id=player_id)
    context = {"player": player}
    return render(request, 'players/player_detail.html', context)


def player_create(request):
    if request.method == 'POST':
        player_form = PlayerForm(request.POST)
        if player_form.is_valid():
            new_player = player_form.save()
            r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
            players = Player.objects.all().values('name', 'coin')
            for player in players:
                name = player['name']
                coin = player['coin']
                r.zadd('coinrank', {name: coin})
            return redirect('player-detail', player_id=new_player.id)
    else:
        player_form = PlayerForm()
    return render(request, 'players/player_form.html', {'form': player_form})


def player_update(request, player_id):
    player = Player.objects.get(id=player_id)
    if request.method == 'POST':
        player_form = PlayerForm(request.POST, instance=player)
        if player_form.is_valid():
            player_form.save()
            r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)  # 코인은 유저당 1개 정보만 들고 있어서, 전보다 더 높은 값인지 비교는 안함
            name = player.name
            coin = player.coin
            r.zadd('coinrank', {name: coin})
            return redirect('player-detail', player_id=player.id)
    else:
        player_form = PlayerForm(instance=player)
    return render(request, 'players/player_update.html', {'form': player_form})


def player_delete(request, player_id):
    player = Player.objects.get(id=player_id)
    if request.method == 'POST':
        player.delete()
        r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        name = player.name
        r.zrem('coinrank', name)
        return redirect('player-list')
    else:
        return render(request, 'players/player_confirm_delete.html', {'player': player})


def index(request):
    return redirect('player-list')


